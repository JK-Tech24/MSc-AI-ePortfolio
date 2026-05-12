
import json
import re
import sys
import platform
import hashlib
from pathlib import Path
from datetime import datetime, timezone

import numpy as np
import pandas as pd
import yaml

RAW = Path("data/01_raw")
OUT = Path("data/05_bi")
OUT.mkdir(parents=True, exist_ok=True)

CONFIG_THRESH = Path("config/thresholds.yaml")
AUDIT_PATH = OUT / "audit_log.csv"

# Keep the same exception handling already present in the current pipeline:
# this project can pass with the same extracted panel even if numeric coverage
# is below the global quality gate, provided the same conditions hold.
PARTIAL_QUALITY_PROJECTS = {"P020"}


# --------------------------------------------------
# Helpers
# --------------------------------------------------
def now_utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def safe_num(x):
    return pd.to_numeric(x, errors="coerce")


def parse_project_id_from_filename(name: str) -> str:
    m = re.search(r"(P\d{3})", name, re.IGNORECASE)
    return m.group(1).upper() if m else Path(name).stem[:20]


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def load_thresholds(fp: Path) -> dict:
    """
    Loads thresholds.yaml (single source of truth).
    Uses safe defaults if the file is missing or incomplete.
    """
    defaults = {
        "tiers": {"high": 0.85, "medium": 0.70, "low": 0.50},
        "evm": {"cpi_warn": 0.90, "spi_warn": 0.90},
        "quality": {"min_numeric_pct": 60, "min_input_rows": 5},
    }
    if not fp.exists():
        return defaults

    try:
        cfg = yaml.safe_load(fp.read_text(encoding="utf-8")) or {}
    except Exception:
        return defaults

    cfg.setdefault("tiers", defaults["tiers"])
    cfg.setdefault("evm", defaults["evm"])
    cfg.setdefault("quality", defaults["quality"])
    return cfg


def numeric_coverage_pct(panel: pd.DataFrame, cols) -> float:
    """
    Numeric coverage = % of non-null cells in a set of numeric columns.
    """
    if panel is None or panel.empty:
        return 0.0
    denom = len(panel) * len(cols)
    if denom == 0:
        return 0.0
    num = panel[cols].notna().sum().sum()
    return float(100.0 * num / denom)


def ensure_columns(df: pd.DataFrame, cols) -> pd.DataFrame:
    out = df.copy()
    for c in cols:
        if c not in out.columns:
            out[c] = np.nan
    return out[cols]


def write_csv(df: pd.DataFrame, path: Path, columns=None):
    if columns is not None:
        df = ensure_columns(df, columns)
    df.to_csv(path, index=False)


# --------------------------------------------------
# Column detection (ROBUST)
# --------------------------------------------------
def detect_columns(df: pd.DataFrame):
    cols = {}
    for c in df.columns:
        if pd.isna(c):
            continue
        cols[str(c).strip().lower()] = c

    def pick(*cands):
        for cand in cands:
            k = str(cand).strip().lower()
            if k in cols:
                return cols[k]
        return None

    return {
        "period_end": pick(
            "period_end",
            "period end",
            "period",
            "as_of",
            "asof",
            "status date",
            "date",
            "period end date",
        ),
        "PV": pick("pv", "planned value", "planned_value", "bcws"),
        "EV": pick("ev", "earned value", "earned_value", "bcwp"),
        "AC": pick("ac", "actual cost", "actual_cost", "acwp"),
        "CPI": pick("cpi", "cost performance index"),
        "SPI": pick("spi", "schedule performance index"),
        "CV": pick("cv", "cost variance"),
        "SV": pick("sv", "schedule variance"),
    }


# --------------------------------------------------
# Header row auto-detection
# --------------------------------------------------
def _find_header_row(xlsx_path: Path, sheet_name: str, tokens, max_rows=30):
    preview = pd.read_excel(xlsx_path, sheet_name=sheet_name, header=None, nrows=max_rows)
    best_row, best_hits = None, 0

    for i in range(len(preview)):
        row = preview.iloc[i].astype(str).str.lower().tolist()
        hits = sum(any(t in cell for cell in row) for t in tokens)
        if hits > best_hits:
            best_hits, best_row = hits, i

    return best_row if best_hits >= 2 else None


# --------------------------------------------------
# Panel extraction
# --------------------------------------------------
def compute_panel_from_any_sheet(xlsx_path: Path, pid: str) -> pd.DataFrame:
    try:
        xls = pd.ExcelFile(xlsx_path)
    except Exception:
        return pd.DataFrame()

    best_df, best_score = None, -1
    best_sheet, best_header = None, None

    tokens = ["pv", "planned", "ev", "earned", "ac", "actual", "cpi", "spi"]

    for sh in xls.sheet_names:
        try:
            header = _find_header_row(xlsx_path, sh, tokens)
            df = pd.read_excel(xlsx_path, sheet_name=sh, header=header if header is not None else 0)
            df.columns = [c if pd.notna(c) else f"unnamed_{i}" for i, c in enumerate(df.columns)]
        except Exception:
            continue

        if df.empty:
            continue

        col = detect_columns(df)
        score = sum(col[k] is not None for k in ["PV", "EV", "AC", "CPI", "SPI"])

        if score > best_score:
            best_score, best_df = score, df
            best_sheet, best_header = sh, header

    if best_df is None or best_score < 2:
        return pd.DataFrame()

    df = best_df.copy()
    col = detect_columns(df)

    # period_end
    if col["period_end"]:
        synthetic_dates = False
        df["period_end"] = pd.to_datetime(df[col["period_end"]], errors="coerce")
    else:
        synthetic_dates = True
        df["period_end"] = pd.date_range(end=pd.Timestamp.today(), periods=len(df), freq="M")

    # numeric columns
    for k in ["PV", "EV", "AC", "CPI", "SPI", "CV", "SV"]:
        df[k] = safe_num(df[col[k]]) if col[k] else np.nan

    core = ["PV", "EV", "AC", "CPI", "SPI", "CV", "SV"]
    df = df.dropna(subset=core, how="all")

    # avoid divide-by-zero artifacts
    df.loc[df["AC"] == 0, "AC"] = np.nan
    df.loc[df["PV"] == 0, "PV"] = np.nan

    # derive missing EVM metrics if possible
    if df["CPI"].isna().all() and df["EV"].notna().any():
        df["CPI"] = df["EV"] / df["AC"]
    if df["SPI"].isna().all() and df["EV"].notna().any():
        df["SPI"] = df["EV"] / df["PV"]
    if df["CV"].isna().all():
        df["CV"] = df["EV"] - df["AC"]
    if df["SV"].isna().all():
        df["SV"] = df["EV"] - df["PV"]

    out = df[["period_end", "PV", "EV", "AC", "CPI", "SPI", "CV", "SV"]].copy()
    out.insert(0, "project_id", pid)
    out = out.sort_values("period_end")

    # attach audit metadata
    out.attrs["source_sheet"] = best_sheet
    out.attrs["header_row"] = best_header
    out.attrs["synthetic_dates"] = synthetic_dates
    return out


# --------------------------------------------------
# Risk heuristic (CPI/SPI deviation)
# --------------------------------------------------
def make_risk_from_cpi_spi(panel: pd.DataFrame) -> pd.Series:
    def bad(x):
        return (1 - x).clip(0, 1)

    cpi = panel["CPI"].fillna(1)
    spi = panel["SPI"].fillna(1)
    return (0.55 * bad(cpi) + 0.45 * bad(spi)).clip(0, 1)


# --------------------------------------------------
# MAIN PIPELINE
# --------------------------------------------------
def build_outputs_from_raw():
    cfg = load_thresholds(CONFIG_THRESH)
    tiers = cfg["tiers"]
    evm = cfg["evm"]
    quality = cfg["quality"]

    # thresholds (single source of truth)
    thr_high = float(tiers.get("high", 0.85))
    tau_cpi = float(evm.get("cpi_warn", 0.90))
    tau_spi = float(evm.get("spi_warn", 0.90))

    # quality gates (from YAML)
    min_rows = int(quality.get("min_input_rows", 5))
    min_num_pct = float(quality.get("min_numeric_pct", 60))

    # run metadata (consistent across all outputs for this run)
    run_utc = now_utc_iso()
    run_id = sha256_text(run_utc)[:12]

    scores, alerts, features, inputs, panels = [], [], [], [], []
    audit_rows = []

    hist_path = OUT / "scores_history.csv"
    history = pd.read_csv(hist_path) if hist_path.exists() else pd.DataFrame()

    source_files = sorted(RAW.glob("*.xlsx"), key=lambda p: p.name.lower())

    for f in source_files:
        pid = parse_project_id_from_filename(f.name)
        panel = compute_panel_from_any_sheet(f, pid)

        sheet = panel.attrs.get("source_sheet", None) if hasattr(panel, "attrs") else None
        header_row = panel.attrs.get("header_row", None) if hasattr(panel, "attrs") else None
        synthetic_dates = bool(panel.attrs.get("synthetic_dates", False)) if hasattr(panel, "attrs") else False

        if panel.empty:
            audit_rows.append(
                {
                    "run_utc": run_utc,
                    "run_id": run_id,
                    "file": f.name,
                    "project_id": pid,
                    "sheet": sheet,
                    "header_row": header_row,
                    "synthetic_dates": synthetic_dates,
                    "rows": 0,
                    "numeric_pct": 0.0,
                    "partial_quality_accepted": False,
                }
            )
            scores.append({"project_id": pid, "ml_risk": np.nan})
            alerts.append({"project_id": pid, "alert_type": "NO_PANEL", "message": "No EVM detected"})
            continue

        core_q = ["PV", "EV", "AC", "CPI", "SPI"]
        num_pct = numeric_coverage_pct(panel, core_q)
        valid = panel.dropna(subset=["CPI", "SPI"], how="all").sort_values("period_end")

        partial_quality_accepted = bool(
            pid in PARTIAL_QUALITY_PROJECTS
            and len(panel) >= min_rows
            and not valid.empty
            and num_pct < min_num_pct
        )

        audit_rows.append(
            {
                "run_utc": run_utc,
                "run_id": run_id,
                "file": f.name,
                "project_id": pid,
                "sheet": sheet,
                "header_row": header_row,
                "synthetic_dates": synthetic_dates,
                "rows": int(len(panel)),
                "numeric_pct": float(num_pct),
                "partial_quality_accepted": partial_quality_accepted,
            }
        )

        if (len(panel) < min_rows or num_pct < min_num_pct) and not partial_quality_accepted:
            scores.append({"project_id": pid, "ml_risk": np.nan})
            alerts.append(
                {
                    "project_id": pid,
                    "alert_type": "QUALITY_FAIL",
                    "message": f"Panel quality below threshold (rows={len(panel)}, numeric_pct={num_pct:.1f})",
                }
            )
            continue

        # compute ml_risk (same heuristic logic)
        panel = panel.copy()
        panel["ml_risk"] = make_risk_from_cpi_spi(panel)
        panels.append(panel)

        # pick last valid row
        valid = panel.dropna(subset=["CPI", "SPI"], how="all")
        last = valid.sort_values("period_end").tail(1)

        if last.empty:
            scores.append({"project_id": pid, "ml_risk": np.nan})
            alerts.append({"project_id": pid, "alert_type": "NO_VALID_ROW", "message": "No valid CPI/SPI row"})
            continue

        r = float(last["ml_risk"].iloc[0])
        cpi = float(last["CPI"].iloc[0]) if "CPI" in last.columns else np.nan
        spi = float(last["SPI"].iloc[0]) if "SPI" in last.columns else np.nan

        scores.append(
            {
                "project_id": pid,
                "ml_risk": r,
                "CPI": cpi,
                "SPI": spi,
                "asof_period_end": last["period_end"].iloc[0].strftime("%Y-%m-%d"),
            }
        )

        features.append(
            {
                "project_id": pid,
                "feat_cpi_latest": cpi,
                "feat_spi_latest": spi,
                "feat_risk_latest": r,
            }
        )

        inputs += [
            {"project_id": pid, "wbs": "CPI", "model_input_num": cpi},
            {"project_id": pid, "wbs": "SPI", "model_input_num": spi},
        ]

        # alerts (same logic, config-driven thresholds)
        if r >= thr_high:
            alerts.append({"project_id": pid, "alert_type": "RISK_HIGH", "message": f"Risk ≥ {thr_high:.2f}"})
        if pd.notna(cpi) and cpi < tau_cpi:
            alerts.append({"project_id": pid, "alert_type": "CPI_LOW", "message": f"CPI < {tau_cpi:.2f}"})
        if pd.notna(spi) and spi < tau_spi:
            alerts.append({"project_id": pid, "alert_type": "SPI_LOW", "message": f"SPI < {tau_spi:.2f}"})

        history = pd.concat(
            [
                history,
                pd.DataFrame(
                    [
                        {
                            "refreshed_at_utc": run_utc,
                            "run_id": run_id,
                            "project_id": pid,
                            "ml_risk": r,
                        }
                    ]
                ),
            ],
            ignore_index=True,
        )

    scores_df = pd.DataFrame(scores)
    alerts_df = pd.DataFrame(alerts)
    features_df = pd.DataFrame(features)
    inputs_df = pd.DataFrame(inputs)
    panels_df = pd.concat(panels, ignore_index=True) if panels else pd.DataFrame()
    audit_df = pd.DataFrame(audit_rows)

    write_csv(
        scores_df,
        OUT / "scores.csv",
        columns=["project_id", "ml_risk", "CPI", "SPI", "asof_period_end"],
    )
    write_csv(
        alerts_df,
        OUT / "alerts.csv",
        columns=["project_id", "alert_type", "message"],
    )
    write_csv(
        features_df,
        OUT / "features_wide.csv",
        columns=["project_id", "feat_cpi_latest", "feat_spi_latest", "feat_risk_latest"],
    )
    write_csv(
        inputs_df,
        OUT / "model_inputs_long.csv",
        columns=["project_id", "wbs", "model_input_num"],
    )
    write_csv(
        panels_df,
        OUT / "project_period_panel.csv",
        columns=["project_id", "period_end", "PV", "EV", "AC", "CPI", "SPI", "CV", "SV", "ml_risk"],
    )

    history.to_csv(OUT / "scores_history.csv", index=False)
    audit_df.to_csv(AUDIT_PATH, index=False)

    config_hash = None
    if CONFIG_THRESH.exists():
        try:
            config_hash = sha256_text(CONFIG_THRESH.read_text(encoding="utf-8"))
        except Exception:
            config_hash = None

    meta_obj = {
        "refreshed_at_utc": run_utc,
        "run_id": run_id,
        "thresholds": cfg,
        "inputs": [p.name for p in source_files],
        "scores_rows": len(scores_df),
        "alerts_rows": len(alerts_df),
        "versions": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "pandas": pd.__version__,
            "numpy": np.__version__,
        },
        "config_hash": config_hash,
    }

    (OUT / "refresh_meta.json").write_text(json.dumps(meta_obj, indent=2))

    print("✅ BI outputs regenerated successfully")
    print(f"Run ID: {run_id}")
    print(f"Outputs folder: {OUT.resolve()}")
    print(f"Audit log: {AUDIT_PATH.resolve()}")


if __name__ == "__main__":
    build_outputs_from_raw()


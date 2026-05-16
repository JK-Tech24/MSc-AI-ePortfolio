
import json
from io import BytesIO
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st
import yaml

pio.templates.default = "plotly_white"

BASE_DIR = Path(__file__).parent

DATA_DIR = BASE_DIR / "data/05_bi"
RAW_DIR = BASE_DIR / "data/01_raw"
CONFIG_THRESH = BASE_DIR / "config/thresholds.yaml"

FILES = {
    "scores": DATA_DIR / "scores.csv",
    "alerts": DATA_DIR / "alerts.csv",
    "features": DATA_DIR / "features_wide.csv",
    "inputs_long": DATA_DIR / "model_inputs_long.csv",
    "meta": DATA_DIR / "refresh_meta.json",
    "history": DATA_DIR / "scores_history.csv",
    "panel": DATA_DIR / "project_period_panel.csv",
    "shap_global": DATA_DIR / "shap_global.csv",
    "shap_local": DATA_DIR / "shap_local.csv",
    "audit": DATA_DIR / "audit_log.csv",
}

st.set_page_config(
    page_title="AI-Powered Early Warning Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

TIER_ORDER = ["high", "medium", "low", "none"]
TIER_COLOR = {"high": "#D9485F", "medium": "#F4A261", "low": "#E9C46A", "none": "#54A24B"}
TIER_BADGE_BG = {
    "high": "rgba(217,72,95,0.12)",
    "medium": "rgba(244,162,97,0.14)",
    "low": "rgba(233,196,106,0.18)",
    "none": "rgba(84,162,75,0.14)",
}
TIER_LABEL = {"high": "High", "medium": "Medium", "low": "Low", "none": "None"}


# ------------------ STYLING ------------------
def inject_css():
    st.markdown(
        """
        <style>
        .block-container{
            padding-top: 1.25rem;
            padding-bottom: 2rem;
            max-width: 1500px;
        }
        .main h1, .main h2, .main h3 {
            letter-spacing: -0.01em;
        }
        .report-shell{
            padding: 0.25rem 0 0.5rem 0;
        }
        .hero-card{
            background: linear-gradient(180deg, #FFFFFF 0%, #F8FAFC 100%);
            border: 1px solid rgba(15,23,42,0.08);
            border-radius: 20px;
            padding: 1.05rem 1.15rem;
            box-shadow: 0 8px 30px rgba(15,23,42,0.05);
            margin-bottom: 1rem;
        }
        .section-card{
            background: #FFFFFF;
            border: 1px solid rgba(15,23,42,0.08);
            border-radius: 18px;
            padding: 1rem 1rem 0.4rem 1rem;
            box-shadow: 0 6px 24px rgba(15,23,42,0.04);
            margin-bottom: 1rem;
        }
        .metric-card{
            background: #FFFFFF;
            border: 1px solid rgba(15,23,42,0.08);
            border-radius: 18px;
            padding: 0.95rem 1rem;
            min-height: 120px;
            box-shadow: 0 6px 22px rgba(15,23,42,0.04);
        }
        .metric-label{
            color: #475569;
            font-size: 0.84rem;
            font-weight: 600;
            margin-bottom: 0.35rem;
        }
        .metric-value{
            color: #0F172A;
            font-size: 1.7rem;
            font-weight: 750;
            line-height: 1.1;
            margin-bottom: 0.28rem;
        }
        .metric-sub{
            color: #64748B;
            font-size: 0.84rem;
            line-height: 1.4;
        }
        .pill-row{
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-top: 0.65rem;
        }
        .pill{
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            border: 1px solid rgba(15,23,42,0.08);
            background: rgba(248,250,252,0.95);
            border-radius: 999px;
            padding: 0.36rem 0.72rem;
            color: #334155;
            font-size: 0.82rem;
            font-weight: 600;
        }
        .badge{
            display:inline-block;
            padding: 0.26rem 0.6rem;
            border-radius: 999px;
            font-size: 0.76rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.03em;
        }
        .small-note{
            color:#64748B;
            font-size:0.82rem;
            margin-top:0.25rem;
        }
        div[data-testid="stDownloadButton"] > button {
            border-radius: 10px;
            font-weight: 700;
        }
        @media print {
            .block-container {
                max-width: 100% !important;
                padding-top: 0.6rem !important;
            }
            .hero-card, .section-card, .metric-card {
                box-shadow: none !important;
                break-inside: avoid;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ------------------ HELPERS ------------------
def safe_float(x, default=np.nan):
    try:
        return float(x)
    except Exception:
        return default


def pick_risk_col(df: pd.DataFrame) -> str:
    if df is None or df.empty:
        return "score"
    for c in ["ml_risk", "risk", "score"]:
        if c in df.columns:
            return c
    return "score"


def short_ids(ids, max_ids=4):
    ids = ids or []
    if len(ids) <= max_ids:
        return ", ".join(ids)
    return ", ".join(ids[:max_ids]) + f" (+{len(ids) - max_ids})"


def fmt_num(x, digits=3):
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return "—"
    try:
        return f"{float(x):,.{digits}f}"
    except Exception:
        return "—"


def fmt_pct(x, digits=1):
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return "—"
    try:
        return f"{100 * float(x):,.{digits}f}%"
    except Exception:
        return "—"


def fmt_date(x):
    try:
        return pd.to_datetime(x).strftime("%Y-%m-%d")
    except Exception:
        return "—"


def tier_badge_html(tier: str) -> str:
    t = str(tier).lower() if tier else "none"
    bg = TIER_BADGE_BG.get(t, "rgba(148,163,184,0.18)")
    fg = TIER_COLOR.get(t, "#64748B")
    label = TIER_LABEL.get(t, str(t).title())
    return f'<span class="badge" style="background:{bg};color:{fg};">{label}</span>'


def section_start(title: str, subtitle: str | None = None):
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown(f"### {title}")
    if subtitle:
        st.caption(subtitle)


def section_end():
    st.markdown("</div>", unsafe_allow_html=True)


def metric_card(label: str, value: str, subtitle: str = ""):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-sub">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def load_csv(fp: Path) -> pd.DataFrame:
    if not fp.exists() or fp.stat().st_size == 0:
        return pd.DataFrame()
    try:
        return pd.read_csv(fp)
    except Exception:
        return pd.DataFrame()


def load_meta(fp: Path) -> dict:
    if not fp.exists() or fp.stat().st_size == 0:
        return {}
    try:
        return json.loads(fp.read_text(encoding="utf-8"))
    except Exception:
        return {}


def load_thresholds(fp: Path) -> dict:
    defaults = {
        "tiers": {"high": 0.85, "medium": 0.70, "low": 0.50},
        "evm": {"cpi_warn": 0.90, "spi_warn": 0.90},
    }
    if not fp.exists():
        return defaults
    try:
        cfg = yaml.safe_load(fp.read_text(encoding="utf-8")) or {}
        cfg.setdefault("tiers", defaults["tiers"])
        cfg.setdefault("evm", defaults["evm"])
        return cfg
    except Exception:
        return defaults


def tier_from_score(score: float, tiers: dict) -> str:
    if score is None or (isinstance(score, float) and np.isnan(score)):
        return "none"
    if score >= tiers.get("high", 0.85):
        return "high"
    if score >= tiers.get("medium", 0.70):
        return "medium"
    if score >= tiers.get("low", 0.50):
        return "low"
    return "none"


def tier_rank(t: str) -> int:
    return {"high": 0, "medium": 1, "low": 2, "none": 3}.get(str(t).lower(), 9)


def add_threshold_lines(fig, thr_high, thr_med, thr_low, title="Thresholds"):
    for thr, name in [(thr_high, "High"), (thr_med, "Medium"), (thr_low, "Low")]:
        if thr is not None and not (isinstance(thr, float) and np.isnan(thr)):
            fig.add_hline(
                y=float(thr),
                line_dash="dot",
                line_color="#64748B",
                annotation_text=f"{name} = {float(thr):.2f}",
                annotation_position="top left",
            )
    fig.update_layout(legend_title_text=title)
    return fig


def add_tier_bands(fig, thr_high, thr_med, thr_low):
    bands = []
    bands.append((0.0, float(thr_low) if pd.notna(thr_low) else 0.50, "none"))
    if pd.notna(thr_low) and pd.notna(thr_med):
        bands.append((float(thr_low), float(thr_med), "low"))
    if pd.notna(thr_med) and pd.notna(thr_high):
        bands.append((float(thr_med), float(thr_high), "medium"))
    if pd.notna(thr_high):
        bands.append((float(thr_high), 1.0, "high"))

    for y0, y1, t in bands:
        fig.add_hrect(
            y0=y0,
            y1=y1,
            fillcolor=TIER_COLOR.get(t, "#cccccc"),
            opacity=0.07,
            line_width=0,
            layer="below",
        )
    return fig


def finalise_fig(fig, height=360, legend_orientation="h", legend_y=1.08):
    fig.update_layout(
        height=height,
        margin=dict(l=16, r=16, t=36, b=16),
        paper_bgcolor="white",
        plot_bgcolor="white",
        legend=dict(
            orientation=legend_orientation,
            yanchor="bottom",
            y=legend_y,
            xanchor="left",
            x=0,
            title_text=fig.layout.legend.title.text if fig.layout.legend and fig.layout.legend.title else "",
        ),
        font=dict(size=13, color="#0F172A"),
    )
    fig.update_xaxes(showgrid=False, zeroline=False, title_font=dict(size=13), tickfont=dict(size=12))
    fig.update_yaxes(gridcolor="rgba(148,163,184,0.25)", zeroline=False, title_font=dict(size=13), tickfont=dict(size=12))
    return fig


def risk_gauge(score: float, thr_low: float, thr_med: float, thr_high: float, title="Current risk (0-1)"):
    if score is None or (isinstance(score, float) and np.isnan(score)):
        score = 0.0

    thr_low_ = float(thr_low) if pd.notna(thr_low) else 0.50
    thr_med_ = float(thr_med) if pd.notna(thr_med) else 0.70
    thr_high_ = float(thr_high) if pd.notna(thr_high) else 0.85

    steps = [
        {"range": [0.0, thr_low_], "color": TIER_COLOR["none"]},
        {"range": [thr_low_, thr_med_], "color": TIER_COLOR["low"]},
        {"range": [thr_med_, thr_high_], "color": TIER_COLOR["medium"]},
        {"range": [thr_high_, 1.0], "color": TIER_COLOR["high"]},
    ]

    fig = go.Figure()
    fig.add_trace(
        go.Indicator(
            mode="gauge+number",
            value=float(score),
            number={"valueformat": ".3f"},
            title={"text": title, "font": {"size": 16}},
            gauge={
                "axis": {"range": [0, 1], "tickwidth": 1},
                "bar": {"color": "#0F172A", "thickness": 0.22},
                "steps": steps,
                "threshold": {"line": {"width": 4, "color": "#0F172A"}, "value": float(score)},
            },
        )
    )

    legend_items = [
        ("high", f"high (≥ {thr_high_:.2f})"),
        ("medium", f"medium (≥ {thr_med_:.2f})"),
        ("low", f"low (≥ {thr_low_:.2f})"),
        ("none", f"none (< {thr_low_:.2f})"),
    ]
    for t, label in legend_items:
        fig.add_trace(
            go.Scatter(
                x=[0],
                y=[0],
                mode="markers",
                marker=dict(size=10, color=TIER_COLOR[t]),
                name=label,
                hoverinfo="skip",
                visible="legendonly",
                showlegend=True,
            )
        )

    fig.update_layout(
        height=310,
        margin=dict(l=10, r=10, t=50, b=10),
        legend_title_text="tier",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        paper_bgcolor="white",
        plot_bgcolor="white",
    )
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    return fig


def risk_delta_table(history: pd.DataFrame) -> pd.DataFrame:
    if history.empty or "project_id" not in history.columns:
        return pd.DataFrame()

    rcol = pick_risk_col(history)
    if rcol not in history.columns or "refreshed_at_utc" not in history.columns:
        return pd.DataFrame()

    h = history.copy()
    h["project_id"] = h["project_id"].astype(str)
    h[rcol] = pd.to_numeric(h[rcol], errors="coerce")
    h["refreshed_at_utc"] = pd.to_datetime(h["refreshed_at_utc"], errors="coerce")
    h = h.dropna(subset=["refreshed_at_utc", rcol])

    if h.empty:
        return pd.DataFrame()

    last2 = h.sort_values("refreshed_at_utc").groupby("project_id", as_index=False).tail(2)

    rows = []
    for pid, g in last2.groupby("project_id"):
        g = g.sort_values("refreshed_at_utc")
        if len(g) < 2:
            continue
        delta = float(g[rcol].iloc[-1] - g[rcol].iloc[-2])
        rows.append(
            {
                "project_id": pid,
                "risk_col": rcol,
                "prev": float(g[rcol].iloc[-2]),
                "latest": float(g[rcol].iloc[-1]),
                "risk_delta": delta,
                "prev_run": g["refreshed_at_utc"].iloc[-2],
                "latest_run": g["refreshed_at_utc"].iloc[-1],
            }
        )

    out = pd.DataFrame(rows)
    return out.sort_values("risk_delta", ascending=False) if not out.empty else out


def tier_trend_over_time(history: pd.DataFrame, tiers_cfg: dict, all_project_ids=None) -> pd.DataFrame:
    if history.empty or "project_id" not in history.columns or "refreshed_at_utc" not in history.columns:
        return pd.DataFrame()

    rcol = pick_risk_col(history)
    if rcol not in history.columns:
        return pd.DataFrame()

    h = history.copy()
    h["refreshed_at_utc"] = pd.to_datetime(h["refreshed_at_utc"], errors="coerce")
    h[rcol] = pd.to_numeric(h[rcol], errors="coerce")
    h["project_id"] = h["project_id"].astype(str)
    h = h.dropna(subset=["refreshed_at_utc", rcol])

    if h.empty:
        return pd.DataFrame()

    h["run_day"] = h["refreshed_at_utc"].dt.floor("D")
    h = h.sort_values("refreshed_at_utc").groupby(["run_day", "project_id"], as_index=False).tail(1)
    h["tier"] = h[rcol].apply(lambda x: tier_from_score(x, tiers_cfg))

    if all_project_ids is None:
        all_project_ids = sorted(h["project_id"].dropna().astype(str).unique().tolist())
    else:
        all_project_ids = sorted([str(x) for x in all_project_ids])

    days = sorted(h["run_day"].dropna().unique().tolist())
    if not days:
        return pd.DataFrame()

    base = pd.MultiIndex.from_product([days, all_project_ids], names=["run_day", "project_id"]).to_frame(index=False)
    hx = base.merge(h[["run_day", "project_id", "tier"]], on=["run_day", "project_id"], how="left")
    hx["tier"] = hx["tier"].fillna("none")

    g = (
        hx.groupby(["run_day", "tier"], as_index=False)
        .agg(projects=("project_id", "nunique"), project_ids=("project_id", lambda s: sorted(set(s.tolist()))))
    )
    g["project_ids_full"] = g["project_ids"].apply(lambda ids: ", ".join(ids) if isinstance(ids, list) else "")
    g = g.drop(columns=["project_ids"])

    rows = []
    for d in days:
        for t in TIER_ORDER:
            v = g[(g["run_day"] == d) & (g["tier"] == t)]
            if not v.empty:
                rows.append(
                    {
                        "run_day": d,
                        "tier": t,
                        "projects": int(v["projects"].iloc[0]),
                        "project_ids_full": str(v["project_ids_full"].iloc[0]),
                    }
                )
            else:
                rows.append({"run_day": d, "tier": t, "projects": 0, "project_ids_full": ""})
    return pd.DataFrame(rows)


def zscore_drivers(features_df: pd.DataFrame, pid: str) -> pd.DataFrame:
    if features_df.empty or "project_id" not in features_df.columns:
        return pd.DataFrame()

    df = features_df.copy()
    df["project_id"] = df["project_id"].astype(str)
    numeric_cols = [c for c in df.columns if c != "project_id"]

    for c in numeric_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    zdf = df[numeric_cols].apply(lambda col: (col - col.mean()) / (col.std(ddof=0) if col.std(ddof=0) else 1))
    zdf.insert(0, "project_id", df["project_id"])

    row = zdf[zdf["project_id"] == str(pid)]
    if row.empty:
        return pd.DataFrame()

    long = row.drop(columns=["project_id"]).melt(var_name="feature", value_name="z")
    long["abs_z"] = long["z"].abs()
    return long.sort_values("abs_z", ascending=False)


def risk_trajectory_by_period(p: pd.DataFrame, tiers_cfg: dict, thr_high, thr_med, thr_low):
    if p is None or p.empty or "period_end" not in p.columns:
        return None

    rcol = pick_risk_col(p)
    d = p.copy()
    d["period_end"] = pd.to_datetime(d["period_end"], errors="coerce")
    d[rcol] = pd.to_numeric(d[rcol], errors="coerce")

    if "CPI" in d.columns:
        d["CPI"] = pd.to_numeric(d["CPI"], errors="coerce")
    if "SPI" in d.columns:
        d["SPI"] = pd.to_numeric(d["SPI"], errors="coerce")

    d = d.dropna(subset=["period_end", rcol]).sort_values("period_end")
    if d.empty:
        return None

    d["tier"] = d[rcol].apply(lambda x: tier_from_score(x, tiers_cfg))
    d["risk_delta"] = d[rcol].diff()

    cpi_s = d["CPI"] if "CPI" in d.columns else pd.Series([np.nan] * len(d), index=d.index)
    spi_s = d["SPI"] if "SPI" in d.columns else pd.Series([np.nan] * len(d), index=d.index)

    custom = np.column_stack([d["tier"].astype(str).values, cpi_s.values, spi_s.values, d["risk_delta"].values])
    marker_colors = [TIER_COLOR.get(t, "#999999") for t in d["tier"]]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=d["period_end"],
            y=d[rcol],
            mode="lines+markers",
            name="risk",
            line=dict(width=3, color="#1D4ED8"),
            marker=dict(size=9, color=marker_colors, line=dict(color="white", width=1)),
            customdata=custom,
            hovertemplate=(
                "period: %{x|%Y-%m-%d}<br>"
                "risk: %{y:.3f}<br>"
                "tier: %{customdata[0]}<br>"
                "CPI: %{customdata[1]:.3f}<br>"
                "SPI: %{customdata[2]:.3f}<br>"
                "Δrisk: %{customdata[3]:+.3f}<extra></extra>"
            ),
        )
    )

    for t in TIER_ORDER:
        fig.add_trace(
            go.Scatter(
                x=[d["period_end"].iloc[0]],
                y=[d[rcol].iloc[0]],
                mode="markers",
                name=t,
                marker=dict(size=10, color=TIER_COLOR.get(t, "#999999")),
                hoverinfo="skip",
                visible="legendonly",
                showlegend=True,
            )
        )

    fig = add_threshold_lines(fig, thr_high, thr_med, thr_low, title="tier")
    fig = add_tier_bands(fig, thr_high, thr_med, thr_low)
    fig.update_layout(xaxis_title="Reporting period", yaxis_title="Risk (0-1)")
    return finalise_fig(fig, height=390)


def bubble_cpi_spi_risk_by_period(p: pd.DataFrame, tiers_cfg: dict, tau_cpi: float, tau_spi: float):
    if p is None or p.empty:
        return None

    rcol = pick_risk_col(p)
    d = p.copy()

    if "period_end" in d.columns:
        d["period_end"] = pd.to_datetime(d["period_end"], errors="coerce")

    for c in ["CPI", "SPI", rcol]:
        if c in d.columns:
            d[c] = pd.to_numeric(d[c], errors="coerce")

    need = [c for c in ["CPI", "SPI", rcol] if c in d.columns]
    d = d.dropna(subset=need)
    if d.empty or "CPI" not in d.columns or "SPI" not in d.columns:
        return None

    d["tier"] = d[rcol].apply(lambda x: tier_from_score(x, tiers_cfg))
    d = d.sort_values("period_end") if "period_end" in d.columns else d

    fig = px.scatter(
        d,
        x="CPI",
        y="SPI",
        size=rcol,
        color="tier",
        color_discrete_map=TIER_COLOR,
        hover_data=["period_end", rcol, "CPI", "SPI"],
        size_max=55,
    )
    fig.add_vline(x=tau_cpi, line_dash="dot", line_color="#64748B", annotation_text="τ_CPI")
    fig.add_hline(y=tau_spi, line_dash="dot", line_color="#64748B", annotation_text="τ_SPI")
    fig.update_layout(xaxis_title="CPI", yaxis_title="SPI")
    return finalise_fig(fig, height=390)


def current_portfolio_snapshot(portfolio_df: pd.DataFrame, alerts_df: pd.DataFrame, deltas_df: pd.DataFrame) -> dict:
    if portfolio_df.empty:
        return {
            "projects": 0,
            "high_count": 0,
            "medium_count": 0,
            "low_count": 0,
            "none_count": 0,
            "top_project": "—",
            "top_risk": np.nan,
            "alerts": 0,
            "largest_increase": "—",
            "largest_delta": np.nan,
        }

    tier_counts = portfolio_df["tier"].fillna("none").value_counts().to_dict()
    top_df = portfolio_df.dropna(subset=["risk"]).sort_values("risk", ascending=False)
    top_project = str(top_df["project_id"].iloc[0]) if not top_df.empty else "—"
    top_risk = float(top_df["risk"].iloc[0]) if not top_df.empty else np.nan

    mover = deltas_df.sort_values("risk_delta", ascending=False).head(1) if not deltas_df.empty else pd.DataFrame()
    return {
        "projects": int(portfolio_df["project_id"].nunique()),
        "high_count": int(tier_counts.get("high", 0)),
        "medium_count": int(tier_counts.get("medium", 0)),
        "low_count": int(tier_counts.get("low", 0)),
        "none_count": int(tier_counts.get("none", 0)),
        "top_project": top_project,
        "top_risk": top_risk,
        "alerts": int(len(alerts_df)) if alerts_df is not None and not alerts_df.empty else 0,
        "largest_increase": str(mover["project_id"].iloc[0]) if not mover.empty else "—",
        "largest_delta": float(mover["risk_delta"].iloc[0]) if not mover.empty else np.nan,
    }


def enrich_portfolio_table(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    out = df.copy()
    out["tier"] = out["tier"].fillna("none")
    if "risk" in out.columns:
        out["risk"] = pd.to_numeric(out["risk"], errors="coerce")
    for c in ["CPI", "SPI", "PV", "EV", "AC", "CV", "SV"]:
        if c in out.columns:
            out[c] = pd.to_numeric(out[c], errors="coerce")
    return out


def alert_summary_table(alerts_df: pd.DataFrame) -> pd.DataFrame:
    if alerts_df.empty or "alert_type" not in alerts_df.columns:
        return pd.DataFrame()
    out = alerts_df.groupby("alert_type", as_index=False).agg(alerts=("alert_type", "size"))
    return out.sort_values(["alerts", "alert_type"], ascending=[False, True])


@st.cache_data
def build_excel_report(scores, alerts, features, inputs_long, history, panel, shap_global, shap_local, audit):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        if not scores.empty:
            scores.to_excel(writer, sheet_name="Scores", index=False)
        if not alerts.empty:
            alerts.to_excel(writer, sheet_name="Alerts", index=False)
        if not features.empty:
            features.to_excel(writer, sheet_name="Features", index=False)
        if not inputs_long.empty:
            inputs_long.to_excel(writer, sheet_name="Inputs_long", index=False)
        if not history.empty:
            history.to_excel(writer, sheet_name="History", index=False)
        if not panel.empty:
            panel.to_excel(writer, sheet_name="Panel", index=False)
        if shap_global is not None and not shap_global.empty:
            shap_global.to_excel(writer, sheet_name="SHAP_global", index=False)
        if shap_local is not None and not shap_local.empty:
            shap_local.to_excel(writer, sheet_name="SHAP_local", index=False)
        if audit is not None and not audit.empty:
            audit.to_excel(writer, sheet_name="Audit", index=False)
    return output.getvalue()


# ------------------ LOAD DATA ------------------
inject_css()

scores = load_csv(FILES["scores"])
alerts = load_csv(FILES["alerts"])
features = load_csv(FILES["features"])
inputs_long = load_csv(FILES["inputs_long"])
meta = load_meta(FILES["meta"])
history = load_csv(FILES["history"])
panel = load_csv(FILES["panel"])
shap_global = load_csv(FILES["shap_global"])
shap_local = load_csv(FILES["shap_local"])
audit = load_csv(FILES["audit"])

cfg = load_thresholds(CONFIG_THRESH)
tiers_cfg = cfg.get("tiers", {})
evm_cfg = cfg.get("evm", {})

thr_high = safe_float(tiers_cfg.get("high", 0.85))
thr_med = safe_float(tiers_cfg.get("medium", 0.70))
thr_low = safe_float(tiers_cfg.get("low", 0.50))

tau_cpi_default = safe_float(evm_cfg.get("cpi_warn", 0.90))
tau_spi_default = safe_float(evm_cfg.get("spi_warn", 0.90))

if not history.empty and "refreshed_at_utc" in history.columns:
    history["refreshed_at_utc"] = pd.to_datetime(history["refreshed_at_utc"], errors="coerce", utc=True).dt.tz_convert(None)

if not panel.empty and "period_end" in panel.columns:
    panel["period_end"] = pd.to_datetime(panel["period_end"], errors="coerce")
    for c in ["PV", "EV", "AC", "CPI", "SPI", "CV", "SV", "ml_risk", "risk", "score"]:
        if c in panel.columns:
            panel[c] = pd.to_numeric(panel[c], errors="coerce")

project_ids = []
for df in [scores, panel, features, inputs_long, alerts, history]:
    if not df.empty and "project_id" in df.columns:
        vals = df["project_id"].dropna().astype(str).unique().tolist()
        project_ids = sorted(set(project_ids).union(vals))


# ------------------ SIDEBAR ------------------
with st.sidebar:
    st.markdown("## Dashboard controls")
    view = st.radio("View", ["Portfolio", "Project detail"], index=0)
    project = st.selectbox("Project", project_ids, index=0) if project_ids else st.text_input("Project ID", value="P001")
    top_n = st.slider("Top N projects", 5, 50, 15)

    st.markdown("## Threshold controls")
    tau_ml = st.slider("ML risk threshold (τ_ML)", 0.05, 0.99, float(thr_med), 0.01)
    tau_cpi = st.slider("CPI warn if CPI < τ_CPI", 0.50, 1.10, float(tau_cpi_default), 0.01)
    tau_spi = st.slider("SPI warn if SPI < τ_SPI", 0.50, 1.10, float(tau_spi_default), 0.01)

    st.markdown("## Export")
    try:
        xlsx_bytes_sidebar = build_excel_report(scores, alerts, features, inputs_long, history, panel, shap_global, shap_local, audit)
        st.download_button(
            "⬇ Download Excel report",
            data=xlsx_bytes_sidebar,
            file_name="ews_full_dashboard_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )
    except Exception as e:
        st.warning(f"Export failed: {e}")

    st.markdown("## Source folders")
    st.caption("Raw EDM folder (.xlsx files)")
    st.code(str(RAW_DIR.resolve()) if RAW_DIR.exists() else str(RAW_DIR))

    st.markdown("## Responsible AI")
    st.caption("Decision support only. Validate alerts using CPI/SPI, period trends, and project context.")


# ------------------ HEADER ------------------
st.markdown('<div class="report-shell">', unsafe_allow_html=True)
st.markdown(
    """
    <div class="hero-card">
        <div style="font-size:2rem;font-weight:800;color:#0F172A;line-height:1.1;">AI-Powered Early Warning Dashboard</div>
        <div style="margin-top:0.35rem;color:#475569;font-size:0.98rem;">
            Portfolio triage, project validation, and explainability support with a cleaner report-style layout for screen and PDF output.
        </div>
    """,
    unsafe_allow_html=True,
)

pill_bits = [
    f"<span class='pill'>Last refresh: {meta.get('refreshed_at_utc', '—')}</span>",
    f"<span class='pill'>Projects: {len(project_ids) if project_ids else 0}</span>",
    f"<span class='pill'>Scores rows: {int(meta.get('scores_rows', 0)) if meta else (len(scores) if not scores.empty else 0)}</span>",
    f"<span class='pill'>Alerts rows: {int(meta.get('alerts_rows', 0)) if meta else (len(alerts) if not alerts.empty else 0)}</span>",
]
st.markdown(f"<div class='pill-row'>{''.join(pill_bits)}</div></div>", unsafe_allow_html=True)

with st.expander("Threshold rationale and interpretation"):
    st.markdown(
        f"""
- **High (≥ {thr_high:.2f})**: strongest current signal and highest review priority.
- **Medium (≥ {thr_med:.2f})**: elevated signal requiring close monitoring and early intervention.
- **Low (≥ {thr_low:.2f})**: weaker deviation signal that still merits observation.
- **None (< {thr_low:.2f})**: no current tier escalation based on the configured thresholds.

These thresholds are read from the configuration and the dashboard only visualises them.
"""
    )


# ------------------ PORTFOLIO BUILD ------------------
portfolio = pd.DataFrame({"project_id": project_ids}) if project_ids else pd.DataFrame(columns=["project_id"])
risk_col_scores = pick_risk_col(scores) if not scores.empty else "score"

if not scores.empty and "project_id" in scores.columns and risk_col_scores in scores.columns:
    s = scores.copy()
    s["project_id"] = s["project_id"].astype(str)
    s[risk_col_scores] = pd.to_numeric(s[risk_col_scores], errors="coerce")
    s["risk"] = s[risk_col_scores]
    s["tier"] = s["risk"].apply(lambda x: tier_from_score(x, tiers_cfg))
    keep_cols = ["project_id", "risk", "tier"]
    for extra in ["CPI", "SPI", "PV", "EV", "AC", "CV", "SV", "asof_period_end"]:
        if extra in s.columns:
            keep_cols.append(extra)
    portfolio = portfolio.merge(s[keep_cols], on="project_id", how="left")
else:
    portfolio["risk"] = np.nan
    portfolio["tier"] = "none"

portfolio["tier_rank"] = portfolio["tier"].apply(tier_rank)
portfolio_sorted = portfolio.sort_values(["tier_rank", "risk"], ascending=[True, False]).drop(columns=["tier_rank"])
portfolio_sorted = enrich_portfolio_table(portfolio_sorted)

deltas = risk_delta_table(history)
snapshot = current_portfolio_snapshot(portfolio_sorted, alerts, deltas)
alert_summary = alert_summary_table(alerts)


# ================== VIEW: PORTFOLIO ==================
if view == "Portfolio":
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        metric_card("Projects in portfolio", f"{snapshot['projects']}", "Current set available to the dashboard")
    with m2:
        metric_card("High-tier projects", f"{snapshot['high_count']}", f"Top risk project: {snapshot['top_project']}")
    with m3:
        metric_card("Alerts raised", f"{snapshot['alerts']}", f"Largest current mover: {snapshot['largest_increase']}")
    with m4:
        tier_mix = f"H {snapshot['high_count']} · M {snapshot['medium_count']} · L {snapshot['low_count']} · N {snapshot['none_count']}"
        metric_card("Tier distribution", tier_mix, "Current portfolio tier mix")

    summary_text = (
        f"Current highest-risk project is **{snapshot['top_project']}** with risk **{fmt_num(snapshot['top_risk'])}**. "
        f"The largest current increase versus the previous run is **{snapshot['largest_increase']}** at **{fmt_num(snapshot['largest_delta'])}** "
        f"(when at least two runs exist)."
    )
    st.caption(summary_text)

    left, right = st.columns([1.03, 0.97])

    with left:
        section_start("Portfolio overview", "Tier composition using current scores and the configured thresholds.")
        if not portfolio_sorted.empty and "tier" in portfolio_sorted.columns:
            tmp = portfolio_sorted.copy()
            tmp["tier"] = tmp["tier"].fillna("none")
            tier_counts = tmp["tier"].value_counts().reindex(TIER_ORDER).fillna(0).astype(int)
            tier_to_ids = (
                tmp.groupby("tier")["project_id"]
                .apply(lambda s: sorted(s.dropna().astype(str).unique().tolist()))
                .to_dict()
            )

            donut_rows = []
            for t in TIER_ORDER:
                ids = tier_to_ids.get(t, [])
                donut_rows.append(
                    {
                        "tier": t,
                        "count": int(tier_counts.loc[t]),
                        "project_ids_full": ", ".join(ids),
                        "tier_label": f"{TIER_LABEL[t]} • {short_ids(ids)}" if ids else TIER_LABEL[t],
                    }
                )
            donut_df = pd.DataFrame(donut_rows)

            fig_donut = px.pie(
                donut_df,
                names="tier_label",
                values="count",
                hole=0.58,
                color="tier",
                color_discrete_map=TIER_COLOR,
                hover_data=["project_ids_full"],
            )
            fig_donut.update_traces(textposition="inside", textinfo="percent+label")
            st.plotly_chart(finalise_fig(fig_donut, height=360, legend_y=1.12), use_container_width=True)

            tier_cols = st.columns(4)
            for col, t in zip(tier_cols, TIER_ORDER):
                with col:
                    ids = tier_to_ids.get(t, [])
                    metric_card(f"{TIER_LABEL[t]} tier", str(int(tier_counts.loc[t])), short_ids(ids) if ids else "No projects")
        else:
            st.info("No portfolio scores available.")
        section_end()

    with right:
        section_start("Top risk projects", "Current project ordering by risk without changing any risk values or tier logic.")
        top_df = portfolio_sorted.dropna(subset=["risk"]).sort_values("risk", ascending=False).head(int(top_n))
        if top_df.empty:
            st.info("No risk values available yet.")
        else:
            fig_bar = px.bar(
                top_df,
                x="project_id",
                y="risk",
                color="tier",
                text=top_df["risk"].map(lambda x: f"{x:.3f}"),
                color_discrete_map=TIER_COLOR,
                hover_data=["project_id", "risk", "CPI", "SPI", "asof_period_end"],
            )
            fig_bar.update_traces(textposition="outside", cliponaxis=False)
            fig_bar = add_threshold_lines(fig_bar, thr_high, thr_med, thr_low, title="Tier thresholds")
            fig_bar = add_tier_bands(fig_bar, thr_high, thr_med, thr_low)
            fig_bar.update_layout(xaxis_title="", yaxis_title="Risk (0-1)", showlegend=True)
            st.plotly_chart(finalise_fig(fig_bar, height=420, legend_y=1.12), use_container_width=True)
        section_end()

    left2, right2 = st.columns([1.03, 0.97])

    with left2:
        section_start("Bubble chart: CPI, SPI, and risk", "Latest per-project position using the same CPI, SPI, and risk values already produced.")
        if ("CPI" in portfolio_sorted.columns) and ("SPI" in portfolio_sorted.columns):
            qdf = portfolio_sorted.copy()
            qdf["CPI"] = pd.to_numeric(qdf["CPI"], errors="coerce")
            qdf["SPI"] = pd.to_numeric(qdf["SPI"], errors="coerce")
            qdf = qdf.dropna(subset=["CPI", "SPI"])
            if qdf.empty:
                st.info("No CPI/SPI values available.")
            else:
                fig_q = px.scatter(
                    qdf,
                    x="CPI",
                    y="SPI",
                    color="tier",
                    color_discrete_map=TIER_COLOR,
                    hover_data=["project_id", "risk", "CPI", "SPI"],
                    size="risk",
                    size_max=58,
                    text="project_id",
                )
                fig_q.update_traces(textposition="top center")
                fig_q.add_vline(x=tau_cpi, line_dash="dot", line_color="#64748B", annotation_text="τ_CPI")
                fig_q.add_hline(y=tau_spi, line_dash="dot", line_color="#64748B", annotation_text="τ_SPI")
                fig_q.update_layout(xaxis_title="CPI", yaxis_title="SPI")
                st.plotly_chart(finalise_fig(fig_q, height=430, legend_y=1.14), use_container_width=True)
                st.caption("Projects in the lower-left area indicate weaker CPI and SPI at the same time; bubble size remains the same current risk score.")
        else:
            st.info("CPI/SPI not available in scores.csv.")
        section_end()

    with right2:
        section_start("Change since previous run", "Uses the existing history file only when at least two runs exist.")
        if deltas.empty:
            st.info("Not enough history yet (need at least two runs).")
        else:
            mover_cards = st.columns(2)
            with mover_cards[0]:
                biggest_up = deltas.sort_values("risk_delta", ascending=False).head(1)
                value = biggest_up["project_id"].iloc[0] if not biggest_up.empty else "—"
                subtitle = f"Δrisk {fmt_num(biggest_up['risk_delta'].iloc[0])}" if not biggest_up.empty else "No change data"
                metric_card("Biggest increase", value, subtitle)
            with mover_cards[1]:
                biggest_down = deltas.sort_values("risk_delta", ascending=True).head(1)
                value = biggest_down["project_id"].iloc[0] if not biggest_down.empty else "—"
                subtitle = f"Δrisk {fmt_num(biggest_down['risk_delta'].iloc[0])}" if not biggest_down.empty else "No change data"
                metric_card("Biggest decrease", value, subtitle)

            figd = px.bar(
                deltas.head(15),
                x="project_id",
                y="risk_delta",
                text=deltas.head(15)["risk_delta"].map(lambda x: f"{x:+.3f}"),
                hover_data=["prev", "latest", "prev_run", "latest_run"],
            )
            figd.update_traces(textposition="outside", cliponaxis=False)
            figd.update_layout(xaxis_title="", yaxis_title="Δ risk (latest - previous)")
            st.plotly_chart(finalise_fig(figd, height=390, legend_y=1.08), use_container_width=True)
        section_end()

    section_start("Tier trend over time", "Daily tier membership based on the existing scores history and current threshold definitions.")
    trend = tier_trend_over_time(history, tiers_cfg, project_ids)
    if trend.empty:
        st.info("Tier trend needs scores_history.csv with at least one run.")
    else:
        latest_day = trend["run_day"].max()
        tier_to_ids_latest = {}
        for t in TIER_ORDER:
            row = trend[(trend["run_day"] == latest_day) & (trend["tier"] == t)]
            tier_to_ids_latest[t] = str(row["project_ids_full"].iloc[0]) if not row.empty else ""

        tier_label_map = {}
        for t in TIER_ORDER:
            ids_str = tier_to_ids_latest.get(t, "")
            ids_list = [x.strip() for x in ids_str.split(",") if x.strip()] if ids_str else []
            tier_label_map[t] = f"{TIER_LABEL[t]} • {short_ids(ids_list)}" if ids_list else f"{TIER_LABEL[t]} • -"

        trend["tier_label"] = trend["tier"].map(tier_label_map)
        color_map = {tier_label_map[t]: TIER_COLOR[t] for t in TIER_ORDER}
        cat_order = [tier_label_map[t] for t in TIER_ORDER]

        if trend["run_day"].nunique() == 1:
            trend_plot = trend.copy()
            trend_plot["run_day_label"] = trend_plot["run_day"].dt.strftime("%Y-%m-%d")
            fig_tr = px.bar(
                trend_plot,
                x="run_day_label",
                y="projects",
                color="tier_label",
                category_orders={"tier_label": cat_order},
                color_discrete_map=color_map,
                hover_data=["project_ids_full"],
            )
            fig_tr.update_layout(xaxis_title="Run day", yaxis_title="Projects", barmode="stack", legend_title_text="Tier")
        else:
            fig_tr = px.area(
                trend,
                x="run_day",
                y="projects",
                color="tier_label",
                category_orders={"tier_label": cat_order},
                color_discrete_map=color_map,
                hover_data=["project_ids_full"],
            )
            fig_tr.update_layout(xaxis_title="Run day", yaxis_title="Projects", legend_title_text="Tier")

        st.plotly_chart(finalise_fig(fig_tr, height=380, legend_y=1.12), use_container_width=True)

        membership_line = " | ".join(
            [f"{TIER_LABEL[t]}: {tier_to_ids_latest.get(t, '') if str(tier_to_ids_latest.get(t, '')).strip() else '-'}" for t in TIER_ORDER]
        )
        st.caption(f"Latest visible membership on {pd.to_datetime(latest_day).date()}: {membership_line}")
    section_end()

    lower_left, lower_right = st.columns([1.08, 0.92])

    with lower_left:
        section_start("Portfolio table", "Triage view with the same portfolio values, reformatted for easier reading.")
        table_df = portfolio_sorted.copy()
        if "tier" in table_df.columns:
            table_df["tier_display"] = table_df["tier"].map(lambda t: TIER_LABEL.get(str(t).lower(), str(t).title()))
        show_cols = [c for c in ["project_id", "tier_display", "risk", "CPI", "SPI", "asof_period_end"] if c in table_df.columns]
        st.dataframe(
            table_df[show_cols].rename(columns={"tier_display": "tier"}),
            use_container_width=True,
            hide_index=True,
            column_config={
                "risk": st.column_config.NumberColumn("risk", format="%.3f"),
                "CPI": st.column_config.NumberColumn("CPI", format="%.3f"),
                "SPI": st.column_config.NumberColumn("SPI", format="%.3f"),
                "asof_period_end": st.column_config.TextColumn("asof_period_end"),
            },
        )
        section_end()

    with lower_right:
        section_start("Alert summary", "Current alert load using the same generated alert table.")
        if alerts.empty:
            st.info("No alerts table available.")
        else:
            if not alert_summary.empty:
                fig_alert = px.bar(alert_summary, x="alert_type", y="alerts", text="alerts")
                fig_alert.update_traces(textposition="outside", cliponaxis=False)
                fig_alert.update_layout(xaxis_title="", yaxis_title="Count")
                st.plotly_chart(finalise_fig(fig_alert, height=310, legend_y=1.08), use_container_width=True)

            latest_alerts = alerts.copy()
            st.dataframe(latest_alerts, use_container_width=True, hide_index=True)
        section_end()

    if audit is not None and not audit.empty:
        with st.expander("Data quality and extraction audit"):
            audit_view = audit.copy()
            st.dataframe(audit_view, use_container_width=True, hide_index=True)

# ================== VIEW: PROJECT DETAIL ==================
else:
    st.caption("Project detail view keeps the same values and rules, but presents them in a cleaner report-style layout.")

    latest_risk = np.nan
    latest_tier = "none"

    if not scores.empty and "project_id" in scores.columns and risk_col_scores in scores.columns:
        srow = scores[scores["project_id"].astype(str) == str(project)].copy()
        if not srow.empty:
            latest_risk = safe_float(srow[risk_col_scores].iloc[0], np.nan)
            latest_tier = tier_from_score(latest_risk, tiers_cfg)

    p_panel = pd.DataFrame()
    if not panel.empty and "project_id" in panel.columns:
        p_panel = panel[panel["project_id"].astype(str) == str(project)].copy()
        if not p_panel.empty and "period_end" in p_panel.columns:
            p_panel["period_end"] = pd.to_datetime(p_panel["period_end"], errors="coerce")
            p_panel = p_panel.dropna(subset=["period_end"]).sort_values("period_end")

    top_inputs = pd.DataFrame()
    if not inputs_long.empty and "project_id" in inputs_long.columns:
        top_inputs = inputs_long[inputs_long["project_id"].astype(str) == str(project)].copy()
        if not top_inputs.empty:
            top_inputs["model_input_num"] = pd.to_numeric(top_inputs["model_input_num"], errors="coerce")
            top_inputs["abs_val"] = top_inputs["model_input_num"].abs()
            top_inputs = top_inputs.sort_values("abs_val", ascending=False).drop(columns=["abs_val"]).head(10)

    ap = pd.DataFrame()
    if not alerts.empty and "project_id" in alerts.columns:
        ap = alerts[alerts["project_id"].astype(str) == str(project)].copy()

    stats = st.columns(4)
    with stats[0]:
        metric_card("Project", str(project), "Current selected project")
    with stats[1]:
        metric_card("Current tier", TIER_LABEL.get(latest_tier, str(latest_tier).title()), f"Threshold-based tier from {risk_col_scores}")
    with stats[2]:
        metric_card("Current risk", fmt_num(latest_risk), "Latest score from current output")
    with stats[3]:
        metric_card("Alerts for project", str(len(ap)) if not ap.empty else "0", "Current alert rows in generated alerts table")

    gauge_col, status_col = st.columns([1.02, 0.98])
    with gauge_col:
        section_start("Current risk position", "Same current risk score, re-presented with clearer tier context.")
        st.plotly_chart(
            risk_gauge(latest_risk, thr_low, thr_med, thr_high, title=f"Current risk ({risk_col_scores})"),
            use_container_width=True,
        )
        section_end()

    with status_col:
        section_start("Current status and rule reference", "Transparent display of the same tier and alert thresholds already used by the pipeline.")
        st.markdown(f"**Tier:** {tier_badge_html(latest_tier)}", unsafe_allow_html=True)
        st.markdown(f"**Risk:** {fmt_num(latest_risk)}")
        st.markdown(
            f"""
- **CPI_LOW** → CPI below **τ_CPI = {tau_cpi:.2f}**
- **SPI_LOW** → SPI below **τ_SPI = {tau_spi:.2f}**
- **RISK_HIGH** → ML risk score ≥ **{thr_high:.2f}** for the generated alert logic
- **Displayed τ_ML control** remains **{tau_ml:.2f}** for evaluation/visual reference
"""
        )
        if not p_panel.empty:
            period_start = fmt_date(p_panel["period_end"].min())
            period_end = fmt_date(p_panel["period_end"].max())
            st.caption(f"Panel coverage in current file: {period_start} to {period_end}")
        section_end()

    row1_left, row1_right = st.columns([1.04, 0.96])

    with row1_left:
        section_start("Risk trajectory by reporting period", "Period-by-period evidence using the same panel and threshold bands.")
        if p_panel.empty:
            st.info("No project period panel available for this project.")
        else:
            fig_rt = risk_trajectory_by_period(p_panel, tiers_cfg, thr_high, thr_med, thr_low)
            if fig_rt is None:
                st.info("Risk trajectory not available (missing period_end or risk column).")
            else:
                st.plotly_chart(fig_rt, use_container_width=True)
        section_end()

    with row1_right:
        section_start("CPI vs SPI vs risk by period", "Same per-period values, arranged for easier scanning and reporting.")
        if p_panel.empty:
            st.info("No panel available for this bubble chart.")
        else:
            fig_bp = bubble_cpi_spi_risk_by_period(p_panel, tiers_cfg, tau_cpi, tau_spi)
            if fig_bp is None:
                st.info("Bubble chart not available (need CPI, SPI, and risk per period).")
            else:
                st.plotly_chart(fig_bp, use_container_width=True)
        section_end()

    row2_left, row2_right = st.columns([1.02, 0.98])

    with row2_left:
        section_start("Risk trend across runs", "Historical refresh-based trend using the current history output.")
        if history.empty or "project_id" not in history.columns:
            st.info("No history file available yet.")
        else:
            hproj = history[history["project_id"].astype(str) == str(project)].copy()
            if hproj.empty:
                st.info("No history rows for this project yet.")
            else:
                rcol_h = pick_risk_col(hproj)
                hproj[rcol_h] = pd.to_numeric(hproj[rcol_h], errors="coerce")
                hproj = hproj.dropna(subset=[rcol_h, "refreshed_at_utc"]).sort_values("refreshed_at_utc")
                fig_h = px.line(hproj, x="refreshed_at_utc", y=rcol_h, markers=True)
                fig_h = add_threshold_lines(fig_h, thr_high, thr_med, thr_low, title="Tier thresholds")
                fig_h.update_layout(xaxis_title="Run time (UTC)", yaxis_title="Risk (0-1)")
                st.plotly_chart(finalise_fig(fig_h, height=350, legend_y=1.12), use_container_width=True)
        section_end()

    with row2_right:
        section_start("Period trends", "CPI, SPI, and risk shown together using the same panel values and visual thresholds.")
        if p_panel.empty:
            st.info("No panel rows for this project.")
        else:
            p = p_panel.copy()
            rcol_panel = pick_risk_col(p)

            figp = go.Figure()
            if "CPI" in p.columns:
                figp.add_trace(go.Scatter(x=p["period_end"], y=p["CPI"], mode="lines+markers", name="CPI"))
                figp.add_hline(y=tau_cpi, line_dash="dot", line_color="#64748B", annotation_text="τ_CPI")
            if "SPI" in p.columns:
                figp.add_trace(go.Scatter(x=p["period_end"], y=p["SPI"], mode="lines+markers", name="SPI"))
                figp.add_hline(y=tau_spi, line_dash="dot", line_color="#64748B", annotation_text="τ_SPI")
            if rcol_panel in p.columns:
                figp.add_trace(go.Scatter(x=p["period_end"], y=p[rcol_panel], mode="lines+markers", name=rcol_panel))
                figp.add_hline(y=tau_ml, line_dash="dot", line_color="#64748B", annotation_text="τ_ML")

            figp.update_layout(xaxis_title="Reporting period", yaxis_title="Value")
            st.plotly_chart(finalise_fig(figp, height=390, legend_y=1.12), use_container_width=True)
        section_end()

    row3_left, row3_right = st.columns([1.02, 0.98])

    with row3_left:
        section_start("Top model inputs", "Largest-magnitude current model inputs for the selected project.")
        if top_inputs.empty:
            st.info("No model inputs available for this project.")
        else:
            st.dataframe(
                top_inputs,
                use_container_width=True,
                hide_index=True,
                column_config={"model_input_num": st.column_config.NumberColumn("model_input_num", format="%.3f")},
            )
        section_end()

    with row3_right:
        section_start("Explainability proxy drivers", "Current z-score-based driver view using the existing features table.")
        zdf = zscore_drivers(features, project)
        if zdf.empty:
            st.caption("Proxy explainability not available (features_wide missing or empty).")
        else:
            top_z = zdf.head(10).copy()
            st.dataframe(
                top_z,
                use_container_width=True,
                hide_index=True,
                column_config={"z": st.column_config.NumberColumn("z", format="%.3f")},
            )
            figz = px.bar(top_z.sort_values("z"), x="z", y="feature", orientation="h")
            figz.update_layout(xaxis_title="z-score", yaxis_title="Feature")
            st.plotly_chart(finalise_fig(figz, height=360, legend_y=1.08), use_container_width=True)
        section_end()

    section_start("Alerts for this project", "Project-level alert rows from the same generated alert table.")
    if ap.empty:
        st.info("No alerts for this project.")
    else:
        st.dataframe(ap, use_container_width=True, hide_index=True)
    section_end()

    if shap_local is not None and not shap_local.empty:
        section_start("SHAP explainability (optional extension)", "Only shown when optional SHAP output exists.")
        sl = shap_local.copy()
        if "project_id" in sl.columns:
            sl = sl[sl["project_id"].astype(str) == str(project)]
        if sl.empty:
            st.caption("No SHAP rows for this project.")
        else:
            sl["shap_value"] = pd.to_numeric(sl.get("shap_value", np.nan), errors="coerce")
            top_pos = sl.sort_values("shap_value", ascending=False).head(10)
            st.dataframe(top_pos, use_container_width=True, hide_index=True)
        section_end()

st.markdown("</div>", unsafe_allow_html=True)

with st.expander("Data preview"):
    tabs = st.tabs(["Scores", "Alerts", "Features", "Inputs", "History", "Panel"])
    with tabs[0]:
        st.dataframe(scores, use_container_width=True, hide_index=True)
    with tabs[1]:
        st.dataframe(alerts, use_container_width=True, hide_index=True)
    with tabs[2]:
        st.dataframe(features, use_container_width=True, hide_index=True)
    with tabs[3]:
        st.dataframe(inputs_long, use_container_width=True, hide_index=True)
    with tabs[4]:
        st.dataframe(history, use_container_width=True, hide_index=True)
    with tabs[5]:
        st.dataframe(panel, use_container_width=True, hide_index=True)


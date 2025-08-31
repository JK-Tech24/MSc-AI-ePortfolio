# Agent Dialogue: Alice and Bob – TV Stock Inquiry

## Context
- **Alice**: Procurement agent (needs stock info)
- **Bob**: Warehouse agent (manages inventory)
- **Protocol**: KQML (communication)
- **Content Language**: KIF (knowledge representation)


## Dialogue

### Step 1 — Alice asks about available 50-inch TVs
```lisp
(ask-one
  :sender Alice
  :receiver Bob
  :language KIF
  :ontology warehouse-inventory
  :content (available-stock (television 50-inch)))
```

### Step 2 — Bob replies with stock info + brands
```lisp
(tell
  :sender Bob
  :receiver Alice
  :language KIF
  :ontology warehouse-inventory
  :content (and (= (stock-level (television 50-inch Samsung)) 15)
                (= (stock-level (television 50-inch LG)) 8)))
```

### Step 3 — Alice asks about HDMI ports
```lisp
(ask-one
  :sender Alice
  :receiver Bob
  :language KIF
  :ontology warehouse-inventory
  :content (hdmi-ports (television 50-inch)))
```

### Step 4 — Bob replies with HDMI details per brand
```lisp
(tell
  :sender Bob
  :receiver Alice
  :language KIF
  :ontology warehouse-inventory
  :content (and (= (hdmi-ports (television 50-inch Samsung)) 3)
                (= (hdmi-ports (television 50-inch LG)) 4)))
```


## Summary
Alice queries 50-inch TV availability. Bob returns brand-specific stock (Samsung (15) and LG (8)). Alice then asks about HDMI ports; Bob confirms Samsung has 3 and LG has 4.

---

## Learning Outcomes (Met)
- **Agent-based computing motivation & use**: Demonstrates precise, automated info exchange between procurement and inventory agents.
- **Agent models & AI grounding**: Uses KQML performatives (`ask-one`, `tell`) and KIF predicates to represent knowledge clearly.

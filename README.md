# Project SURVEA (Smart Unified Reliability and Vulnerability Evaluation for Assets)
**AI-Driven Predictive Asset Health Monitoring & Prognostics for Critical Substation Equipment**

Project SURVEA is an end-to-end predictive maintenance platform for four critical power substation assets: transformers, generators, circuit breakers, and protection relays. It combines Random Forest fault classification, LSTM degradation prognostics, a source-grounded operator advisory system, and a live Digital Twin bridge — all surfaced through a real-time Streamlit dashboard. 

This framework operates as a standalone prognostics and health management (PHM) system. However, the foundational physics-based Digital Twin utilized for real-time telemetry generation and power flow co-simulation (IEEE 39 and 118-bus networks) was originally architected under **Project SWING** (Physics-Validated AI Architecture for Autonomous Grid Resilience). SURVEA adapts SWING's Digital Twin infrastructure to focus exclusively on multi-modal asset health monitoring.

The Streamlit frontend never fabricates data. In live mode, it pulls current telemetry from the Digital Twin's `/asset_health/{grid}` endpoint and runs it through the trained models. In demo mode (twin unreachable), it replays a real row from each asset's own historical CSV. The distinction is always visible to the operator.

---

## 1. Architecture & Separation of Concerns
The system is deliberately split into two independent layers that share no runtime state:

```text
┌─────────────────────────────────────────┐        HTTP         ┌──────────────────────────────┐
│         DIGITAL TWIN SERVICE            │  <────────────────> │     SURVEA ML PIPELINE       │
│   modules/physics_engine/twin_model.py  │                     │     src/                     │
│   modules/physics_engine/api.py         │                     │                              │
│                (port 8001)              │                     │  - RF Fault Classifiers      │
│                                         │                     │  - LSTM RUL Regressors       │
│  - pandapower IEEE-39/118 AC power flow │                     │  - AssetHealthPredictor      │
│  - Asset health simulation (4 types)    │                     │  - Advisory Brief Generator  │
│  - N-1 Contingency Scanner              │                     │  - DigitalTwinClient bridge  │
│  - Scenario & stress test engine        │                     └──────────────────────────────┘
│  - WebSocket telemetry stream           │                                    ▲
└─────────────────────────────────────────┘                                    │
                    ▲                                                           │
                    │ HTTP/WS                                              Streamlit
                    │                                                           │
┌─────────────────────────────────────────┐          ┌──────────────────────────────────────────┐
│         Digital Twin UI                 │          │         SURVEA Dashboard (Streamlit)     │
│         Digital_Twin_UI/                │          │         frontend/                        │
│  Cytoscape.js grid topology viewer,     │          │  Home, Generator, Transformer, Relay,    │
│  live telemetry, fault injection panel  │          │  Circuit Breaker, XAI pages              │
└─────────────────────────────────────────┘          └──────────────────────────────────────────┘

Either service can run independently. The only coupling is the Digital Twin's base URL,
defaulting to http://127.0.0.1:8001.
```

---

## 2. ML Pipeline

### Fault Classification (Random Forest)
All four asset types share a single generic `AssetFaultClassifier` wrapper. Asset-specific behavior — which CSV, which feature columns, which class labels — lives entirely in `src/config.py`. The classifier uses `class_weight="balanced"` throughout; several fault classes are rare (e.g. transformer D2 has only 14 rows), and accuracy would be a misleading metric.

### Degradation Prognostics (LSTM)
Three of the four assets support an LSTM regressor (relay is excluded — its CSV has flat, independently-shuffled snapshot rows with no temporal signal to build sequences from). The LSTM predicts the `regression_target` at the next time step from a sliding window of past readings:

| Asset | Regression Target | Notes |
|---|---|---|
| Transformer | `dga_severity_index` | Max of 6 standardized gas readings — derived here because the dataset's row structure is maintenance-log entries, not smooth degradation trajectories |
| Generator | `Health_Index` | Pre-existing column; confirmed empirically to rise with fault severity |
| Circuit Breaker | `Health_Index` | Same pattern as generator |
| Relay Endurance | `RUL_operations_remaining` | Real ground-truth countdown from actual relay endurance test data |
| Generator Plant Log | `max_bearing_temp_c` | Max across 4 bearing temperature sensors |

### Advisory Brief System
The operator brief is **template-fill only** — it selects and formats paraphrased passages from `src/advisory/knowledge_base.py`, each tagged to a real source document (CBIP manuals, CEA regulations, IS standards). Nothing is LLM-generated. Every sentence in a brief traces to a `KnowledgeEntry` with a real `source_doc` and `source_section`. Retrieval is exact-tag lookup — no embeddings, no vector database, no semantic search — because with ~5–10 entries per (asset_type, fault_class) bucket, a similarity index would add deployment weight for zero retrieval-quality benefit.

---

## 3. Repository Structure

```
Project_SURVEA/
├── data/
│   └── raw/
│       ├── dga_ml_ready.csv                    # transformer DGA (real, per-unit maintenance log)
│       ├── Generator_dataset.csv               # generator vibration + thermal (labeled)
│       ├── cb_refined_dataset.csv              # circuit breaker TCCS + contact travel (labeled)
│       ├── relay_dataset_F.csv                 # relay fault phasors (live-twin-compatible)
│       ├── Relais_0097.h5                      # relay endurance test unit 1 (raw waveforms)
│       ├── Relais_0139.h5                      # relay endurance test unit 2 (raw waveforms)
│       ├── relay_h5_processed.csv              # generated -- run src/data/relay_h5_processor.py
│       └── steam_alternator_generator_log.csv  # real hourly plant telemetry (no fault labels)
│
├── data_generation/
│   ├── generate_transformer_dga.m              # Octave/MATLAB DGA synthetic generator
│   └── synthetic_transformer_dga.csv           # raw ppm + Duval percentages
│
├── Digital_Twin_UI/                            # Standalone Cytoscape.js topology dashboard
│   ├── home.html                               # landing page
│   ├── ieee39.html / ieee118.html              # per-grid topology views
│   ├── app.js                                  # all graph rendering, WebSocket, control logic
│   └── style.css
│
├── docs/
│   └── source_documents/                       # IEGC, CBIP manuals, IS standards (Markdown)
│
├── frontend/                                   # Streamlit multipage app
│   ├── Home.py                                 # grid selector, fleet overview, alert banner
│   ├── shared.py                               # data-access layer (live twin / demo fallback)
│   └── pages/
│       ├── 1_Generator.py
│       ├── 2_Transformer.py
│       ├── 3_Relay.py
│       ├── 4_Circuit_Breaker.py
│       └── 5_XAI.py                           # SHAP / feature-importance explainability page
│
├── models/                                     # generated by src/training/train_all.py
│   ├── <asset>_rf.pkl
│   ├── <asset>_lstm.pt
│   └── scalers/
│       └── <asset>_lstm_scalers.pkl
│
├── modules/
│   ├── event_store.py                          # shared SQLite event timeline (physics + AI)
│   └── physics_engine/
│       ├── api.py                              # FastAPI Digital Twin service (port 8001)
│       ├── twin_model.py                       # TwinModel class — IEEE-39/118 pandapower network
│       ├── scenario_engine.py                  # asset degradation simulators + weather events
│       └── grid_metrics.py                     # GRI, security metrics, health aggregation
│
├── outputs/                                    # generated by evaluation.py (300dpi PNGs)
│
├── src/
│   ├── config.py                               # THE schema for every asset -- read this first
│   ├── data/
│   │   ├── loaders.py                          # CSV -> (X, y) and -> LSTM sequence windows
│   │   └── relay_h5_processor.py              # raw .h5 waveforms -> per-operation feature table
│   ├── models/
│   │   ├── rf_classifier.py                   # generic RF wrapper (asset-agnostic)
│   │   └── lstm_rul.py                        # generic LSTM wrapper (asset-agnostic)
│   ├── training/
│   │   └── train_all.py                       # trains + saves all models
│   ├── inference/
│   │   └── predictor.py                       # AssetHealthPredictor -- the frontend's entry point
│   ├── live_feed/
│   │   └── digital_twin_client.py             # bridges Digital Twin telemetry to model feature schema
│   └── advisory/
│       ├── knowledge_base.py                  # paraphrased passages tagged (asset_type, fault_class)
│       ├── retriever.py                       # exact-tag lookup (no embeddings at this scale)
│       └── brief_generator.py                 # template-fill only -- never LLM-generated text
│
├── evaluation.py                               # generates all research figures (real numbers, not placeholders)
├── launch.py                                   # starts the Digital Twin API + static frontend server
├── relay_data_gen.m                            # relay dataset generation script
└── requirements.txt
```

---

## 4. Key Design Decisions

**No fabricated data, anywhere.**
Every regression target is either a pre-existing column in the source CSV (generator's `Health_Index`, circuit breaker's `Health_Index`, relay endurance's `RUL_operations_remaining`) or an explicitly documented heuristic derived from real sensor readings (`dga_severity_index`, `max_bearing_temp_c`). The relay classification model — where the source CSV has no timestamps and no unit IDs — gets no LSTM at all rather than a fake one.

**config.py is the single source of truth.**
Every asset-specific detail (CSV path, feature columns, classification label, class names, regression target, whether LSTM is supported, higher-is-worse direction) lives in `src/config.py`. Training scripts, the predictor, and the live-feed client never hardcode a column name themselves.

**Digital Twin client bridges two different baselines.**
The Digital Twin simulates the primary sensor readings but not the engineered features several training CSVs also include (ratio features, deviation-from-baseline columns, Duval percentages). `digital_twin_client.py` derives those from the real baseline constants found in the source CSVs — not the Twin's own internal baselines, which are different numbers — and documents every fallback explicitly.

**GRI composite metric.**
The Grid Resilience Index (0–100) combines three sub-scores: voltage deviation from nominal (weight 0.35), max line loading (0.40), and number of overloaded lines (0.25). A non-convergent power flow is explicitly caught as `collapsed: True` (GRI = 0.0), not silently ignored.

---

## 5. Setup & Installation

**1. Install dependencies**
```bash
pip install -r requirements.txt
```

**2. Process the relay endurance data** (only needed once)
```bash
python -m src.data.relay_h5_processor
```

**3. Train all models**
```bash
python -m src.training.train_all
```

**4. Start the Digital Twin backend** (optional — Streamlit falls back to demo mode without it)
```bash
python launch.py
# Digital Twin UI: http://127.0.0.1:5500/home.html
# Digital Twin API: http://127.0.0.1:8001
```

**5. Launch the Streamlit dashboard**
```bash
streamlit run frontend/Home.py
```

---

## 6. Evaluation

Regenerates all research figures to `outputs/` as 300dpi PNGs. Every number is recomputed from real models and real data — no hardcoded results.

```bash
python evaluation.py
```

Outputs include: per-asset confusion matrices, LSTM forecast plots (actual vs predicted ± RMSE), macro-F1 summary bar chart, feature importance charts, class distribution charts, relay cross-unit generalization ablation, and the physics-validated GRI resilience impact chart (with a real bisection-search corrective action, not a placeholder multiplier).

---

## 7. Known Limitations

- **Relay classification is live-twin-compatible, relay endurance is not.** The `relay` asset type uses `relay_dataset_F.csv` (5 fault phasors exactly matching what the Digital Twin simulates). The `relay_endurance` asset type is trained on real .h5 waveform data — physically different quantities — and cannot feed live twin telemetry.

- **Transformer Duval percentages are approximated.** The true Duval Triangle requires raw ppm values the Digital Twin never simulates. Live transformer inference falls back to Normal-class means from the training data for these three features. This is documented in `digital_twin_client.py`, flagged in predictor responses, and is not a hidden approximation.

- **LSTM sequence window is a fixed length of 20.** Training datasets with fewer rows per unit (after groupby splitting) may not produce enough windows; the loader raises a `ValueError` with an explicit message rather than silently returning an empty array.

- **Event store is SQLite.** `modules/event_store.py` uses SQLite for the shared event timeline. It handles concurrent single-writer access from the Digital Twin and the Streamlit app fine at local scale. Swap the internals for DuckDB or Postgres if that becomes a constraint.

---

## 8. Academic Scope

Project SURVEA focuses on predictive maintenance and asset health prognostics for substation equipment: fault classification, remaining-useful-life estimation, and structured operator advisory grounded in real standards documents. It is intentionally distinct from grid-level power flow optimization and autonomous control — that domain is covered by the companion **Project SWING**.

---


## Team & Contributions

- **Utthan Singh Roy** *Project Lead & AI Architecture*
    - B.Tech in Electrical Engineering, Madan Mohan Malaviya University of Technology (MMMUT)
    - B.Sc. (Hons) in Data Science and Artificial Intelligence, IIT Guwahati

- **Vartika Pandey** *Frontend UI/UX & HMI Integration*
    - B.Tech in Electrical Engineering, Madan Mohan Malaviya University of Technology (MMMUT)

- **Raj Kamal** *Data Engineering & Systems Integration*
    - B.Tech in Electrical Engineering, Madan Mohan Malaviya University of Technology (MMMUT)

- **Shivangi Singh** *Power Systems Domain & Regulatory Mapping*
    - B.Tech in Electrical Engineering, Madan Mohan Malaviya University of Technology (MMMUT)
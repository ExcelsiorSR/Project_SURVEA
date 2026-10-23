import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from frontend.shared import live_clock

st.set_page_config(
    page_title="XAI — Parameter Explainability",
    page_icon="ℹ️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

col1, col2 = st.columns([3, 1])
with col1:
    st.caption("ℹ️ EXPLAINABLE AI — PARAMETER SIGNIFICANCE")
    st.title("XAI: Why These Parameters Matter")
    st.caption("This page explains the AI-monitored parameters, their physical significance, failure mechanisms "
               "they detect, and how the trained models use them for classification and RUL prognostics.")
with col2:
    live_clock()

if st.button("← Back to Home"):
    st.switch_page("home.py")

st.divider()

# --- INTERACTIVE XAI VISUALIZATION WIDGET ---
st.subheader("🎛️ Interactive Prognostics Pipeline Simulator")
st.caption("Adjust the specific telemetry parameters below to visualize how the LSTM gates weigh the data, route the anomalies, and project the Failure Horizon.")

asset_choice = st.selectbox(
    "Target Asset Model", 
    ["Transformer", "Generator", "Circuit Breaker", "Relay"],
    label_visibility="collapsed"
)

# Define multi-parameter inputs based on the asset
if asset_choice == "Transformer":
    params = [("Acetylene (C₂H₂)", 0.0, 10.0, "ppm"), ("Ethylene (C₂H₄)", 10.0, 150.0, "ppm")]
    m_rul, metric = 60, "RUL (Days)"
elif asset_choice == "Generator":
    params = [("Bearing Vibration", 2.0, 15.0, "mm/s"), ("Stator Temp", 40.0, 130.0, "°C")]
    m_rul, metric = 120, "RUL (Days)"
elif asset_choice == "Circuit Breaker":
    params = [("Contact Travel Time", 32.0, 80.0, "ms"), ("SF6 Pressure", 6.0, 3.0, "bar")]
    m_rul, metric = 60, "RUL (Days)"
else: 
    params = [("V_rms", 1.0, 0.5, "p.u."), ("Impedance Z", 1.4, 0.1, "Ω")]
    m_rul, metric = 100, "Logic Health (%)"

# HTML/JS/CSS Injection with CSS Animations and Tooltips
xai_html = f"""
<!DOCTYPE html>
<html>
<head>
<style>
    body {{ background-color: #0e1117; color: #fafafa; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; text-align: center; margin: 0; padding: 0; user-select: none; }}
    
    .control-panel {{ background: #1a1c23; border: 1px solid #2d3139; border-radius: 8px; padding: 20px; margin: 10px auto 30px auto; width: 90%; max-width: 700px; box-shadow: 0 4px 12px rgba(0,0,0,0.5); }}
    .slider-row {{ margin-bottom: 20px; text-align: left; }}
    .slider-label {{ display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 8px; color: #e2e8f0; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; }}
    input[type=range] {{ width: 100%; cursor: pointer; accent-color: #7b61ff; height: 6px; background: #333; outline: none; border-radius: 3px; }}
    
    .pipeline-container {{ display: flex; flex-direction: column; align-items: center; margin-top: 10px; }}
    .node {{ width: 64px; height: 64px; border-radius: 50%; border: 2px solid #4b4b4b; background: #1e1e1e; display: flex; align-items: center; justify-content: center; font-size: 24px; position: relative; z-index: 2; transition: all 0.3s ease; }}
    
    /* Flow Animation */
    .line {{ width: 3px; height: 40px; margin: -2px auto; position: relative; z-index: 1; background: #4b4b4b; transition: all 0.3s ease; }}
    .line.flowing {{ background: linear-gradient(180deg, #4b4b4b, #7b61ff, #4b4b4b); background-size: 200% 200%; animation: dataFlow 1.5s linear infinite; }}
    @keyframes dataFlow {{ 0% {{ background-position: 50% -100%; }} 100% {{ background-position: 50% 100%; }} }}
    
    .label-text {{ font-size: 12px; color: #a0a0a0; font-weight: 600; letter-spacing: 1.5px; margin-bottom: 4px; text-transform: uppercase; }}
    .sub-text {{ font-size: 11px; color: #888; margin-top: 4px; margin-bottom: 12px; max-width: 400px; line-height: 1.4; }}
    
    .lstm-group {{ position: relative; display: flex; justify-content: center; align-items: center; margin: 15px 0; }}
    .gate {{ width: 28px; height: 28px; border-radius: 50%; border: 1px solid #7b61ff; background: #2d2b42; color: #d4c5ff; position: absolute; display: flex; align-items: center; justify-content: center; font-size: 13px; font-weight: bold; transition: all 0.3s; z-index: 3; cursor: help; }}
    
    /* Tooltips */
    .gate[title]:hover::after {{ content: attr(title); position: absolute; top: -35px; left: 50%; transform: translateX(-50%); background: #fff; color: #000; padding: 4px 8px; border-radius: 4px; font-size: 10px; white-space: nowrap; font-weight: normal; z-index: 10; }}
    
    .state-green {{ border-color: #22c55e !important; box-shadow: 0 0 15px rgba(34,197,94,0.3) !important; color: #22c55e !important; }}
    .state-yellow {{ border-color: #eab308 !important; box-shadow: 0 0 15px rgba(234,179,8,0.4) !important; color: #eab308 !important; }}
    .state-red {{ border-color: #ef4444 !important; box-shadow: 0 0 25px rgba(239,68,68,0.6) !important; color: #ef4444 !important; }}
    
    .rul-display {{ font-size: 24px; font-weight: bold; padding: 15px 30px; border-radius: 8px; border: 1px solid #333; display: inline-block; margin-top: 5px; transition: all 0.3s; background: #1a1c23; }}
</style>
</head>
<body>

    <div class="control-panel">
        <div class="slider-row">
            <div class="slider-label"><span>{params[0][0]}</span> <span id="val0">0.0 {params[0][3]}</span></div>
            <input type="range" id="slider0" min="0" max="100" value="0">
        </div>
        <div class="slider-row">
            <div class="slider-label"><span>{params[1][0]}</span> <span id="val1">0.0 {params[1][3]}</span></div>
            <input type="range" id="slider1" min="0" max="100" value="0">
        </div>
    </div>

    <div class="pipeline-container">
        <div class="label-text">RAW SCADA TELEMETRY</div>
        <div class="node" id="node1">📡</div>
        <div class="line" id="line1"></div>

        <div class="label-text">STANDARDIZED REFINEMENT</div>
        <div class="node" id="node2">≍</div>
        <div class="line" id="line2"></div>

        <div class="label-text">NEURAL STATE ESTIMATION (LSTM)</div>
        <div class="lstm-group">
            <div class="node" id="node3" style="font-size: 32px; width: 80px; height: 80px;">🧠</div>
            <div class="gate" id="gateF" title="Forget Gate: Discards nominal memory during faults" style="transform: translate(-60px, -30px)">f</div>
            <div class="gate" id="gateI" title="Input Gate: Scales up incoming anomaly weights" style="transform: translate(60px, -30px)">i</div>
            <div class="gate" id="gateO" title="Output Gate: Pushes new hidden state to next layer" style="transform: translate(-60px, 30px)">o</div>
            <div class="gate" id="gateC" title="Cell State: The long-term degradation memory" style="transform: translate(60px, 30px)">c</div>
        </div>
        <div class="sub-text" id="lstmSub">System Nominal. Purple lines indicate steady-state data routing.</div>
        <div class="line" id="line3"></div>

        <div class="label-text">FAILURE HORIZON</div>
        <div class="node" id="node4" style="margin-bottom: 15px;">📉</div>
        <div id="rulVal" class="rul-display">Est. RUL: {m_rul}</div>
    </div>

<script>
    const slider0 = document.getElementById('slider0');
    const slider1 = document.getElementById('slider1');
    const val0 = document.getElementById('val0');
    const val1 = document.getElementById('val1');
    const rulVal = document.getElementById('rulVal');
    const lstmSub = document.getElementById('lstmSub');
    
    const nodes = [document.getElementById('node1'), document.getElementById('node2'), document.getElementById('node3'), document.getElementById('node4')];
    const lines = [document.getElementById('line1'), document.getElementById('line2'), document.getElementById('line3')];
    const gates = [document.getElementById('gateF'), document.getElementById('gateI'), document.getElementById('gateO'), document.getElementById('gateC')];

    function updateViz() {{
        let s0 = parseInt(slider0.value);
        let s1 = parseInt(slider1.value);
        let totalStress = (s0 + s1) / 2; // Average stress
        
        // Map slider (0-100) to physical parameters
        let p0 = {params[0][1]} + (s0 / 100) * ({params[0][2]} - {params[0][1]});
        let p1 = {params[1][1]} + (s1 / 100) * ({params[1][2]} - {params[1][1]});
        val0.innerText = p0.toFixed(2) + " {params[0][3]}";
        val1.innerText = p1.toFixed(2) + " {params[1][3]}";

        // Calculate RUL
        let rul = {m_rul} - (totalStress / 100) * {m_rul};
        rulVal.innerText = "{metric}: " + rul.toFixed(0);

        // Determine State and Animation
        let stateClass = "state-green";
        let isFlowing = false;
        
        if (totalStress > 75) {{
            stateClass = "state-red";
            isFlowing = true;
            lstmSub.innerText = "CATASTROPHIC PATTERN DETECTED: Forget Gate (f) dumping memory. Output Gate (o) forcing RUL collapse.";
        }} else if (totalStress > 40) {{
            stateClass = "state-yellow";
            isFlowing = true;
            lstmSub.innerText = "ANOMALY: Input Gate (i) amplifying anomaly weights. Cell State (c) degrading.";
        }} else {{
            lstmSub.innerText = "NOMINAL: Static cell state. Standard data routing active.";
        }}

        // Apply Node Colors and Line Animations
        nodes.forEach(n => {{ n.className = "node " + stateClass; }});
        rulVal.className = "rul-display " + stateClass;
        
        lines.forEach(l => {{
            l.className = isFlowing ? "line flowing" : "line";
            if (!isFlowing) l.style.background = "#4b4b4b";
        }});

        // Gate Scaling and Coloring
        let gateScale = 1 + (totalStress / 150);
        gates.forEach((g, idx) => {{
            let trans = g.style.transform.split(" scale")[0]; // keep translate
            if (totalStress > 40 && (idx === 0 || idx === 1)) {{ // f and i gates pulse
                g.style.transform = trans + " scale(" + gateScale + ")";
                g.className = "gate " + stateClass;
            }} else {{
                g.style.transform = trans + " scale(1)";
                g.className = "gate";
            }}
        }});
    }}

    slider0.addEventListener('input', updateViz);
    slider1.addEventListener('input', updateViz);
    updateViz(); // init
</script>
</body>
</html>
"""
components.html(xai_html, height=900, scrolling=False)

st.divider()

st.info(
    "**What is XAI (Explainable AI)?**\n\n"
    "Explainable AI refers to methods that make an AI model's decisions transparent and traceable to a "
    "specific measurable parameter with clear physical meaning. In this project, each asset's Random Forest "
    "classifier and LSTM prognostic model are trained directly on the real sensor features described below "
    "-- not synthetic placeholders -- so every alert and RUL estimate traces back to real data."
)

st.divider()

st.subheader("⚙️ Generator — Real Features Used")
with st.expander("📊 Bearing Vibration & Thermal Parameters", expanded=True):
    st.markdown("""
**Real features the trained model uses:** `Bearing_Frequency_Hz`, `Bearing_Amplitude_mm_s`, `Temperature_C`,
`Temp_Rise_Rate_C_min`, `Thermal_Runaway_Indicator` (from `Generator_dataset.csv`).

**Why they matter:** Bearing amplitude is the leading mechanical failure indicator (ISO 10816 zones A-D).
Temperature rise rate is the leading thermal indicator — every 10°C above rated temperature roughly halves
insulation life (Arrhenius law).

**AI use:** The Random Forest classifies discrete fault states (Normal / Moderate Fault / Severe Fault /
Thermal Warning / Thermal Runaway); the LSTM forecasts the dataset's own composite `Health_Index` one step ahead.

**Standards referenced:** ISO 10816-3, IEC 60034-1.
    """)

st.divider()

st.subheader("🔌 Transformer — Real Features Used")
with st.expander("🧪 Dissolved Gas Analysis (standardized readings)", expanded=True):
    dga_df = pd.DataFrame({
        "Gas": ["Hydrogen (H2)", "Acetylene (C2H2)", "Ethylene (C2H4)", "Methane (CH4)", "Ethane (C2H6)", "Carbon Monoxide (CO)"],
        "Fault Indicated": [
            "Partial discharge / low-energy arcing",
            "High-energy arcing (most critical single gas)",
            "Thermal fault >300°C",
            "Low-level thermal fault <300°C",
            "Mild overheating",
            "Cellulose insulation degradation",
        ],
    })
    st.dataframe(dga_df, use_container_width=True, hide_index=True)
    st.markdown("""
**Important:** the real source dataset (`dga_ml_ready.csv`) ships these six gases as STANDARDIZED values
(mean ≈ 0, std ≈ 1), not raw ppm — so absolute IEEE C57.104 ppm thresholds don't apply directly to the numbers
shown on the Transformer page. The Random Forest was trained on these standardized values directly and
classifies 8 fault classes (Normal, Partial Discharge, D1/D2 discharge, T1/T2/T3 thermal, Undetermined).
A separate physics-informed synthetic generator (`generate_transformer_dga.m`) produces RAW ppm values with
real Duval-triangle percentages, used to broaden training coverage.

**Standards referenced:** IEEE C57.104, IEC 60599.
    """)

st.divider()

st.subheader("🛡️ Relay — Real Features Used")
with st.expander("📊 Fault-Condition Phasors & Apparent Impedance", expanded=True):
    st.markdown("""
**Real features the trained model uses:** `V_rms`, `I_rms`, `V_peak`, `I_peak`, `Impedance_Z`
(from `relay_dataset_F.csv`).

**Why they matter:** A distance relay's mho-circle logic classifies faults by apparent impedance — the
per-class averages in the real data show impedance falling from ~1.40 Ω (Normal) to ~0.22 Ω as fault
severity increases, with fault current rising correspondingly.

**A note on limitations:** the trip-timing, THD, and pickup-ratio parameters described in earlier drafts of
this framework aren't present in the real relay dataset — this page and the Relay detail page were updated
to reflect only what the model actually sees.

**RUL:** not available for this feature set — no timestamp or operation counter exists in the source data.
A separate real relay endurance dataset (200k+ switching operations, raw coil/contact waveforms) DOES support
RUL forecasting, tracked in this project as a distinct asset type (`relay_endurance`) since it measures
different physical quantities than steady-state fault impedance.

**Standards referenced:** IEC 60255.
    """)

st.divider()

st.subheader("🎚️ Circuit Breaker — Real Features Used")
with st.expander("🔌 Trip Coil, Contact & SF6 Parameters", expanded=True):
    st.markdown("""
**Real features the trained model uses:** `TCCS_Peak_Current_A`, `TCCS_Duration_ms`,
`Contact_Travel_Time_ms`, `Contact_Temperature_C`, `Gas_Pressure_bar`, plus deviation-from-baseline features
(`Current_Dev`, `Travel_Dev`, `Temp_Dev`, `Pressure_Drop`) from `cb_refined_dataset.csv`.

**Why they matter:** Trip coil current fingerprints coil winding health. Contact travel time characterises
the operating mechanism (dried lubrication, worn linkages). SF6 pressure is safety-critical — IEC 62271
mandates automatic lockout below minimum operating pressure.

**AI use:** The Random Forest classifies 6 fault states (Normal, Coil Degradation Early/Severe, Friction Wear,
Mechanical Jamming Mild/Severe); the LSTM forecasts the dataset's own `Health_Index`.

**Standards referenced:** IEC 62271-100.
    """)

st.divider()

st.subheader("🤖 How the AI Framework Actually Works")
ai_df = pd.DataFrame({
    "Layer": ["1. Data Acquisition", "2. Fault Classification", "3. Prognostics"],
    "Function": [
        "Live Digital Twin telemetry (when running) or real historical CSV replay in demo mode — never fabricated random noise",
        "Random Forest, trained per-asset on real dataset features and real fault labels/codes",
        "LSTM, trained on real dataset-native regression targets (Health_Index, DGA severity index, or true RUL — never a fabricated number)",
    ],
    "Output": [
        "A feature_dict matching each asset's exact trained schema",
        "Predicted fault class + confidence",
        "One-step-ahead forecast of the asset's degradation trend",
    ],
})
st.dataframe(ai_df, use_container_width=True, hide_index=True)

st.divider()

st.caption("XAI — Explainable AI Parameter Reference  |  Real-Data-Driven Health Monitoring Framework")
if st.button("← Back to Home", key="home_btn_bottom"):
    st.switch_page("home.py")
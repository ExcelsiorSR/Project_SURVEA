import streamlit as st
import pandas as pd
from datetime import datetime
import pytz
import sys
from pathlib import Path
from shared import render_industrial_gauge

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from frontend.shared import (
    get_prediction, risk_badge, enable_autorefresh, live_clock, get_selected_grid,
    render_fleet_alert_banner, get_fleet_asset_ids, get_fleet_overview,
)

st.set_page_config(page_title="Relay Fleet | Health Monitor", page_icon="🛡️", layout="wide", initial_sidebar_state="collapsed")
enable_autorefresh(interval_seconds=3)

ist = pytz.timezone("Asia/Kolkata")
now_str = datetime.now(ist).strftime("%d %b %Y  %H:%M:%S IST")

# --- HEADER ---
col1, col2 = st.columns([3, 1])
with col1:
    st.caption("🛡️ ASSET FLEET VIEW — PROTECTION RELAYS")
    st.title(f"Relay Fleet — IEEE {get_selected_grid()}-Bus System")
with col2:
    live_clock()

st.divider()

# Fleet-wide alert
render_fleet_alert_banner(current_asset_type="relay")

# --- VISUAL FLEET DASHBOARD ---
st.subheader("🛡️ Relay Fleet Overview")
st.caption("One protection relay is modelled per bus on this grid.")
all_ids = get_fleet_asset_ids("relay")
overview = get_fleet_overview("relay")

if "selected_rly_id" not in st.session_state or st.session_state["selected_rly_id"] not in all_ids:
    failing_unit = next((a["asset_id"] for a in overview if a["fault_class"] != "Normal"), None)
    st.session_state["selected_rly_id"] = failing_unit if failing_unit is not None else (all_ids[0] if all_ids else 0)

if overview:
    st.caption("Click any unit below to view live telemetry and diagnostics.")
    cols = st.columns(8) 
    for index, asset in enumerate(overview):
        uid = asset["asset_id"]
        fc = asset["fault_class"]
        
        if fc == "Normal":
            btn_label = f"🟢 R-{uid:02d}\nNormal"
        elif "Critical" in fc or "CATASTROPHIC" in fc:
            btn_label = f"🔴 R-{uid:02d}\n{fc}"
        else:
            btn_label = f"🟡 R-{uid:02d}\n{fc}"
            
        with cols[index % 8]:
            if st.button(btn_label, key=f"btn_rly_{uid}", use_container_width=True):
                st.session_state["selected_rly_id"] = uid
                st.rerun()
else:
    st.info("Live twin disconnected. Demo mode active.")
    st.session_state["selected_rly_id"] = st.selectbox("Select Relay", options=all_ids, format_func=lambda i: f"Relay R-{i:02d}")

col1, col2, col3 = st.columns([1, 1, 1])

with col2:

    btn_left, btn_center, btn_right = st.columns([1, 1, 1])

    with btn_center:
        if st.button("🔄 Refresh Grid State", width = 'content'):
            st.rerun()


st.divider()

# --- DETAILED SINGLE-UNIT VIEW ---
selected_id = st.session_state["selected_rly_id"]
result = get_prediction("relay", asset_id=selected_id)
r = result["reading"]
clf = result["classification"]
badge = risk_badge(clf["fault_label"])

st.subheader(f"📡 Relay R-{selected_id:02d} (Bus {selected_id}) — Health & Diagnostics")
st.caption(f"Unit {selected_id} of {len(all_ids)} on this grid  |  Model: Random Forest (impedance-zone classifier)  |  "
           f"{'🟢 LIVE DIGITAL TWIN FEED' if result['source'] == 'LIVE DIGITAL TWIN' else '🟡 DEMO MODE — replaying real historical readings'}")

# --- MODEL ASSESSMENT ---
st.subheader("🔔 Model Assessment")
if clf["fault_label"] == "Normal":
    st.success(f"{badge} — Random Forest classifier: **{clf['fault_label']}** (confidence {clf['confidence']:.0%})")
else:
    alert_fn = st.error if "🔴" in badge else st.warning
    alert_fn(
        f"{badge} — Random Forest classifier: **{clf['fault_label']}** (confidence {clf['confidence']:.0%})\n\n"
        f"Impedance Z: {r['Impedance_Z']:.3f} Ω  |  I_rms: {r['I_rms']:.3f}  |  I_peak: {r['I_peak']:.3f}"
    )

st.divider()

# --- OPERATOR BRIEF ---
st.subheader("🧠 Operator Brief")
st.caption("Retrieved guidance, not AI-generated prose -- every passage below cites its source document.")
st.markdown(result["brief"].markdown)

st.divider()

# --- LIVE PARAMETER FEED ---
st.subheader("⚡ Live Parameter Feed")
st.caption(f"Source: {result['source']}  |  Features: $V_{{rms}}$, $I_{{rms}}$, $V_{{peak}}$, $I_{{peak}}$, $Z$ (mho-circle distance protection)")

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric(label=r"$V_{rms}$", value=f"{r['V_rms']:.3f}")
c2.metric(label=r"$I_{rms}$", value=f"{r['I_rms']:.3f}")
c3.metric(label=r"$V_{peak}$", value=f"{r['V_peak']:.3f}")
c4.metric(label=r"$I_{peak}$", value=f"{r['I_peak']:.3f}")
c5.metric(label=r"Impedance $Z$", value=f"{r['Impedance_Z']:.3f} Ω")
st.caption("Apparent impedance falling toward ~0.2-0.3 Ω indicates a fault electrically closer to the relay.")

st.divider()

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    # Nominal V_rms in dataset is ~0.71 (Normal operating band: 0.65 to 0.76)
    v_steps = [
        {'range': [0.0, 0.60], 'color': 'rgba(239, 68, 68, 0.2)'},     # Voltage Collapse
        {'range': [0.60, 0.65], 'color': 'rgba(234, 179, 8, 0.2)'},    # Undervoltage Warning
        {'range': [0.65, 0.76], 'color': 'rgba(34, 197, 94, 0.25)'},   # Nominal Healthy Band
        {'range': [0.76, 0.85], 'color': 'rgba(234, 179, 8, 0.2)'},    # Overvoltage Warning
        {'range': [0.85, 1.20], 'color': 'rgba(239, 68, 68, 0.2)'}     # Severe Overvoltage
    ]
    render_industrial_gauge(r['V_rms'], "V (RMS)", 0.0, 1.2, "p.u.", steps=v_steps)

with c2:
    # Nominal I_rms in dataset is ~0.36
    i_steps = [
        {'range': [0.0, 0.45], 'color': 'rgba(34, 197, 94, 0.25)'},    # Normal Load Current
        {'range': [0.45, 0.75], 'color': 'rgba(234, 179, 8, 0.2)'},    # Elevated Current
        {'range': [0.75, 2.00], 'color': 'rgba(239, 68, 68, 0.2)'}     # Heavy Fault Current
    ]
    render_industrial_gauge(r['I_rms'], "I (RMS)", 0.0, 2.0, "p.u.", steps=i_steps)

with c3:
    # Nominal V_peak in dataset is ~1.06
    vp_steps = [
        {'range': [0.0, 0.90], 'color': 'rgba(239, 68, 68, 0.2)'},     # Low Peak
        {'range': [0.90, 0.98], 'color': 'rgba(234, 179, 8, 0.2)'},    # Dip Warning
        {'range': [0.98, 1.14], 'color': 'rgba(34, 197, 94, 0.25)'},   # Nominal Healthy Band
        {'range': [1.14, 1.25], 'color': 'rgba(234, 179, 8, 0.2)'},    # Surge Warning
        {'range': [1.25, 1.60], 'color': 'rgba(239, 68, 68, 0.2)'}     # Overvoltage Peak
    ]
    render_industrial_gauge(r['V_peak'], "V (Peak)", 0.0, 1.6, "p.u.", steps=vp_steps)

with c4:
    # Nominal I_peak in dataset is ~0.53
    ip_steps = [
        {'range': [0.0, 0.70], 'color': 'rgba(34, 197, 94, 0.25)'},    # Normal Current Peak
        {'range': [0.70, 1.50], 'color': 'rgba(234, 179, 8, 0.2)'},    # Inrush / Moderate Surge
        {'range': [1.50, 5.00], 'color': 'rgba(239, 68, 68, 0.2)'}     # Severe Fault Current Peak
    ]
    render_industrial_gauge(r['I_peak'], "I (Peak)", 0.0, 5.0, "p.u.", steps=ip_steps)

with c5:
    # Mho-circle distance zones (Nominal Z ~ 1.40 Ohm)
    z_steps = [
        {'range': [0.0, 0.28], 'color': 'rgba(239, 68, 68, 0.25)'},    # Zone 1 Fault (Trip)
        {'range': [0.28, 0.40], 'color': 'rgba(239, 68, 68, 0.2)'},    # Zone 2 Fault (Trip)
        {'range': [0.40, 0.90], 'color': 'rgba(234, 179, 8, 0.2)'},    # Zone 3 Fault (Warning)
        {'range': [0.90, 2.00], 'color': 'rgba(34, 197, 94, 0.25)'}    # Healthy Operating Region
    ]
    render_industrial_gauge(r['Impedance_Z'], "Impedance Z", 0.0, 2.0, "Ω", steps=z_steps)

st.divider()

# --- PROGNOSTICS ---
st.subheader("⏱️ Prognostics")
st.warning(
    "**No RUL/trend forecast available for this relay model.** The source dataset "
    "(`relay_dataset_F.csv`) has no timestamp, unit ID, or operation counter — just "
    "independent snapshot readings — so there is no time-series to extrapolate dynamic failure boxes from."
)

st.divider()

# --- MAINTENANCE (Dual View & Action Dispatch) ---
st.subheader("🔧 Mandatory Maintenance — Action Required")

maintenance_df = pd.DataFrame({
    "Fault Class": ["Elevated Fault Current", "Moderate Impedance Fault", "Critical Zone Fault", "CATASTROPHIC MISOPERATION"],
    "Recommended Action": [
        "Verify CT ratio, check for distant downstream faults",
        "Secondary injection test — confirm trip coordination curves",
        "Immediate protection scheme review — fault deep in trip zone",
        "UNIT ISOLATED. Relay logic compromised. Recalibrate Mho-circle distance settings immediately."
    ],
    "Priority": ["🟡 MEDIUM", "🟡 MEDIUM", "🔴 HIGH", "🚨 CRITICAL"],
})

if clf["fault_label"] == "Normal":
    st.success("**Status:** Relay logic and impedance trajectory are nominal. No mandatory maintenance required.")
else:
    active_maintenance = maintenance_df[maintenance_df["Fault Class"] == clf["fault_label"]]
    if not active_maintenance.empty:
        action = active_maintenance.iloc[0]["Recommended Action"]
        priority = active_maintenance.iloc[0]["Priority"]
        
        maint_key = f"maint_dispatched_rly_{selected_id}"
        
        if st.session_state.get(maint_key, False):
            st.success(f"✅ **Maintenance Crew Dispatched.** Relay R-{selected_id:02d} is isolated and pending physical recalibration.")
            if st.button("Complete Repair & Reset Asset Status"):
                st.session_state[maint_key] = False
                st.rerun()
        else:
            st.error(f"**Prescribed Task ({priority}):** {action}")
            if st.button(f"🚨 Dispatch Maintenance Team to R-{selected_id:02d}", type="primary"):
                st.session_state[maint_key] = True
                st.session_state['auto_redirect'] = False 
                st.rerun()
    else:
        st.warning(f"**Prescribed Action:** No standard maintenance protocol mapped for fault class: {clf['fault_label']}")

st.caption("Standard Maintenance Reference Dictionary (Schedule Within 30 Days)")
st.dataframe(maintenance_df, width='stretch', hide_index=True)

st.divider()

# --- FOOTER ---
nav1, nav2, nav3 = st.columns([1, 1, 4])
with nav1:
    if st.button("← Back to Home"):
        st.switch_page("home.py")
with nav2:
    if st.button("ℹ️ XAI Explanation"):
        st.switch_page("pages/5_XAI.py")
with nav3:
    st.caption(f"Fleet: {len(all_ids)} relay(s)  |  Model-driven live feed (RF only)")
import streamlit as st

st.set_page_config(page_title="Sentinel Hub", layout="wide", initial_sidebar_state="collapsed")

# EYE-FRIENDLY "FOREST DARK" THEME
st.markdown("""
<style>
    .stApp { background-color: #0B0E11; color: #D1D5DB; }
    [data-testid="stMetricValue"] { color: #4ADE80 !important; font-family: 'Courier New', monospace; }
    .stButton>button { border: 1px solid #059669 !important; background: #064E3B !important; color: white !important; width: 100%; border-radius: 8px; }
    .stAlert { background-color: #111827 !important; border: 1px solid #374151 !important; color: #10B981 !important; }
</style>
""", unsafe_allow_html=True)

st.title("🛡️ Sentinel Alpha: Strategic Command")
st.caption("EAT Timezone | Satellite Uplink: 🟢 STABLE")

# --- FEATURES 1-10: LIVE METRICS ---
col1, col2, col3, col4 = st.columns(4)
with col1: st.metric("Elephant Corridors", "Active", "North")
with col2: st.metric("Acoustic Sensors", "98%", "Online")
with col3: st.metric("Poaching Threat", "Low", "-12%")
with col4: st.metric("Ranger Vitals", "Stable", "99 BPM")

st.markdown("---")

# --- FEATURES 11-30: MISSION CONTROL GRID ---
st.subheader("🛠️ Tactical Operations")
c1, c2, c3 = st.columns(3)

with c1:
    st.write("**Intelligence & Mapping**")
    if st.button("🛰️ Advanced AI Intel"): st.switch_page("pages/12_Advanced_Intel.py")
    if st.button("🗺️ Interactive Sightings"): st.switch_page("pages/5_Sightings_Map.py")
    if st.button("🧬 Bio-Analytic Reports"): st.switch_page("pages/11_Generate_Report.py")

with c2:
    st.write("**Field Operations**")
    if st.button("📝 Log Field Notes"): st.switch_page("pages/9_Field_Notes.py")
    if st.button("🚁 Drone Surveillance"): st.switch_page("pages/14_Ranger_Academy.py")
    if st.button("🐾 Species Guide"): st.switch_page("pages/6_Species_Guide.py")

with c3:
    st.write("**Team & Coordination**")
    if st.button("🏆 Global Leaderboard"): st.switch_page("pages/4_Leaderboard.py")
    if st.button("🛡️ Sentinel Academy"): st.switch_page("pages/14_Ranger_Academy.py")
    if st.button("💬 Mission Comms"): st.info("Chat link coming soon...")

st.markdown("---")

# --- FEATURES 31-40: STATUS FEED ---
with st.container():
    st.info("📡 **Recent Intel Feed:** Drone 04 detected a Black Rhino mother & calf near Sector B. Water levels at Salt Lick are currently 72%.")
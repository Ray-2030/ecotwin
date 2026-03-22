import streamlit as st

# MUST BE FIRST
st.set_page_config(page_title="Sentinel Hub", layout="wide")

# EYE-FRIENDLY "FOREST DARK" THEME
st.markdown("""
<style>
    .stApp { background-color: #0B0E11; color: #D1D5DB; }
    [data-testid="stMetricValue"] { color: #4ADE80 !important; }
    .stButton>button { border: 1px solid #059669 !important; background: #064E3B !important; color: white !important; width: 100%; border-radius: 8px; height: 3.5em; }
    .stAlert { background-color: #111827 !important; border: 1px solid #374151 !important; color: #10B981 !important; }
</style>
""", unsafe_allow_html=True)

st.title("🛡️ Sentinel Alpha: Strategic Command")
st.write(f"Active Session: **Ranger {st.session_state.get('user', 'Wolf')}**")

# FEATURES: LIVE METRICS
col1, col2, col3, col4 = st.columns(4)
col1.metric("Elephant Corridors", "Active", "North")
col2.metric("Acoustic Sensors", "98%", "Online")
col3.metric("Poaching Threat", "Low", "-12%")
col4.metric("Ranger Vitals", "Stable", "72 BPM")

st.divider()

# FEATURES: MISSION CONTROL GRID
st.subheader("🚀 Tactical Operations")
c1, c2, c3 = st.columns(3)

with c1:
    if st.button("🗺️ Sightings Map"): st.switch_page("pages/5_Sightings_Map.py")
    if st.button("📓 Field Notes"): st.switch_page("pages/9_Field_Notes.py")

with c2:
    if st.button("🧬 Bio-Reports"): st.switch_page("pages/11_Generate_Report.py")
    if st.button("🎓 Ranger Academy"): st.switch_page("pages/14_Ranger_Academy.py")

with c3:
    if st.button("🏆 Leaderboard"): st.switch_page("pages/4_Leaderboard.py")
    if st.button("🛰️ Advanced Intel"): st.switch_page("pages/12_Advanced_Intel.py")

st.info("📡 **Status:** Drone fleet 04 detected a Black Rhino mother near Sector B. All systems green.")
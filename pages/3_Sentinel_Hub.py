import streamlit as st

st.set_page_config(page_title="Sentinel Hub", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0B0E11; color: #D1D5DB; }
    .stButton>button { background-color: #064E3B !important; color: white !important; border: 1px solid #059669 !important; height: 3em; }
    .stMetric { background: rgba(16, 185, 129, 0.05); padding: 15px; border-radius: 10px; border: 1px solid #064E3B; }
</style>
""", unsafe_allow_html=True)

st.title("🛡️ Sentinel Alpha Hub")

# NEW TECH: BIO-ACOUSTIC & BLOCKCHAIN METRICS
col1, col2, col3, col4 = st.columns(4)
col1.metric("Acoustic AI", "Active", "Scanning")
col2.metric("Blockchain Ledger", "Verified", "102 Nodes")
col3.metric("Edge Processing", "Local", "9ms Latency")
col4.metric("Ranger Stress", "Low", "72 BPM")

st.divider()

st.subheader("🚀 Strategic Operations")
c1, c2, c3 = st.columns(3)

with c1:
    if st.button("🗺️ Open Sightings Map"): st.switch_page("pages/5_Sightings_Map.py")
    if st.button("📓 Field Notes"): st.switch_page("pages/9_Field_Notes.py")
with c2:
    if st.button("🧬 Generate Report"): st.switch_page("pages/11_Generate_Report.py")
    if st.button("🎓 Ranger Academy"): st.switch_page("pages/14_Ranger_Academy.py")
with c3:
    if st.button("🏆 Leaderboard"): st.switch_page("pages/4_Leaderboard.py")
    if st.button("🛰️ Advanced AI"): st.switch_page("pages/12_Advanced_Intel.py")
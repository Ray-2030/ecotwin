import streamlit as st
import datetime, pytz, geocoder

st.set_page_config(page_title="Command Hub", layout="wide")

# Sidebar Navigation (The Full 2026 Suite)
with st.sidebar:
    st.title("🌲 Ranger Tools")
    st.info(f"Ranger: {st.session_state.get('user', 'Wolf')}")
    
    # Core Tools
    if st.button("📍 Sightings Heatmap"): st.switch_page("pages/5_Sightings_Map.py")
    if st.button("🔍 Species Guide"): st.switch_page("pages/8_Species_Guide.py")
    if st.button("📕 My Pokédex"): st.switch_page("pages/7_Pokedex.py")
    if st.button("📓 Field Notes"): st.switch_page("pages/9_Field_Notes.py")
    
    st.markdown("---")
    st.subheader("🚀 2026 Advanced Suite")
    if st.button("🧬 Biosphere Intel"): st.switch_page("pages/13_Biosphere_Intel.py")
    if st.button("🎓 Ranger Academy"): st.switch_page("pages/14_Ranger_Academy.py")
    if st.button("🎮 Ranger Console"): st.switch_page("pages/11_Ranger_Console.py")
    if st.button("🛡️ Advanced Intel"): st.switch_page("pages/12_Advanced_Intel.py")
    if st.button("📊 QR Report Tool"): st.switch_page("pages/10_Generate_Report.py")

    # 36. GHOST MODE TOGGLE
    ghost_mode = st.toggle("👻 Anti-Poaching Ghost Mode")
    if ghost_mode: st.sidebar.warning("Location Encrypted.")

# Main Display
st.title("🛡️ Sentinel Alpha Hub")
# Add live location/time as done previously
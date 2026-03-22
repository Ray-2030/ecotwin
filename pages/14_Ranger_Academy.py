import streamlit as st

st.set_page_config(page_title="Drone Command", layout="wide")

# Eye-Friendly Theme
st.markdown("""
<style>
    .stApp { background-color: #0B0E11; color: #D1D5DB; }
    .stVideo { border: 2px solid #059669; border-radius: 15px; }
</style>
""", unsafe_allow_html=True)

st.title("🚁 Drone 'Sentinel-X' Live Link")
st.markdown("---")

# --- FEATURES: DRONE UPLINK & DIAGNOSTICS ---
col1, col2 = st.columns([2, 1])

with col1:
    # Reliable, stable Vimeo wildlife clip
    st.video("https://vimeo.com/226343940") 
    st.caption("🔴 STABLE UPLINK: Sentinel Satellite 6 (Sector Mara)")

with col2:
    st.subheader("🕹️ Drone Dashboard")
    st.progress(85, text="🔋 Battery: 85%")
    st.write("**📡 Signal Strength:** 📶 98%")
    st.write("**🌡️ Thermal Sensors:** Online")
    st.write("**💨 Wind Speed:** 12 km/h")
    
    if st.button("🔄 Sync Flight Path"):
        st.toast("Uploading new vector to Sentinel-X...")
    
    st.divider()
    st.write("**🛰️ Satellite Metadata:**")
    st.code("Lat: -1.3521 | Lon: 34.9012\nAltitude: 450m MSL")

st.markdown("---")

# --- FEATURES: RANGER TRAINING ---
st.subheader("🎓 Field Skill Assessment")
skill = st.radio("Select a module to begin:", 
                 ["🐾 Track Identification", "🐘 Behavior Analysis", "🩹 Emergency First Aid"])

if st.button("Launch Training Module"):
    st.info(f"Initiating {skill} simulation... Please standby, Ranger Wolf.")

if st.button("⬅️ Return to Hub"):
    st.switch_page("pages/3_Sentinel_Hub.py")
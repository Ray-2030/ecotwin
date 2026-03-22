import streamlit as st

st.set_page_config(page_title="Drone Command", layout="wide")

st.title("🚁 Drone 'Sentinel-X' Live Link")
st.markdown("---")

# --- FEATURES 41-50: DRONE & TRAINING ---
col1, col2 = st.columns([2, 1])

with col1:
    # Using a high-quality Vimeo link (More stable for Streamlit)
    st.video("https://vimeo.com/226343940") 
    st.caption("🔴 STABLE UPLINK: Sentinel Satellite 6 (Sector Mara)")

with col2:
    st.subheader("🕹️ Drone Dashboard")
    st.progress(85, text="Battery: 85%")
    st.write("**Sensors:** Thermal, Acoustic, Lidar")
    st.write("**Wind Speed:** 12 km/h")
    if st.button("🔄 Sync Flight Path"): st.toast("New flight path uploaded.")

st.markdown("---")

st.subheader("🎓 Field Skill Assessment")
skill = st.radio("Choose a skill to test:", ["Track ID", "Behavior Analysis", "Emergency First Aid"])
if st.button("Begin Training Module"):
    st.write(f"Loading {skill} simulation... please standby.")

if st.button("⬅️ Return to Hub"):
    st.switch_page("pages/3_Sentinel_Hub.py")
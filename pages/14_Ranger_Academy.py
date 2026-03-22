import streamlit as st

st.set_page_config(page_title="Ranger Academy", page_icon="🎓", layout="wide")

st.title("🎓 Sentinel Academy & Drone Command")

st.info("🛰️ Encrypted Satellite Uplink Established. Ghost Mode Active.")

# Updated to a stable, high-quality wildlife drone video
st.subheader("🚁 Drone 'Sentinel-X' Live Link")
if st.button("🚀 Launch Surveillance Drone"):
    st.video("https://www.youtube.com/watch?v=306u9L_8x8A") 
    st.caption("🔴 LIVE FEED: High-Altitude Surveillance of the Savanna.")

st.markdown("---")

# Ranger Quiz Section
st.subheader("🧠 ID Challenge: Track Identification")
choice = st.radio("Identify this track:", ["Hyena", "Leopard", "Lion", "Cheetah"])
if st.button("Check Answer"):
    if choice == "Leopard":
        st.success("🎯 Correct! Leopard tracks show a distinct tri-lobed pad.")
        st.balloons()
    else:
        st.error("❌ Incorrect. Try again, Ranger.")

if st.button("⬅️ Return to Hub"):
    st.switch_page("pages/3_Sentinel_Hub.py")
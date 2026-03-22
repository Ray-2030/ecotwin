import streamlit as st

# --- PAGE SETUP ---
st.set_page_config(page_title="Ranger Academy", page_icon="🎓", layout="wide")

st.title("🎓 Sentinel Academy & Drone Command")
st.markdown("---")

# --- 33. DRONE LINK-UP (FIXED FEED) ---
st.subheader("🚁 Drone 'Sentinel-X' Live Link")
st.info("📡 Encrypted Satellite Uplink Established. Ghost Mode Active.")

# Replacing the Rickroll with a professional Wildlife Drone Simulation
# This ensures the WIEM 102 project remains academic and professional.
if st.button("🚀 Launch Surveillance Drone"):
    st.video("https://www.youtube.com/watch?v=7u8pS_MAszE") 
    st.caption("🔴 LIVE FEED: Surveillance Drone over North Mara Conservancy.")

st.markdown("---")

# --- 41. AI RANGER TRAINING QUIZ ---
st.subheader("🧠 ID Challenge: Track Identification")
st.write("Examine the pad shape and claw marks below.")
choice = st.radio("Identify this track:", ["Hyena", "Leopard", "Lion", "Cheetah"])

if st.button("Check Answer"):
    if choice == "Leopard":
        st.success("🎯 Correct! Leopard tracks show no retractable claw marks and a distinct tri-lobed pad.")
        st.balloons()
    else:
        st.error("❌ Incorrect. Hint: Look at the absence of claw marks which indicates a feline.")

st.markdown("---")

# --- 44. BIOMIMICRY & 45. ANCESTRAL KNOWLEDGE ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("💡 Biomimicry Insight")
    st.info("""
    **Aerodynamics:** Study the Cheetah's tail for better drone stabilization. 
    The tail acts as a rudder during high-speed maneuvers, a principle used in 2026 Agile-Drone tech.
    """)

with col2:
    st.subheader("📜 Ancestral Knowledge")
    with st.expander("View Traditional Wisdom"):
        st.write("""
        **Community Insight:** Local elders track the movement of the 'Chicas' (birds) 
        to predict localized weather changes and predator presence in the Rift Valley.
        """)

# --- NAVIGATION ---
if st.button("⬅️ Return to Hub"):
    st.switch_page("pages/3_Sentinel_Hub.py")
import streamlit as st
import google.generativeai as genai

# 🔒 SECURITY CHECK: Kick out users who aren't logged in
if "auth" not in st.session_state or not st.session_state.auth:
    st.warning("Please login at the Portal first.")
    if st.button("Go to Login"): st.switch_page("ecotwin_app.py")
    st.stop()

st.title(f"🌿 Sentinel Hub: Welcome, {st.session_state.user}")

# 🧬 AI CONFIGURATION
genai.configure(api_key=st.secrets["gemini"]["api_key"])
# Updated model to fix your 404/NotFound error
model = genai.GenerativeModel('gemini-2.0-flash') 

# 🏆 REWARDS SYSTEM
if "points" not in st.session_state: st.session_state.points = 0
st.sidebar.metric("Your Ranger Points", f"{st.session_state.points} 🟢")

# 📸 FIELD TOOLS
tab1, tab2 = st.tabs(["📷 Vision Scanner", "💬 Intel Query"])

with tab1:
    img = st.camera_input("Scan Wildlife")
    if img:
        with st.spinner("Analyzing Species..."):
            try:
                # Multimodal analysis (Image + Text)
                res = model.generate_content(["Identify this species. Is it endangered in Kenya? Give a brief ecology fact.", img])
                st.write(res.text)
                # Reward points if user finds something
                st.session_state.points += 10
                st.toast("Observation Logged! +10 Points")
            except Exception as e:
                st.error(f"Scanner Error: {e}")

with tab2:
    q = st.text_input("Ask Sentinel AI about Kenyan Wildlife:")
    if q:
        resp = model.generate_content(f"You are the Sentinel AI, an expert in Kenya's Wildlife Ecology. User asks: {q}")
        st.write(resp.text)

if st.sidebar.button("Log Out"):
    st.session_state.auth = False
    st.switch_page("ecotwin_app.py")
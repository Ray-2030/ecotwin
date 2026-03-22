import streamlit as st
import hashlib
from sqlalchemy import create_engine, text

st.set_page_config(page_title="Sentinel Alpha Portal", page_icon="🛡️", layout="centered")

# --- STEP 1: CYBER-SAFARI CSS THEME ---
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #0f2027, #203a43, #2c5364); color: white; }
    [data-testid="stSidebar"] { background-color: rgba(32, 58, 67, 0.9); border-right: 2px solid #00f2fe; }
    .stButton>button {
        background: linear-gradient(45deg, #2E7D32, #00f2fe);
        color: white; border-radius: 25px; border: none;
        padding: 10px 24px; font-weight: bold;
        box-shadow: 0 4px 15px rgba(0, 242, 254, 0.4);
    }
    .stTextInput>div>div>input { background-color: rgba(255,255,255,0.1); color: white; border: 1px solid #00f2fe; }
</style>
""", unsafe_allow_html=True)

# Branding
st.image("https://cdn-icons-png.flaticon.com/512/3062/3062250.png", width=80)
st.title("🛡️ Sentinel Alpha")

# Login Logic
with st.container(border=True):
    st.subheader("Ranger Authentication")
    u_in = st.text_input("Ranger ID")
    p_in = st.text_input("Security Key", type="password")
    
    if st.button("Unlock Portal", use_container_width=True):
        if u_in.lower() == "wolf" and p_in == "WolfAdmin@2026":
            st.session_state.auth = True
            st.session_state.user = "Wolf (Admin)"
            st.switch_page("pages/3_Sentinel_Hub.py")
        else:
            st.error("Access Denied.")
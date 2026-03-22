import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import google.generativeai as genai
import hashlib
from streamlit_js_eval import streamlit_js_eval
from datetime import datetime
import pytz

# --- 1. CORE CONFIG & AI ---
st.set_page_config(page_title="EcoTwin Sentinel Alpha", page_icon="🚨", layout="wide")

genai.configure(api_key=st.secrets["gemini"]["api_key"])
model = genai.GenerativeModel('gemini-1.5-flash') 

def get_engine():
    s = st.secrets["connections"]["postgresql"]
    return create_engine(
        f"postgresql://{s['username']}:{s['password']}@{s['host']}:{s['port']}/{s['database']}?sslmode=require",
        pool_pre_ping=True
    )

def hash_pw(pw):
    return hashlib.sha256(str.encode(pw)).hexdigest()

# --- 2. THE DYNAMIC THEME ENGINE ---
kenya_tz = pytz.timezone('Africa/Nairobi')
now = datetime.now(kenya_tz)

# Default Theme based on Time
if now.hour < 12: greeting, base_bg = "Good Morning", "#F0FFF0" # Honeydew
elif 12 <= now.hour < 18: greeting, base_bg = "Good Afternoon", "#FFF8E1" # Amber
else: greeting, base_bg = "Good Evening", "#E8EAF6" # Indigo

# Session State for the "Red Alert"
if "alert_active" not in st.session_state:
    st.session_state.alert_active = False

# Inject CSS for Background and the RED FLASH
alert_css = """
<style>
@keyframes flash {
    0% { background-color: #ff4d4d; }
    50% { background-color: #800000; }
    100% { background-color: #ff4d4d; }
}
.stApp {
    background-color: """ + (base_bg if not st.session_state.alert_active else "#ff4d4d") + """;
    """ + ("animation: flash 1s infinite;" if st.session_state.alert_active else "") + """
}
</style>
"""
st.markdown(alert_css, unsafe_allow_html=True)

# --- 3. AUTHENTICATION SYSTEM ---
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    t1, t2, t3 = st.tabs(["🔐 Login", "✨ Join Pride", "ℹ️ About"])
    
    with t1:
        st.subheader("Sentinel Login")
        # MASTER ADMIN: Wolf | Password: WolfAdmin@2026
        admin_h = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"
        u_in = st.text_input("Username", key="login_u")
        p_in = st.text_input("Password", type="password", key="login_p")
        
        if st.button("Unlock Portal", use_container_width=True):
            if u_in == "Wolf" and hash_pw(p_in) == admin_h:
                st.session_state.auth = True
                st.session_state.user = "Wolf (Admin)"
                st.rerun()
            else:
                try:
                    with get_engine().connect() as conn:
                        res = conn.execute(text("SELECT password FROM users WHERE username = :u"), {"u": u_in}).fetchone()
                        if res and res[0] == hash_pw(p_in):
                            st.session_state.auth = True
                            st.session_state.user = u_in
                            st.rerun()
                        else: st.error("Incorrect details.")
                except: st.error("Database connection busy. Try again.")

    with t2:
        st.subheader("Register New Ranger")
        reg_u = st.text_input("New Username")
        reg_p = st.text_input("New Password", type="password")
        if st.button("Confirm Registration"):
            if reg_u and reg_p:
                try:
                    with get_engine().begin() as conn:
                        conn.execute(text("INSERT INTO users (username, password) VALUES (:u, :p)"), 
                                     {"u": reg_u, "p": hash_pw(reg_p)})
                    st.success("Welcome to the Pride! Go to Login tab.")
                except: st.error("That name is taken. Try another!")
            else: st.warning("Fill in all fields.")
    
    with t3:
        st.header("Why EcoTwin?")
        st.write("The world's first agentic wildlife monitor built for Kenya. Secure, local, and powerful.")
    st.stop()

# --- 4. MAIN INTERFACE ---
st.title(f"🌿 {greeting}, {st.session_state.user}!")

# Reset Alert Button (if it gets stuck)
if st.session_state.alert_active:
    if st.button("🚨 DISMISS CRITICAL ALERT"):
        st.session_state.alert_active = False
        st.rerun()

st.sidebar.write(f"⏰ {now.strftime('%H:%M')} EAT")
if st.sidebar.button("Logout"):
    st.session_state.auth = False
    st.rerun()

# --- 5. THE AI FIELD EYE ---
c1, c2 = st.columns(2)
with c1:
    img = st.camera_input("Capture Species")
    loc = streamlit_js_eval(js_expressions='navigator.geolocation.getCurrentPosition(s => { return {lat: s.coords.latitude, lon: s.coords.longitude} })', target_flatten=True, key='geo')

with c2:
    q = st.text_input("Ask Sentinel AI:")
    if q:
        resp = model.generate_content(f"User in Kenya. Query: {q}")
        st.write(resp.text)

if img:
    with st.spinner("Analyzing threat levels..."):
        res = model.generate_content(["Check if this species is endangered. Identify it.", img])
        analysis = res.text
        st.markdown(analysis)
        
        # LOGIC: Flash Red if Endangered keywords found
        danger_keywords = ["endangered", "critical", "threatened", "illegal", "poaching"]
        if any(word in analysis.lower() for word in danger_keywords):
            st.session_state.alert_active = True
            st.error("🚨 CRITICAL ALERT: ENDANGERED SPECIES DETECTED")
            st.rerun()
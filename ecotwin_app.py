import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import google.generativeai as genai
import hashlib
from streamlit_js_eval import streamlit_js_eval
from datetime import datetime
import pytz

# --- 1. CORE SETTINGS ---
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

# --- 2. THEME & RED ALERT ENGINE ---
kenya_tz = pytz.timezone('Africa/Nairobi')
now = datetime.now(kenya_tz)

if "alert_active" not in st.session_state:
    st.session_state.alert_active = False

# Wallpaper changes by time of day
if now.hour < 12: bg = "#F0FFF0" # Morning
elif 12 <= now.hour < 18: bg = "#FFF8E1" # Afternoon
else: bg = "#E8EAF6" # Evening

st.markdown(f"""
<style>
@keyframes flash {{ 0% {{ background-color: #ff4d4d; }} 50% {{ background-color: #800000; }} 100% {{ background-color: #ff4d4d; }} }}
.stApp {{ background-color: {bg if not st.session_state.alert_active else "#ff4d4d"}; 
         {"animation: flash 1s infinite;" if st.session_state.alert_active else ""} }}
</style>
""", unsafe_allow_html=True)

# --- 3. FIX: BULLETPROOF AUTHENTICATION ---
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    t1, t2, t3 = st.tabs(["🔐 Login", "✨ Join Pride", "ℹ️ About"])
    
    with t1:
        st.subheader("Sentinel Login")
        # MASTER BYPASS: Wolf | Password: WolfAdmin@2026
        admin_h = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"
        u_in = st.text_input("Username", key="l_u")
        p_in = st.text_input("Password", type="password", key="l_p")
        
        if st.button("Unlock Portal", use_container_width=True):
            if u_in == "Wolf" and hash_pw(p_in) == admin_h:
                st.session_state.auth, st.session_state.user = True, "Wolf (Admin)"
                st.rerun()
            else:
                try:
                    with get_engine().connect() as conn:
                        res = conn.execute(text("SELECT password FROM users WHERE username = :u"), {"u": u_in}).fetchone()
                        if res and res[0] == hash_pw(p_in):
                            st.session_state.auth, st.session_state.user = True, u_in
                            st.rerun()
                        else: st.error("Access Denied. Check your typing.")
                except: st.error("Database is waking up... try once more.")

    with t2:
        st.subheader("New Ranger Registration")
        reg_u = st.text_input("Username Choice")
        reg_p = st.text_input("Password Choice", type="password")
        if st.button("Create Account"):
            if reg_u and reg_p:
                try:
                    with get_engine().begin() as conn:
                        conn.execute(text("INSERT INTO users (username, password) VALUES (:u, :p)"), {"u": reg_u, "p": hash_pw(reg_p)})
                    st.success("Welcome! Now switch to the Login tab.")
                except: st.error("Name taken! Try 'Ranger' + your name.")
    
    with t3:
        st.header("Sentinel Elite 2026")
        st.write("A global leader in agentic conservation technology.")
    st.stop()

# --- 4. MAIN HUB & LEADERBOARD ---
st.title(f"🌿 Welcome, {st.session_state.user}")
if st.session_state.alert_active:
    if st.button("🚨 DISMISS CRITICAL THREAT ALERT"):
        st.session_state.alert_active = False
        st.rerun()

st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"auth": False}))

# THE THREAT LEADERBOARD
with st.expander("📊 Global Threat Leaderboard (Kenya Hotspots)"):
    threat_data = pd.DataFrame({
        "Region (County)": ["Garissa", "Laikipia", "Tana River", "Kitui", "Marsabit"],
        "Top Threat Species": ["Hirola Antelope", "Grevy's Zebra", "Red Colobus", "Pancake Tortoise", "Elephant"],
        "Risk Level": ["CRITICAL", "HIGH", "CRITICAL", "HIGH", "MODERATE"],
        "Status": ["Population 245", "Stronghold", "Habitat Loss", "Recovery Plan", "Conflict Zone"]
    })
    st.table(threat_data)

# --- 5. AGENTIC AI & CAMERA ---
c1, c2 = st.columns(2)
with c1:
    img = st.camera_input("Field Scan")
    loc = streamlit_js_eval(js_expressions='navigator.geolocation.getCurrentPosition(s => { return {lat: s.coords.latitude, lon: s.coords.longitude} })', target_flatten=True, key='geo')

with c2:
    q = st.text_input("Ask Sentinel AI (e.g., 'Identify this animal'):")
    if q:
        resp = model.generate_content(f"User in Kenya. Query: {q}")
        st.write(resp.text)

if img:
    with st.spinner("Analyzing for endangered markers..."):
        res = model.generate_content(["Is this species endangered? Provide name and status.", img])
        analysis = res.text
        st.markdown(analysis)
        
        # Endangered species keywords triggers RED ALERT
        if any(w in analysis.lower() for w in ["endangered", "critical", "threatened", "hirola", "bongo"]):
            st.session_state.alert_active = True
            st.error("🚨 CRITICAL: ENDANGERED SPECIES DETECTED")
            st.rerun()
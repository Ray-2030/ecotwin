import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import google.generativeai as genai
import hashlib
from streamlit_js_eval import streamlit_js_eval
from datetime import datetime
import pytz

# --- 1. CORE CONFIG & STABLE AI ---
st.set_page_config(page_title="EcoTwin Sentinel Alpha", page_icon="🚨", layout="wide")

genai.configure(api_key=st.secrets["gemini"]["api_key"])
model = genai.GenerativeModel('gemini-1.5-flash') 

# FIX: Increased timeout and pre-ping to stop the "Waking Up" loop
def get_engine():
    s = st.secrets["connections"]["postgresql"]
    return create_engine(
        f"postgresql://{s['username']}:{s['password']}@{s['host']}:{s['port']}/{s['database']}?sslmode=require",
        pool_pre_ping=True, # Validates connection before use
        pool_recycle=300,    # Refreshes every 5 mins
        connect_args={'connect_timeout': 60} # Gives Aiven 60s to wake up
    )

def hash_pw(pw):
    return hashlib.sha256(str.encode(pw)).hexdigest()

# --- 2. THEME & RED ALERT ENGINE ---
if "ranger_points" not in st.session_state:
    st.session_state.ranger_points = 0
if "alert_active" not in st.session_state:
    st.session_state.alert_active = False

kenya_tz = pytz.timezone('Africa/Nairobi')
now = datetime.now(kenya_tz)

# Dynamic Wallpaper Logic
bg = "#F0FFF0" if now.hour < 12 else "#FFF8E1" if now.hour < 18 else "#E8EAF6"

st.markdown(f"""
<style>
@keyframes flash {{ 0% {{ background-color: #ff4d4d; }} 50% {{ background-color: #800000; }} 100% {{ background-color: #ff4d4d; }} }}
.stApp {{ background-color: {bg if not st.session_state.alert_active else "#ff4d4d"}; 
         {"animation: flash 1.5s infinite;" if st.session_state.alert_active else ""} }}
</style>
""", unsafe_allow_html=True)

# --- 3. FIX: BULLETPROOF AUTHENTICATION ---
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    t1, t2 = st.tabs(["🔐 Portal Login", "✨ Join the Pride"])
    
    with t1:
        st.subheader("Sentinel Login")
        # MASTER BYPASS: Username: Wolf | Password: WolfAdmin@2026
        admin_h = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"
        u_in = st.text_input("Username", key="l_u").strip()
        p_in = st.text_input("Password", type="password", key="l_p").strip()
        
        if st.button("Unlock Portal", use_container_width=True):
            if u_in.lower() == "wolf" and hash_pw(p_in) == admin_h:
                st.session_state.auth, st.session_state.user = True, "Wolf (Admin)"
                st.rerun()
            else:
                try:
                    with get_engine().connect() as conn:
                        res = conn.execute(text("SELECT password FROM users WHERE username = :u"), {"u": u_in}).fetchone()
                        if res and res[0] == hash_pw(p_in):
                            st.session_state.auth, st.session_state.user = True, u_in
                            st.rerun()
                        else: st.error("Access Denied. Please check your spelling.")
                except Exception:
                    st.error("Database is waking up... Please wait 15 seconds and try again.")

    with t2:
        st.subheader("New Ranger Registration")
        reg_u = st.text_input("Username Choice").strip()
        reg_p = st.text_input("Password Choice", type="password").strip()
        if st.button("Create Account"):
            if reg_u and reg_p:
                try:
                    with get_engine().begin() as conn:
                        conn.execute(text("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)"))
                        conn.execute(text("INSERT INTO users (username, password) VALUES (:u, :p)"), {"u": reg_u, "p": hash_pw(reg_p)})
                    st.success(f"Welcome Ranger {reg_u}! Now switch to the Login tab.")
                except:
                    st.warning("This name is already registered. If you forgot your password, please contact Admin Wolf.")
            else: st.warning("Please fill in both fields.")
    st.stop()

# --- 4. RANGER HUB & REWARDS ---
st.title(f"🌿 Welcome, Ranger {st.session_state.user}")

# Reward Tier Logic
rank = "Scout" if st.session_state.ranger_points < 50 else "Guardian" if st.session_state.ranger_points < 150 else "Elite Sentinel"
st.sidebar.metric("Conservation Points", f"{st.session_state.ranger_points} pts")
st.sidebar.write(f"**Current Rank:** {rank}")
st.sidebar.progress(min(st.session_state.ranger_points / 200, 1.0))

if st.session_state.alert_active:
    if st.button("🚨 DISMISS THREAT ALERT"):
        st.session_state.alert_active = False
        st.rerun()

# --- 5. FIELD TOOLS ---
c1, c2 = st.columns(2)
with c1:
    img = st.camera_input("Field Observation")
    loc = streamlit_js_eval(js_expressions='navigator.geolocation.getCurrentPosition(s => { return {lat: s.coords.latitude, lon: s.coords.longitude} })', target_flatten=True, key='geo')

with c2:
    q = st.text_input("Consult Sentinel Intelligence:")
    if q:
        with st.spinner("AI thinking..."):
            resp = model.generate_content(f"User in Kenya. Local Time: {now}. Query: {q}")
            st.write(resp.text)

if img:
    with st.spinner("Analyzing threat levels..."):
        res = model.generate_content(["Identify this species and check if it is endangered.", img])
        analysis = res.text
        st.markdown(analysis)
        
        # Reward & Alert Logic
        if any(w in analysis.lower() for w in ["endangered", "critical", "threatened", "hirola", "rhino", "leopard"]):
            st.session_state.alert_active = True
            st.session_state.ranger_points += 25
            st.toast("🏆 +25 Points: Critical Observation Logged!")
            st.rerun()
        else:
            st.session_state.ranger_points += 5
            st.toast("✅ +5 Points: Species Observation Logged.")

st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"auth": False}))
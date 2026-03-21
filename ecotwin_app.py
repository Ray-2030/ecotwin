import streamlit as st
import pandas as pd
import pydeck as pdk
from sqlalchemy import create_engine, text
import google.generativeai as genai
import hashlib
from streamlit_js_eval import streamlit_js_eval
from datetime import datetime
import io

# --- 1. CORE CONFIGURATION ---
st.set_page_config(page_title="EcoTwin Sentinel", page_icon="🌿", layout="wide")

# AI Setup: Using Gemini 3 Flash for high-speed 2026 multimodal reasoning
genai.configure(api_key=st.secrets["gemini"]["api_key"])
model = genai.GenerativeModel('gemini-1.5-flash') 

def get_engine():
    s = st.secrets["connections"]["postgresql"]
    return create_engine(f"postgresql://{s['username']}:{s['password']}@{s['host']}:{s['port']}/{s['database']}?sslmode=require")

# --- 2. DATABASE AUTO-REPAIR ---
# This bypasses Aiven's web interface errors by fixing the DB via code
def auto_repair_db():
    engine = get_engine()
    with engine.begin() as conn:
        # Create users table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password TEXT NOT NULL
            );
        """))
        
        # Create eco_logs table if missing
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS eco_logs (
                id SERIAL PRIMARY KEY,
                recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                temperature_c FLOAT,
                soil_moisture_pct FLOAT,
                lux FLOAT,
                lat FLOAT,
                lon FLOAT,
                notes TEXT
            );
        """))
        
        # Add 'Wolf' user (Password: wolf2026)
        wolf_hash = hashlib.sha256("wolf2026".encode()).hexdigest()
        conn.execute(text("""
            INSERT INTO users (username, password) 
            VALUES ('Wolf', :hpw) 
            ON CONFLICT (username) DO NOTHING;
        """), {"hpw": wolf_hash})

# Run repair on startup
try:
    auto_repair_db()
except Exception as e:
    st.error(f"Database Syncing... {e}")

# --- 3. AUTHENTICATION ---
def hash_pw(pw):
    return hashlib.sha256(str.encode(pw)).hexdigest()

if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    # Centered Login UI with Logo
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        try:
            st.image("logo.png", use_container_width=True)
        except:
            st.warning("Logo file missing. Please upload logo.png to GitHub.")
        
        st.title("🔐 Sentinel Portal")
        st.markdown("### Wildlife Monitoring • Kenya 2026")
        
        user_input = st.text_input("Username")
        pw_input = st.text_input("Password", type="password")
        
        if st.button("Authorize Access", use_container_width=True):
            engine = get_engine()
            with engine.connect() as conn:
                query = text("SELECT password FROM users WHERE username = :u")
                res = conn.execute(query, {"u": user_input}).fetchone()
                if res and res[0] == hash_pw(pw_input):
                    st.session_state.auth = True
                    st.session_state.user = user_input
                    st.success("Access Granted!")
                    st.rerun()
                else:
                    st.error("Invalid Credentials.")
    st.stop()

# --- 4. MAIN DASHBOARD (After Login) ---
st.title("🌿 EcoTwin Field Sentinel")
st.sidebar.title(f"👤 {st.session_state.user}")

# Grab GPS Location from Browser
loc = streamlit_js_eval(js_expressions='navigator.geolocation.getCurrentPosition(s => { return {lat: s.coords.latitude, lon: s.coords.longitude} })', target_flatten=True, key='geo')

# --- 5. PROFESSIONAL SATELLITE GIS ---
st.subheader("🗺️ Kenya Observation Network")
try:
    engine = get_engine()
    df = pd.read_sql("SELECT lat, lon, notes, recorded_at FROM eco_logs WHERE lat IS NOT NULL", engine)
    
    # Focus map on Kenya
    view_state = pdk.ViewState(latitude=-1.28, longitude=36.82, zoom=6, pitch=40)
    
    # Red dots for tagged field observations
    layer = pdk.Layer(
        "ScatterplotLayer",
        df,
        get_position='[lon, lat]',
        get_color='[200, 30, 30, 160]',
        get_radius=7000,
        pickable=True
    )

    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/satellite-streets-v12',
        initial_view_state=view_state,
        layers=[layer],
        tooltip={"text": "Observation: {notes}\nDate: {recorded_at}"}
    ))
except Exception as e:
    st.info("Mapping system active. Log your first GPS tag to see pins.")

# --- 6. MULTILINGUAL VIDEO AI ---
st.markdown("---")
st.subheader("🎥 AI Field Diagnostic (Video)")
lang = st.radio("Response Language:", ["English", "Swahili", "Japanese"], horizontal=True)
vid_file = st.file_uploader("Upload video of garden/wildlife issue", type=["mp4", "mov"])

if vid_file:
    with st.spinner(f"Analyzing in {lang}..."):
        # Process video for immediate ecological troubleshooting
        response = model.generate_content([
            f"Identify any issues in this video related to plant health, animal behavior, or ecology. Provide solutions in {lang}.",
            {"mime_type": "video/mp4", "data": vid_file.getvalue()}
        ])
        st.success(response.text)

# --- 7. SIDEBAR FIELD TOOLS ---
with st.sidebar:
    st.markdown("---")
    st.header("📍 GIS Tagging")
    field_notes = st.text_area("Observation Details")
    
    if st.button("🛰️ Sync GPS to Cloud"):
        if loc and 'lat' in loc:
            try:
                with get_engine().begin() as conn:
                    conn.execute(text("INSERT INTO eco_logs (lat, lon, notes) VALUES (:la, :lo, :n)"), 
                                 {"la": loc['lat'], "lo": loc['lon'], "n": field_notes})
                st.success("Tagged to Global Map!")
                st.balloons()
            except Exception as e:
                st.error(f"Sync failed: {e}")
        else:
            st.warning("Waiting for GPS signal...")

    if st.button("Logout"):
        st.session_state.auth = False
        st.rerun()
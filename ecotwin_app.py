import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import google.generativeai as genai
from PIL import Image
from streamlit_js_eval import streamlit_js_eval
from datetime import datetime

# --- 1. DATABASE SETUP & AUTO-FIX ---
def get_engine():
    user = st.secrets["connections"]["postgresql"]["username"]
    pw = st.secrets["connections"]["postgresql"]["password"]
    host = st.secrets["connections"]["postgresql"]["host"]
    port = st.secrets["connections"]["postgresql"]["port"]
    db = st.secrets["connections"]["postgresql"]["database"]
    db_url = f"postgresql://{user}:{pw}@{host}:{port}/{db}?sslmode=require"
    return create_engine(db_url)

def init_db():
    """Automatically creates the lat, lon, and lux columns if they are missing."""
    engine = get_engine()
    with engine.begin() as conn:
        for col in ["lux", "lat", "lon"]:
            try:
                conn.execute(text(f"ALTER TABLE eco_logs ADD COLUMN {col} FLOAT;"))
            except Exception:
                pass # Skips if column already exists

# Run the fix once when the app starts
init_db()

# --- 2. AI SETUP ---
# Updated to 2.5 Flash for better performance and 2026 quota limits
genai.configure(api_key=st.secrets["gemini"]["api_key"])
model = genai.GenerativeModel('gemini-2.5-flash')

# --- 3. APP UI & GPS ---
st.set_page_config(page_title="EcoTwin Field Patrol", page_icon="🌍", layout="wide")
# Requests GPS from your iPhone or Samsung
location = streamlit_js_eval(js_expressions='navigator.geolocation.getCurrentPosition(success => { return {lat: success.coords.latitude, lon: success.coords.longitude} })', target_flatten=True, key='geo')

st.title("🌍 EcoTwin Field Patrol")
st.caption(f"Wildlife Ecology GIS Dashboard • {datetime.now().strftime('%Y')}")

# --- 4. SIDEBAR: DATA ENTRY ---
with st.sidebar:
    st.header("📋 Field Observations")
    # Values from your Physics Toolbox Sensor Suite
    lux = st.number_input("Light Intensity (Lux)", min_value=0.0, value=500.0)
    temp = st.number_input("Air Temp (°C)", value=25.0)
    soil = st.slider("Soil Moisture (%)", 0, 100, 30)
    
    if location:
        st.success(f"📍 GPS Locked: {round(location['lat'], 4)}, {round(location['lon'], 4)}")
    else:
        st.warning("📍 Waiting for GPS... (Check phone permissions)")

    if st.button("🛰️ Sync Field Patrol to Cloud"):
        if location:
            try:
                engine = get_engine()
                with engine.begin() as conn:
                    query = text("INSERT INTO eco_logs (temperature_c, soil_moisture_pct, lux, lat, lon) VALUES (:t, :s, :l, :lat, :lon)")
                    conn.execute(query, {"t": temp, "s": soil, "l": lux, "lat": location['lat'], "lon": location['lon']})
                st.success("✅ Patrol Synced!")
                st.balloons()
            except Exception as e:
                st.error(f"Sync Error: {e}")
        else:
            st.error("Enable location access to save coordinates!")

# --- 5. MAIN DASHBOARD ---
try:
    engine = get_engine()
    df = pd.read_sql("SELECT * FROM eco_logs ORDER BY recorded_at DESC LIMIT 100", engine)
    
    if not df.empty:
        st.subheader("🗺️ Sample Site Mapping")
        # Only maps points that have actual coordinates
        if 'lat' in df.columns and 'lon' in df.columns:
            map_data = df.dropna(subset=['lat', 'lon'])
            if not map_data.empty:
                st.map(map_data[['lat', 'lon']])
        
        st.markdown("---")
        st.subheader("📸 Visual Soil Scan")
        img_file = st.file_uploader("Upload soil photo", type=["jpg", "png"])
        if img_file:
            img = Image.open(img_file)
            st.image(img, width=300)
            if st.button("Run AI Soil Diagnostics"):
                res = model.generate_content(["As an ecology expert, analyze this soil moisture/texture.", img])
                st.info(res.text)
except Exception as e:
    st.error(f"Dashboard Error: {e}")
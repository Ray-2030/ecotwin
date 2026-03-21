import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import google.generativeai as genai
from PIL import Image
from streamlit_js_eval import streamlit_js_eval
from datetime import datetime

# --- 1. DATABASE SETUP ---
def get_engine():
    user = st.secrets["connections"]["postgresql"]["username"]
    pw = st.secrets["connections"]["postgresql"]["password"]
    host = st.secrets["connections"]["postgresql"]["host"]
    port = st.secrets["connections"]["postgresql"]["port"]
    db = st.secrets["connections"]["postgresql"]["database"]
    db_url = f"postgresql://{user}:{pw}@{host}:{port}/{db}?sslmode=require"
    return create_engine(db_url)

def init_db():
    """Automatically adds missing columns to bypass Aiven website errors."""
    engine = get_engine()
    with engine.begin() as conn:
        for col in ["lux", "lat", "lon"]:
            try:
                conn.execute(text(f"ALTER TABLE eco_logs ADD COLUMN {col} FLOAT;"))
            except Exception:
                pass 

init_db()

# --- 2. 2026 AI UPGRADE (Fixes 404 Error) ---
# Gemini 1.5 is retired. We are now using the stable Gemini 3 series.
genai.configure(api_key=st.secrets["gemini"]["api_key"])
model = genai.GenerativeModel('gemini-3-flash-preview')

# --- 3. GPS GEOLOCATION (Permission Booster) ---
st.set_page_config(page_title="EcoTwin Field Patrol", page_icon="🌍", layout="wide")

# High-accuracy mode helps mobile browsers (Chrome/Safari) lock GPS faster
location = streamlit_js_eval(
    js_expressions='navigator.geolocation.getCurrentPosition(s => { return {lat: s.coords.latitude, lon: s.coords.longitude} }, e => { return {error: e.message} }, {enableHighAccuracy: true, timeout: 15000})', 
    target_flatten=True, 
    key='geo'
)

st.title("🌍 EcoTwin Field Patrol")
st.caption(f"Wildlife Ecology GIS Dashboard • {datetime.now().strftime('%Y')}")

# --- 4. SIDEBAR: DATA ENTRY ---
with st.sidebar:
    st.header("📋 Field Observations")
    lux = st.number_input("Light Intensity (Lux)", min_value=0.0, value=500.0)
    temp = st.number_input("Air Temp (°C)", value=25.0)
    soil = st.slider("Soil Moisture (%)", 0, 100, 30)
    
    if location and 'lat' in location:
        st.success(f"📍 GPS Locked: {round(location['lat'], 4)}, {round(location['lon'], 4)}")
    elif location and 'error' in location:
        st.error(f"📍 GPS Timeout. Please refresh and 'Allow' location.")
    else:
        st.warning("📍 Waiting for GPS... (Check phone permissions)")

    if st.button("🛰️ Sync to Cloud"):
        if location and 'lat' in location:
            try:
                engine = get_engine()
                with engine.begin() as conn:
                    query = text("INSERT INTO eco_logs (temperature_c, soil_moisture_pct, lux, lat, lon) VALUES (:t, :s, :l, :lat, :lon)")
                    conn.execute(query, {"t": temp, "s": soil, "l": lux, "lat": location['lat'], "lon": location['lon']})
                st.success("Patrol Synced!")
                st.balloons()
            except Exception as e:
                st.error(f"Sync failed: {e}")

# --- 5. MAIN DASHBOARD ---
try:
    engine = get_engine()
    df = pd.read_sql("SELECT * FROM eco_logs ORDER BY recorded_at DESC LIMIT 100", engine)
    
    if not df.empty:
        # GIS MAPPING
        st.subheader("🗺️ Sample Site Mapping")
        if 'lat' in df.columns and 'lon' in df.columns:
            st.map(df.dropna(subset=['lat', 'lon'])[['lat', 'lon']])
        
        st.markdown("---")
        
        # --- 6. UNLIMITED AI CHAT & SUGGESTIONS ---
        st.subheader("🤖 EcoTwin AI Assistant")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Visual Soil Analyzer**")
            img_file = st.file_uploader("Upload/Take Photo", type=["jpg", "png"])
            if img_file:
                img = Image.open(img_file)
                st.image(img, width=300)
                if st.button("Run AI Diagnostics"):
                    # This allows the AI to analyze the photo and give ecology advice
                    res = model.generate_content(["Act as a wildlife ecologist. Analyze this soil photo and provide 3 management suggestions.", img])
                    st.info(res.text)
        
        with col2:
            st.write("**Universal Ecology Chat**")
            user_msg = st.text_input("Ask any question or request suggestions:")
            if user_msg:
                # We feed the AI your current data so it gives SMART suggestions
                latest = df.iloc[0]
                context = f"Current site: {latest['temperature_c']}°C, {latest['soil_moisture_pct']}% moisture."
                res = model.generate_content(f"Answer this: {user_msg}. Also, give 2 suggestions based on: {context}")
                st.write(res.text)

except Exception as e:
    st.error(f"Error loading data: {e}")
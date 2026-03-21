import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import google.generativeai as genai
from PIL import Image
from streamlit_js_eval import streamlit_js_eval
from datetime import datetime

# --- 1. DATABASE & AUTO-REPAIR ---
def get_engine():
    user = st.secrets["connections"]["postgresql"]["username"]
    pw = st.secrets["connections"]["postgresql"]["password"]
    host = st.secrets["connections"]["postgresql"]["host"]
    port = st.secrets["connections"]["postgresql"]["port"]
    db = st.secrets["connections"]["postgresql"]["database"]
    db_url = f"postgresql://{user}:{pw}@{host}:{port}/{db}?sslmode=require"
    return create_engine(db_url)

def init_db():
    """Forces the database to create columns if Aiven console is giving errors."""
    engine = get_engine()
    with engine.begin() as conn:
        for col in ["lux", "lat", "lon"]:
            try:
                conn.execute(text(f"ALTER TABLE eco_logs ADD COLUMN {col} FLOAT;"))
            except Exception:
                pass 

init_db()

# --- 2. THE 2026 AI UPGRADE (Fixes 404 Error) ---
# We are moving to 2.0-flash because 1.5 was deprecated for new projects
genai.configure(api_key=st.secrets["gemini"]["api_key"])
model = genai.GenerativeModel('gemini-2.0-flash')

# --- 3. GPS GEOLOCATION (With Permission Booster) ---
st.set_page_config(page_title="EcoTwin Field Patrol", page_icon="🌍", layout="wide")

# This is the "booster" - it asks the browser more aggressively for the location
location = streamlit_js_eval(
    js_expressions='navigator.geolocation.getCurrentPosition(s => { return {lat: s.coords.latitude, lon: s.coords.longitude} }, e => { return {error: e.message} }, {enableHighAccuracy: true, timeout: 10000})', 
    target_flatten=True, 
    key='geo'
)

st.title("🌍 EcoTwin Field Patrol")
st.caption(f"Wildlife Ecology GIS Project • {datetime.now().strftime('%Y')}")

# --- 4. SIDEBAR: DATA ENTRY ---
with st.sidebar:
    st.header("📋 Field Observations")
    st.info("Reading from: Physics Toolbox Sensor Suite")
    
    lux = st.number_input("Light Intensity (Lux)", min_value=0.0, value=500.0)
    temp = st.number_input("Air Temp (°C)", value=25.0)
    soil = st.slider("Soil Moisture (%)", 0, 100, 30)
    
    # GPS Status Check
    if location and 'lat' in location:
        st.success(f"📍 GPS Locked: {round(location['lat'], 4)}, {round(location['lon'], 4)}")
    elif location and 'error' in location:
        st.error(f"📍 GPS Error: {location['error']}. Check phone settings!")
    else:
        st.warning("📍 Waiting for GPS... (Tap 'Allow' on your phone)")

    if st.button("🛰️ Sync Field Patrol to Cloud"):
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
        else:
            st.error("Cannot sync without GPS coordinates.")

# --- 5. MAIN DASHBOARD ---
try:
    engine = get_engine()
    df = pd.read_sql("SELECT * FROM eco_logs ORDER BY recorded_at DESC LIMIT 100", engine)
    
    if not df.empty:
        # MAP VIEW
        st.subheader("🗺️ Sample Site Mapping (GIS)")
        if 'lat' in df.columns and 'lon' in df.columns:
            st.map(df.dropna(subset=['lat', 'lon'])[['lat', 'lon']])
        
        st.markdown("---")
        
        # --- 6. SMART AI CHAT & SUGGESTIONS ---
        st.subheader("🤖 EcoTwin AI Assistant")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Visual Soil Analyzer**")
            img_file = st.file_uploader("Take/Upload soil photo", type=["jpg", "png"])
            if img_file:
                img = Image.open(img_file)
                st.image(img, width=300)
                if st.button("Analyze Photo"):
                    # Multimodal prompt: Image + Text
                    res = model.generate_content(["Analyze this soil moisture/health and give 3 wildlife ecology suggestions.", img])
                    st.info(res.text)
        
        with col2:
            st.write("**General Ecology Chat**")
            user_msg = st.text_input("Ask any question or get suggestions:")
            if user_msg:
                # We feed the AI your current data so it gives specific suggestions
                latest = df.iloc[0]
                context_prompt = f"""
                User Question: {user_msg}
                Context: Current temp is {latest['temperature_c']}°C and soil moisture is {latest['soil_moisture_pct']}%.
                Answer the question and provide 2 eco-suggestions based on these values.
                """
                res = model.generate_content(context_prompt)
                st.write(res.text)

except Exception as e:
    st.error(f"Dashboard error: {e}")
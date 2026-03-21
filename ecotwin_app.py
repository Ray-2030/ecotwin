import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import google.generativeai as genai
from PIL import Image
from streamlit_js_eval import streamlit_js_eval
from datetime import datetime

# --- 1. DATABASE SETUP & AUTO-FIX (2026 Standardization) ---
def get_engine():
    """Builds a secure connection string to your Aiven database."""
    user = st.secrets["connections"]["postgresql"]["username"]
    pw = st.secrets["connections"]["postgresql"]["password"]
    host = st.secrets["connections"]["postgresql"]["host"]
    port = st.secrets["connections"]["postgresql"]["port"]
    db = st.secrets["connections"]["postgresql"]["database"]
    db_url = f"postgresql://{user}:{pw}@{host}:{port}/{db}?sslmode=require"
    return create_engine(db_url)

def init_db():
    """Automatically synchronizes database schema to support 2026 mapping features."""
    engine = get_engine()
    with engine.begin() as conn:
        for col in ["lux", "lat", "lon"]:
            try:
                # Forces new columns to existence without needing Aiven's website
                conn.execute(text(f"ALTER TABLE eco_logs ADD COLUMN {col} FLOAT;"))
            except Exception:
                pass # Skips if column is already present

init_db() # Ensures database columns are ready for field data

# --- 2. THE 2026 AI UPGRADE (Fixes 403 and 429 Errors) ---
# Crucial change: Replaced gemini-2.0-flash (unstable tier) with gemini-1.5-flash.
# This model has the best stability for image/text free-tier access in 2026.
genai.configure(api_key=st.secrets["gemini"]["api_key"])
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 3. APP UI & SMART Field GPS ---
st.set_page_config(page_title="EcoTwin Field Patrol GIS", page_icon="🌍", layout="wide")

# This component requests GPS coordinates directly from your phone's browser (Safari/Chrome).
# You must accept the location permission on your device!
location = streamlit_js_eval(js_expressions='navigator.geolocation.getCurrentPosition(success => { return {lat: success.coords.latitude, lon: success.coords.longitude} })', target_flatten=True, key='geo')

st.title("🌍 EcoTwin Field Patrol")
st.caption(f"Wildlife Ecology GIS Dashboard • {datetime.now().strftime('%Y')} Project")

# --- 4. SIDEBAR: The "Manual-Smart" Field Journal ---
with st.sidebar:
    st.header("📋 Field Patrol Journal")
    st.write("Enter readings from your *Physics Toolbox Sensor Suite* app.")
    
    lux = st.number_input("Light Intensity (Lux)", min_value=0.0, value=500.0, step=10.0)
    temp = st.number_input("Air Temperature (°C)", value=25.0, step=0.1)
    # Manual estimate is fine when visual scanning
    soil = st.slider("Manual Soil Estimate (%)", 0, 100, 30)
    
    # Visual validation for the Field Marshall
    if location:
        st.success(f"📍 GPS coordinates locked and verified.")
    else:
        # Check permissions on phone if this is stuck on yellow warning
        st.warning("📍 Waiting for GPS location from browser...")

    if st.button("🛰️ Sync Field Patrol to Cloud"):
        # We enforce GPS lock as a requirement for any ecological survey sync
        if location:
            try:
                engine = get_engine()
                with engine.begin() as conn:
                    query = text("INSERT INTO eco_logs (temperature_c, soil_moisture_pct, lux, lat, lon) VALUES (:t, :s, :l, :lat, :lon)")
                    conn.execute(query, {"t": temp, "s": soil, "l": lux, "lat": location['lat'], "lon": location['lon']})
                st.success("✅ GPS-tagged observation saved to Aiven cloud!")
                st.balloons()
            except Exception as e:
                st.error(f"Sync failed: {e}")
        else:
            st.error("Error: GPS coordinate lock required for standard ecological surveys. Enable location permissions.")

# --- 5. MAIN DASHBOARD: The Wildlife GIS Map ---
try:
    engine = get_engine()
    df = pd.read_sql("SELECT * FROM eco_logs ORDER BY recorded_at DESC LIMIT 100", engine)
    
    if not df.empty:
        st.subheader("🗺️ Spatiotemporal Ecology Map")
        st.caption("Each point represents a timestamped GPS-tagged observation in the study area.")
        # Ensure the table columns now exist and are populated to render the map
        if 'lat' in df.columns and 'lon' in df.columns:
            # Drop entries without location data to avoid map rendering errors
            st.map(df.dropna(subset=['lat', 'lon'])[['lat', 'lon']])
        
        st.markdown("---")
        
        # --- 6. AI & MULTIMODAL DIAGNOSTICS SECTION ---
        # The AI options are integrated here into two powerful tools.
        st.subheader("🤖 Multimodal AI & Field Diagnostics")
        
        analysis_cols = st.columns(2)
        
        with analysis_cols[0]:
            st.write("**Visual Soil Scanner (multimodal):**")
            st.caption("Upload soil samples from your phone's camera.")
            img_file = st.file_uploader("Capture or upload soil photo", type=["jpg", "jpeg", "png"], key="soil_scan")
            
            if img_file:
                img = Image.open(img_file)
                st.image(img, caption="Field Sample", width=300)
                
                if st.button("Analyze Soil Health (gemini-1.5)"):
                    with st.spinner("Executing multimodal diagnostics..."):
                        # Custom multimodal prompt instructions
                        prompt = """
                        As an experienced Wildlife Ecology consultant, execute the following from this field image:
                        1. Estimate soil moisture percentage based on color saturation and texture.
                        2. Identify dominant soil type (Sandy, Loamy, Clay).
                        3. Based on the appearance, provide one ecological suggestion for maximizing plant health in this specific ground composition.
                        """
                        try:
                            # Sends text prompt + image concurrently
                            response = model.generate_content([prompt, img])
                            st.success("Analysis Complete")
                            st.info(response.text)
                        except Exception as e:
                            st.error(f"Visual Diagnosis Error: {e}. (Verify API status)")

        with analysis_cols[1]:
            st.write("**Ecology General Question (text-only):**")
            st.caption("Ask ANY question about your environment or ecology assignment.")
            user_query = st.text_input("Ask Gemini standard ecology questions...")

            if user_query:
                with st.spinner("Consulting Gemini knowledge base..."):
                    try:
                        # Contextualize standard queries with the latest field data.
                        # This enables Gemini to offer personalized suggestions.
                        latest = df.iloc[0]
                        context = f"The current site reading is Air Temp {latest['temperature_c']}°C, Soil Moisture {latest['soil_moisture_pct']}%."
                        
                        custom_prompt = f"""
                        {user_query}. Please incorporate the following environmental data into your response and offer any ecological management suggestions if the conditions look suboptimal: {context}
                        """
                        
                        response = model.generate_content(custom_prompt)
                        st.info(response.text)
                    except Exception as ai_err:
                        st.error(f"AI Quota Issue: {ai_err}. (Try again in 60 seconds)")

        st.markdown("---")
        with st.expander("📂 Field Study Data Log"):
            st.dataframe(df.dropna(subset=['lat', 'lon']), use_container_width=True)
except Exception as e:
    st.error(f"Critical Dashboard Error: {e}. (Verify database connection)")
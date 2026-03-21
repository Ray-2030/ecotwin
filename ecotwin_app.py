import streamlit as st
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import google.generativeai as genai
from datetime import datetime

# --- 1. DATABASE & AI SETUP ---
def get_engine():
    user = st.secrets["connections"]["postgresql"]["username"]
    pw = st.secrets["connections"]["postgresql"]["password"]
    host = st.secrets["connections"]["postgresql"]["host"]
    port = st.secrets["connections"]["postgresql"]["port"]
    db = st.secrets["connections"]["postgresql"]["database"]
    db_url = f"postgresql://{user}:{pw}@{host}:{port}/{db}?sslmode=require"
    return create_engine(db_url)

# Setup Gemini AI - Updated to 1.5-flash to fix 404 error
genai.configure(api_key=st.secrets["gemini"]["api_key"])
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 2. APP LAYOUT ---
st.set_page_config(page_title="EcoTwin AI Dashboard", page_icon="🌿", layout="wide")
st.title("🌿 EcoTwin AI Cloud Monitoring")
st.caption("Wildlife Ecology & Management - Digital Twin Project")

# --- 3. SIDEBAR: DATA ENTRY ---
with st.sidebar:
    st.header("📍 Field Data Entry")
    temp = st.number_input("Temp (°C)", value=24.5, step=0.1)
    hum = st.number_input("Humidity (%)", value=58.0, step=0.1)
    soil = st.number_input("Soil Moisture (%)", value=40.0, step=0.1)
    
    if st.button("Push to Aiven Cloud"):
        try:
            engine = get_engine()
            with engine.begin() as conn:
                # Use text() or proper parameters for SQLAlchemy connection
                from sqlalchemy import text
                query = text("INSERT INTO eco_logs (temperature_c, humidity_pct, soil_moisture_pct) VALUES (:t, :h, :s)")
                conn.execute(query, {"t": temp, "h": hum, "s": soil})
            st.success("✅ Saved to Cloud!")
            st.balloons()
        except Exception as e:
            st.error(f"Sync Failed: {e}")

# --- 4. MAIN DASHBOARD: VISUALS ---
try:
    engine = get_engine()
    df = pd.read_sql("SELECT recorded_at, temperature_c, humidity_pct, soil_moisture_pct FROM eco_logs ORDER BY recorded_at DESC LIMIT 50", engine)
    
    if not df.empty:
        # Metrics
        m1, m2, m3 = st.columns(3)
        latest = df.iloc[0]
        m1.metric("Current Temp", f"{latest['temperature_c']}°C")
        m2.metric("Humidity", f"{latest['humidity_pct']}%")
        m3.metric("Soil Moisture", f"{latest['soil_moisture_pct']}%")
        
        # Charts
        st.subheader("Ecological Trends")
        st.line_chart(df.set_index('recorded_at')[['temperature_c', 'humidity_pct', 'soil_moisture_pct']])
        
        # --- 5. AI ASSISTANT SECTION ---
        st.markdown("---")
        st.subheader("🤖 Chat with EcoTwin AI")
        user_query = st.text_input("Ask about your garden (e.g., 'Is my soil too dry?')")

        if user_query:
            with st.spinner("Analyzing ecological data..."):
                # Context provides the AI with your real-time cloud data
                context = f"The current temperature is {latest['temperature_c']}°C, humidity is {latest['humidity_pct']}%, and soil moisture is {latest['soil_moisture_pct']}%."
                prompt = f"As a Wildlife Ecology expert, answer this: {user_query}. Context: {context}"
                
                response = model.generate_content(prompt)
                st.info(response.text)

        with st.expander("📂 View Raw History"):
            st.dataframe(df, use_container_width=True)
    else:
        st.warning("Database is empty. Log your first reading!")

except Exception as e:
    st.error(f"System Error: {e}")
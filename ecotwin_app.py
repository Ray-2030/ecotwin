import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
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

# Setup Gemini AI - Updated for 2026 Model Standards
genai.configure(api_key=st.secrets["gemini"]["api_key"])
# Using gemini-2.0-flash which replaces the retired 1.5 versions
model = genai.GenerativeModel('gemini-2.0-flash')

# --- 2. APP LAYOUT ---
st.set_page_config(page_title="EcoTwin AI Dashboard", page_icon="🌿", layout="wide")
st.title("🌿 EcoTwin AI Cloud Monitoring")
st.caption("Wildlife Ecology & Management Project")

# --- 3. SIDEBAR: DATA ENTRY ---
with st.sidebar:
    st.header("📍 Field Data Entry")
    temp = st.number_input("Temp (°C)", value=25.0, step=0.1)
    hum = st.number_input("Humidity (%)", value=50.0, step=0.1)
    soil = st.number_input("Soil Moisture (%)", value=30.0, step=0.1)
    
    if st.button("Push to Aiven Cloud"):
        try:
            engine = get_engine()
            with engine.begin() as conn:
                query = text("INSERT INTO eco_logs (temperature_c, humidity_pct, soil_moisture_pct) VALUES (:t, :h, :s)")
                conn.execute(query, {"t": temp, "h": hum, "s": soil})
            st.success("✅ Saved to Cloud!")
            st.balloons()
        except Exception as e:
            st.error(f"Sync Failed: {e}")

# --- 4. MAIN DASHBOARD ---
try:
    engine = get_engine()
    df = pd.read_sql("SELECT recorded_at, temperature_c, humidity_pct, soil_moisture_pct FROM eco_logs ORDER BY recorded_at DESC LIMIT 50", engine)
    
    if not df.empty:
        latest = df.iloc[0]
        m1, m2, m3 = st.columns(3)
        m1.metric("Current Temp", f"{latest['temperature_c']}°C")
        m2.metric("Humidity", f"{latest['humidity_pct']}%")
        m3.metric("Soil Moisture", f"{latest['soil_moisture_pct']}%")
        
        st.subheader("Ecological Trends")
        st.line_chart(df.set_index('recorded_at')[['temperature_c', 'humidity_pct', 'soil_moisture_pct']])
        
        # --- 5. AI CHAT SECTION ---
        st.markdown("---")
        st.subheader("🤖 Chat with EcoTwin AI")
        user_query = st.text_input("Ask about your garden readings:")

        if user_query:
            with st.spinner("Consulting Gemini 2.0..."):
                context = f"Context: Temp {latest['temperature_c']}°C, Humidity {latest['humidity_pct']}%, Soil {latest['soil_moisture_pct']}%."
                prompt = f"As a Wildlife Ecology expert, answer: {user_query}. {context}"
                
                try:
                    response = model.generate_content(prompt)
                    st.info(response.text)
                except Exception as ai_err:
                    st.error(f"AI Connection Error: {ai_err}")

        with st.expander("📂 Raw Data Log"):
            st.dataframe(df, use_container_width=True)
except Exception as e:
    st.error(f"System Error: {e}")
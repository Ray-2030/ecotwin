import streamlit as st
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from datetime import datetime

# --- DATABASE ENGINE SETUP ---
def get_engine():
    # Constructing the modern SQLAlchemy URL from your secrets
    user = st.secrets["connections"]["postgresql"]["username"]
    pw = st.secrets["connections"]["postgresql"]["password"]
    host = st.secrets["connections"]["postgresql"]["host"]
    port = st.secrets["connections"]["postgresql"]["port"]
    db = st.secrets["connections"]["postgresql"]["database"]
    
    db_url = f"postgresql://{user}:{pw}@{host}:{port}/{db}?sslmode=require"
    return create_engine(db_url)

# --- APP LAYOUT ---
st.set_page_config(page_title="EcoTwin Dashboard", page_icon="🌿", layout="wide")
st.title("🌿 EcoTwin Cloud Monitoring")
st.info("Wildlife Ecology & Management - Digital Twin Project")

# --- SIDEBAR: DATA ENTRY ---
with st.sidebar:
    st.header("📍 Field Data Entry")
    temp = st.number_input("Temp (°C)", value=24.5, step=0.1)
    hum = st.number_input("Humidity (%)", value=58.0, step=0.1)
    soil = st.number_input("Soil Moisture (%)", value=40.0, step=0.1)
    
    if st.button("Push to Aiven Cloud"):
        try:
            engine = get_engine()
            with engine.begin() as conn:
                query = "INSERT INTO eco_logs (temperature_c, humidity_pct, soil_moisture_pct) VALUES (%s, %s, %s)"
                conn.execute(query, (temp, hum, soil))
            st.success("✅ Saved to Cloud!")
            st.balloons()
        except Exception as e:
            st.error(f"Sync Failed: {e}")

# --- MAIN DASHBOARD: VISUALS ---
try:
    engine = get_engine()
    # Pull latest 50 records
    df = pd.read_sql("SELECT recorded_at, temperature_c, humidity_pct, soil_moisture_pct FROM eco_logs ORDER BY recorded_at DESC LIMIT 50", engine)
    
    if not df.empty:
        # Metric row for mobile-friendly view
        m1, m2, m3 = st.columns(3)
        m1.metric("Current Temp", f"{df['temperature_c'].iloc[0]}°C")
        m2.metric("Humidity", f"{df['humidity_pct'].iloc[0]}%")
        m3.metric("Soil Moisture", f"{df['soil_moisture_pct'].iloc[0]}%")
        
        # Charts
        st.subheader("Ecological Trends")
        st.line_chart(df.set_index('recorded_at')[['temperature_c', 'humidity_pct', 'soil_moisture_pct']])
        
        # Raw Data Table
        with st.expander("📂 View Raw History"):
            st.dataframe(df, use_container_width=True)
    else:
        st.warning("Cloud database is empty. Add your first field reading in the sidebar!")

except Exception as e:
    st.error(f"Database Offline: {e}")
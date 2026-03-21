import streamlit as st
import psycopg2
import pandas as pd
from datetime import datetime

# --- DATABASE CONNECTION (Aiven Cloud) ---
def get_db_connection():
    # This automatically reads your credentials from .streamlit/secrets.toml
    return psycopg2.connect(
        host=st.secrets["connections"]["postgresql"]["host"],
        port=st.secrets["connections"]["postgresql"]["port"],
        database=st.secrets["connections"]["postgresql"]["database"],
        user=st.secrets["connections"]["postgresql"]["username"],
        password=st.secrets["connections"]["postgresql"]["password"],
        sslmode="require"
    )

# Page Branding
st.set_page_config(page_title="EcoTwin Dashboard", page_icon="🌿")
st.title("🌿 EcoTwin Cloud Dashboard")
st.markdown("---")

# --- SIDEBAR: LOG DATA ---
st.sidebar.header("Input Sensor Data")
temp = st.sidebar.number_input("Temperature (°C)", value=25.0, step=0.1)
hum = st.sidebar.number_input("Humidity (%)", value=60.0, step=0.1)
soil = st.sidebar.number_input("Soil Moisture (%)", value=45.0, step=0.1)

if st.sidebar.button("Push to Aiven Cloud"):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        # SQL Command for your new PostgreSQL table
        query = """
            INSERT INTO eco_logs (temperature_c, humidity_pct, soil_moisture_pct) 
            VALUES (%s, %s, %s)
        """
        cur.execute(query, (temp, hum, soil))
        conn.commit()
        cur.close()
        conn.close()
        st.sidebar.success("✅ Data secured in the cloud!")
    except Exception as e:
        st.sidebar.error(f"❌ Connection Error: {e}")

# --- MAIN AREA: TRENDS & ANALYTICS ---
try:
    conn = get_db_connection()
    # Pulling the last 50 entries to show on the graph
    df = pd.read_sql("SELECT recorded_at, temperature_c, humidity_pct, soil_moisture_pct FROM eco_logs ORDER BY recorded_at DESC LIMIT 50", conn)
    conn.close()

    if not df.empty:
        # Latest Readings Metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Current Temp", f"{df['temperature_c'].iloc[0]}°C")
        col2.metric("Humidity", f"{df['humidity_pct'].iloc[0]}%")
        col3.metric("Soil Moisture", f"{df['soil_moisture_pct'].iloc[0]}%")

        # Visualization Chart
        st.subheader("Ecological Data History")
        chart_data = df.set_index('recorded_at')
        st.line_chart(chart_data[['temperature_c', 'humidity_pct', 'soil_moisture_pct']])
        
        # Data Table View
        with st.expander("View Raw Data Log"):
            st.dataframe(df)
    else:
        st.info("The cloud database is currently empty. Use the sidebar to log your first ecological reading!")

except Exception as e:
    st.error(f"Could not load data from Cloud: {e}")
import streamlit as st
import pandas as pd
import requests
from sqlalchemy import create_engine, text

st.set_page_config(page_title="Sentinel Live Map", page_icon="📍", layout="wide")

# --- WEATHER API ---
def get_nairobi_weather():
    try:
        url = "https://api.open-meteo.com/v1/forecast?latitude=-1.28&longitude=36.82&current_weather=true"
        res = requests.get(url).json()
        return res['current_weather']
    except:
        return None

# --- DATABASE ENGINE ---
def get_engine():
    s = st.secrets["connections"]["postgresql"]
    return create_engine(
        f"postgresql://{s['username']}:{s['password']}@{s['host']}:{s['port']}/{s['database']}?sslmode=require",
        pool_pre_ping=True,
        connect_args={'connect_timeout': 30}
    )

st.title("📍 Sentinel Live Deployment Map")

# Weather Widget
weather = get_nairobi_weather()
if weather:
    c1, c2, c3 = st.columns(3)
    c1.metric("Nairobi Temp", f"{weather['temperature']}°C")
    c2.metric("Wind Speed", f"{weather['windspeed']} km/h")
    c3.metric("Status", "Clear Skies" if weather['weathercode'] == 0 else "Cloudy")

st.markdown("---")

# --- MAPPING LOGIC ---
try:
    with get_engine().connect() as conn:
        df = pd.read_sql(text("SELECT species, ranger FROM sightings"), conn)
        
        if not df.empty:
            # Generate random visual scatter around Nairobi for current sightings
            import numpy as np
            df['latitude'] = -1.286 + np.random.uniform(-0.05, 0.05, len(df))
            df['longitude'] = 36.817 + np.random.uniform(-0.05, 0.05, len(df))
            
            st.subheader("Recent Field Observations")
            st.map(df, color="#2E7D32")
            st.dataframe(df[['ranger', 'species']], use_container_width=True)
        else:
            st.info("No GPS data reported yet. Use the Hub to scan animals!")
            
except Exception:
    st.error("Map layer connection lost. Central database is likely warming up.")

if st.button("⬅️ Return to Hub"):
    st.switch_page("pages/3_Sentinel_Hub.py")
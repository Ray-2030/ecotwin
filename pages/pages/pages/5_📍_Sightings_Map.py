import streamlit as st
import pandas as pd
import requests
from sqlalchemy import create_engine, text

st.set_page_config(page_title="Ranger Map", page_icon="📍")

# ☁️ LIVE WEATHER OVERLAY
def get_weather():
    # Using Open-Meteo (Free, no API key needed for basic usage)
    url = "https://api.open-meteo.com/v1/forecast?latitude=-1.28&longitude=36.82&current_weather=true"
    res = requests.get(url).json()
    return res['current_weather']

st.title("📍 Sentinel Live Map")

# Weather Card
w = get_weather()
col1, col2 = st.columns(2)
col1.metric("Nairobi Temp", f"{w['temperature']}°C")
col2.metric("Wind Speed", f"{w['windspeed']} km/h")

# Map Logic
def get_engine():
    s = st.secrets["connections"]["postgresql"]
    return create_engine(f"postgresql://{s['username']}:{s['password']}@{s['host']}:{s['port']}/{s['database']}?sslmode=require")

try:
    with get_engine().connect() as conn:
        df = pd.read_sql(text("SELECT lat as latitude, lon as longitude, species FROM sightings"), conn)
        if not df.empty:
            st.map(df)
        else:
            st.info("Map is empty. Go scan some wildlife!")
except:
    st.error("Map layer connection error.")

if st.button("⬅️ Back to Hub"): st.switch_page("pages/3_🌿_Sentinel_Hub.py")
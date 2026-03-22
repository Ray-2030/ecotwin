import streamlit as st
import pandas as pd
import requests
from sqlalchemy import create_engine, text

st.set_page_config(page_title="Wildlife Map", page_icon="📍")

def get_weather():
    url = "https://api.open-meteo.com/v1/forecast?latitude=-1.28&longitude=36.82&current_weather=true"
    return requests.get(url).json()['current_weather']

st.title("📍 Sentinel Live Map")

# Weather Dashboard
w = get_weather()
c1, c2 = st.columns(2)
c1.metric("Nairobi Temp", f"{w['temperature']}°C")
c2.metric("Wind Speed", f"{w['windspeed']} km/h")

def get_engine():
    s = st.secrets["connections"]["postgresql"]
    return create_engine(f"postgresql://{s['username']}:{s['password']}@{s['host']}:{s['port']}/{s['database']}?sslmode=require")

try:
    with get_engine().connect() as conn:
        # We simulate coordinates for now until GPS capture is added
        df = pd.read_sql(text("SELECT species FROM sightings"), conn)
        if not df.empty:
            df['latitude'] = -1.286 + (pd.Series(range(len(df))) * 0.01) # Spread them out slightly
            df['longitude'] = 36.817
            st.map(df)
        else:
            st.info("No map data available.")
except:
    st.error("Map layer connection error.")

if st.button("⬅️ Back to Hub"):
    st.switch_page("pages/3_Sentinel_Hub.py")
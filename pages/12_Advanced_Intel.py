import streamlit as st
import pydeck as pdk
import pandas as pd
import random

st.set_page_config(page_title="Advanced Intel", layout="wide")

st.title("🛰️ Sentinel-6 Satellite: Advanced Intel")

# --- 26. SMART BIOSPHERE IOT (LIVE HEARTBEATS) ---
st.subheader("💓 Live IoT Biosensor Feed")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Rhino-Alpha Heartrate", f"{random.randint(40, 55)} BPM", "Normal")
with col2:
    st.metric("Mara River Level", "1.2m", "-0.1m (Dry Season)")
with col3:
    st.metric("LoRaWAN Signal", "Strong", "915 MHz")

# --- 27 & 29. PREDICTIVE DIGITAL TWIN (MAP) ---
st.subheader("🗺️ 2026 Predictive Digital Twin")
# Simulating NDVI (Vegetation Health) and Prediction Paths
data = pd.DataFrame({
    'lat': [-1.3, -1.31, -1.32],
    'lon': [34.8, 34.81, 34.82],
    'type': ['Current', 'Predicted (2h)', 'Predicted (4h)']
})

st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/satellite-v9',
    initial_view_state=pdk.ViewState(latitude=-1.3, longitude=34.8, zoom=12, pitch=45),
    layers=[
        pdk.Layer(
            "ScatterplotLayer",
            data,
            get_position='[lon, lat]',
            get_color='[0, 255, 0, 160]',
            get_radius=100,
        ),
        pdk.Layer(
            "LineLayer",
            data,
            get_source_position='[34.8, -1.3]',
            get_target_position='[34.82, -1.32]',
            get_color='[255, 255, 0]',
            get_width=5,
        )
    ]
))
st.caption("🟡 Yellow line: AI-predicted migration path based on NDVI vegetation health.")
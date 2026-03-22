import streamlit as st
import pydeck as pdk
import pandas as pd

st.set_page_config(page_title="Advanced Intel", layout="wide")

st.title("🛰️ Sentinel-6 Satellite: Advanced Intel")

st.subheader("🗺️ 2026 Predictive Digital Twin")

# Coordinates centered on the Maasai Mara region
map_data = pd.DataFrame({
    'lat': [-1.35, -1.37, -1.40],
    'lon': [34.90, 34.92, 34.95],
    'type': ['Current Position', 'Predicted (2h)', 'Predicted (4h)']
})

# Correctly centering the map for Kenya
st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/satellite-v9',
    initial_view_state=pdk.ViewState(
        latitude=-1.35, 
        longitude=34.90, 
        zoom=11, 
        pitch=45
    ),
    layers=[
        pdk.Layer(
            "ScatterplotLayer",
            map_data,
            get_position='[lon, lat]',
            get_color='[0, 255, 0, 200]',
            get_radius=300,
        ),
        pdk.Layer(
            "ArcLayer",
            data=map_data,
            get_source_position='[34.90, -1.35]',
            get_target_position='[34.95, -1.40]',
            get_source_color=[0, 255, 0],
            get_target_color=[255, 255, 0],
            get_width=4,
        )
    ]
))

st.caption("🟢 Green Points: Detected Wildlife | 🟡 Yellow Arc: Predicted Movement Vector")

if st.button("⬅️ Back to Hub"):
    st.switch_page("pages/3_Sentinel_Hub.py")
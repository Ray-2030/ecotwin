import streamlit as st
import pandas as pd
import pydeck as pdk

st.title("📍 Field Intelligence: Heatmap")

# Sample Data (In a real app, this comes from your SQL sightings table)
data = pd.DataFrame({
    'lat': [-1.286, -1.292, -0.5, 0.0, -1.3],
    'lon': [36.817, 36.821, 37.0, 36.0, 34.8],
    'weight': [10, 20, 5, 15, 30]
})

view_state = pdk.ViewState(latitude=-1.28, longitude=36.81, zoom=6, pitch=50)

layer = pdk.Layer(
    "HeatmapLayer",
    data,
    get_position='[lon, lat]',
    get_weight='weight',
    aggregation=pdk.types.String("SUM"),
)

st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))

# Weather Overlay Placeholder
st.sidebar.info("🌦️ Ambience: 24°C | Wind: 12km/h SE")
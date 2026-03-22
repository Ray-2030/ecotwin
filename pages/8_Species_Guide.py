import streamlit as st
import plotly.express as px
import pandas as pd

st.title("🔍 Species Explorer")

# Interactive Circle
data = {"Name": ["Fish Eagle", "Crane", "Rhino", "Bongo"], "Type": ["Bird", "Bird", "Mammal", "Mammal"], "Info": ["Apex predator", "Graceful icon", "Critically endangered", "Rare antelope"]}
fig = px.sunburst(pd.DataFrame(data), path=['Type', 'Name'], hover_data=['Info'])
st.plotly_chart(fig)

# AR Guide Placeholder
st.divider()
st.subheader("🕶️ AR Training Guide")
st.warning("AR Model Loading... (Requires mobile browser support)")
st.image("https://cdn-icons-png.flaticon.com/512/1391/1391424.png", width=100)
st.caption("Point your phone at a flat surface to see a 3D Rhino.")
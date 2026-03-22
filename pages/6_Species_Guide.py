import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Species Explorer", layout="wide")

st.title("🔍 Interactive Species Guide")

# Updated data with complete 'Info' strings to fix tooltip errors
data = {
    "labels": ["Fauna", "Mammals", "Birds", "Mountain Bongo", "Grey Crane", "Black Rhino"],
    "parents": ["", "Fauna", "Fauna", "Mammals", "Birds", "Mammals"],
    "values": [10, 2, 2, 1, 1, 1],
    "Info": [
        "Kenyan Biodiversity Base", 
        "Endemic and endangered mammals", 
        "Avian species monitoring", 
        "Critically endangered (~130 remain)", 
        "Rapid wetland habitat loss", 
        "Priority poaching surveillance"
    ]
}

df = pd.DataFrame(data)

# Building the Sunburst Chart with corrected hover data
fig = px.sunburst(
    df,
    names='labels',
    parents='parents',
    values='values',
    hover_data={'Info': True},
    color='labels',
    color_discrete_sequence=px.colors.qualitative.Prism
)

fig.update_layout(margin=dict(t=0, l=0, r=0, b=0), height=600)

st.plotly_chart(fig, use_container_width=True)

if st.button("⬅️ Back to Hub"):
    st.switch_page("pages/3_Sentinel_Hub.py")
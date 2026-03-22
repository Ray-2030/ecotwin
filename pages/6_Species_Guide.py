import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Species Explorer", page_icon="🐦")
st.title("🔍 Interactive Species Guide")

# Ensure the column names here match the path=['Level', 'Type', 'Name'] exactly
data = {
    "Level": ["Fauna", "Fauna", "Fauna", "Fauna"],
    "Type": ["Birds", "Birds", "Mammals", "Mammals"],
    "Name": ["Fish Eagle", "Grey Crane", "Black Rhino", "Mountain Bongo"],
    "Info": [
        "Apex lake predator. Known for its distinct white head.",
        "Kenya's national icon of grace, found in wetlands.",
        "Critically endangered. Monitored for anti-poaching safety.",
        "Rare forest antelope. Native to the Aberdare ranges."
    ]
}

df = pd.DataFrame(data)

# 'hover_data' tells Plotly which columns to show when you move your cursor
fig = px.sunburst(df, 
                  path=['Level', 'Type', 'Name'], 
                  values=[1, 1, 1, 1], # Ensures segments are equal size
                  hover_data={'Info': True, 'Level': False, 'Type': False},
                  color='Type', 
                  color_discrete_map={'Birds': '#00f2fe', 'Mammals': '#2E7D32'})

fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)", 
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="white", 
    margin=dict(t=0, l=0, r=0, b=0)
)

st.plotly_chart(fig, use_container_width=True)
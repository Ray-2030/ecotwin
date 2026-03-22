import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Species Explorer", page_icon="🐦")
st.title("🔍 Interactive Species Guide")
st.write("Hover over the segments to see ecology explanations.")

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

fig = px.sunburst(pd.DataFrame(data), path=['Level', 'Type', 'Name'], 
                  hover_data={'Info': True},
                  color='Type', 
                  color_discrete_map={'Birds': '#00f2fe', 'Mammals': '#2E7D32'})

fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="white", margin=dict(t=0, l=0, r=0, b=0))
st.plotly_chart(fig, use_container_width=True)

st.divider()
st.subheader("🕶️ AR Species Training")
st.image("https://cdn-icons-png.flaticon.com/512/1391/1391424.png", width=80)
st.caption("Point your mobile camera at a flat surface to see 3D wildlife models.")
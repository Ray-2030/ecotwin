import streamlit as st
import datetime
import pytz

# 1. SET KENYA TIME & AUTO-NIGHT LOGIC
kenya_tz = pytz.timezone('Africa/Nairobi')
hour = datetime.datetime.now(kenya_tz).hour
is_night = hour >= 18 or hour < 6  # Night is 6PM to 6AM

st.set_page_config(page_title="Sentinel Alpha", page_icon="🛡️")

# 2. GLOBAL CSS (Night Vision + Glowing Buttons)
night_bg = "linear-gradient(135deg, #051605, #0a200a)"
day_bg = "linear-gradient(135deg, #0f2027, #203a43, #2c5364)"
theme_color = "#00FF00" if is_night else "#00f2fe"

st.markdown(f"""
<style>
    .stApp {{ background: {night_bg if is_night else day_bg}; color: white; }}
    /* Glowing Cyber-Ecology Buttons */
    div.stButton > button {{
        border: 2px solid {theme_color} !important;
        background-color: transparent !important;
        color: white !important;
        box-shadow: 0 0 10px {theme_color};
    }}
</style>
""", unsafe_allow_html=True)

st.title("🛡️ Sentinel Alpha: Mission Start")
st.write(f"Current Status: {'🌙 Night Patrol Active' if is_night else '☀️ Day Surveillance Active'}")

# Login
with st.container(border=True):
    u = st.text_input("Ranger Callsign")
    if st.button("Initialize Link"):
        st.session_state.user = u
        st.switch_page("pages/3_Sentinel_Hub.py")
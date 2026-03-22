import streamlit as st
import google.generativeai as genai
from sqlalchemy import create_engine, text
import numpy as np
import datetime
import geocoder  # Added for live location
import pytz      # Added for accurate Kenyan time

# --- PAGE CONFIG ---
st.set_page_config(page_title="Sentinel Hub", page_icon="🌿", layout="wide")

# --- LIVE CONTEXT: TIME, DATE, & LOCATION ---
# Set to East Africa Time (EAT)
kenya_tz = pytz.timezone('Africa/Nairobi')
kenya_now = datetime.datetime.now(kenya_tz)
current_date = kenya_now.strftime("%d %B %Y")
current_time = kenya_now.strftime("%H:%M:%S")

# Auto-detect location via IP
try:
    g = geocoder.ip('me')
    # Default to Rift Valley/Nairobi if sensor is blocked
    loc_city = g.city if g.city else "Rift Valley"
    loc_coords = f"{g.latlng[0]:.4f}, {g.latlng[1]:.4f}" if g.latlng else "-1.2863, 36.8172"
except Exception:
    loc_city = "Kenya (Field Post)"
    loc_coords = "-1.2863, 36.8172"

# --- UI THEME & NIGHT VISION ---
night_mode = st.sidebar.toggle("🌙 Night Vision Mode")
bg = "linear-gradient(135deg, #051605, #0a200a)" if night_mode else "linear-gradient(135deg, #0f2027, #203a43, #2c5364)"
txt = "#00FF00" if night_mode else "white"

st.markdown(f"""
<style>
    .stApp {{ background: {bg}; color: {txt}; }}
    [data-testid="stSidebar"] {{ background-color: rgba(0,20,0,0.8); border-right: 2px solid #00f2fe; }}
    .ticker-wrap {{ width: 100%; overflow: hidden; background: rgba(0,0,0,0.5); padding: 10px; border-top: 1px solid #00f2fe; position: fixed; bottom: 0; left: 0; z-index: 999; }}
    .ticker {{ display: inline-block; white-space: nowrap; animation: ticker 25s linear infinite; color: #00f2fe; font-weight: bold; }}
    @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("🌲 Ranger Tools")
    
    if st.button("🚨 ACTIVATED DETERRENT", use_container_width=True):
        sample_rate = 44100
        t = np.linspace(0, 2, 2 * sample_rate, False)
        note = np.sin(15000 * t * 2 * np.pi) 
        st.audio(note, sample_rate=sample_rate, autoplay=True)
        st.toast("Deterrent Sound Emitted!", icon="🔊")
    
    st.markdown("---")
    st.subheader("🚀 Quick Navigation")
    # Updated Page list matching your folder structure
    if st.button("📍 Sightings Map", use_container_width=True): st.switch_page("pages/5_Sightings_Map.py")
    if st.button("🔍 Species Guide", use_container_width=True): st.switch_page("pages/8_Species_Guide.py")
    if st.button("📕 My Pokédex", use_container_width=True): st.switch_page("pages/7_Pokedex.py")
    if st.button("📓 Field Notes", use_container_width=True): st.switch_page("pages/9_Field_Notes.py")
    
    # NEW: Report & QR Tool Link
    if st.button("📊 Ecology Report Tools", use_container_width=True): 
        st.switch_page("pages/10_Generate_Report.py")

# --- MAIN DASHBOARD ---
col_logo, col_title = st.columns([1, 5])
with col_logo:
    st.image("https://cdn-icons-png.flaticon.com/512/3062/3062250.png", width=80)
with col_title:
    st.title("🛡️ Sentinel Alpha Command")

# Live Metrics Bar
m1, m2, m3 = st.columns(3)
m1.metric("Date
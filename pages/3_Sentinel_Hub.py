import streamlit as st
import google.generativeai as genai
import numpy as np
import datetime
import geocoder 
import pytz      

# --- PAGE CONFIG ---
st.set_page_config(page_title="Sentinel Hub", page_icon="🌿", layout="wide")

# --- LIVE CONTEXT: TIME, DATE, & LOCATION ---
kenya_tz = pytz.timezone('Africa/Nairobi')
kenya_now = datetime.datetime.now(kenya_tz)
current_date = kenya_now.strftime("%d %B %Y")
current_time = kenya_now.strftime("%H:%M:%S")

try:
    g = geocoder.ip('me')
    loc_city = g.city if g.city else "Rift Valley"
    loc_coords = f"{g.latlng[0]:.4f}, {g.latlng[1]:.4f}" if g.latlng else "-1.2863, 36.8172"
except Exception:
    loc_city = "Kenya (Field Post)"
    loc_coords = "-1.2863, 36.8172"

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("🌲 Ranger Tools")
    st.markdown("---")
    if st.button("📍 Sightings Map", use_container_width=True): st.switch_page("pages/5_Sightings_Map.py")
    if st.button("🔍 Species Guide", use_container_width=True): st.switch_page("pages/8_Species_Guide.py")
    if st.button("📕 My Pokédex", use_container_width=True): st.switch_page("pages/7_Pokedex.py")
    if st.button("📓 Field Notes", use_container_width=True): st.switch_page("pages/9_Field_Notes.py")
    
    # Integrated link to the new report page
    if st.button("📊 Ecology Report Tools", use_container_width=True): 
        st.switch_page("pages/10_Generate_Report.py")

# --- MAIN DASHBOARD ---
col_logo, col_title = st.columns([1, 5])
with col_logo:
    st.image("https://cdn-icons-png.flaticon.com/512/3062/3062250.png", width=80)
with col_title:
    st.title("🛡️ Sentinel Alpha Command")

m1, m2, m3 = st.columns(3)
m1.metric("Date", current_date)
m2.metric("EAT Time", current_time)
m3.metric(f"Location: {loc_city}", loc_coords)

st.markdown("---")

# --- AI SCANNER ---
img = st.camera_input("Scan Wildlife for ID")
if img:
    st.write("Processing field scan...")
    # Your Gemini logic here
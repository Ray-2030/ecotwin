import streamlit as st
from streamlit_lottie import st_lottie
import requests
import google.generativeai as genai
import datetime, pytz, geocoder

# --- PAGE SETUP ---
st.set_page_config(page_title="Command Hub", layout="wide")

# Lottie Animation Loader
def load_lottie(url):
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

# --- SIDEBAR (The 25-Feature Navigation) ---
with st.sidebar:
    st_lottie(load_lottie("https://assets10.lottiefiles.com/packages/lf20_m6cu96ze.json"), height=100)
    st.title("🌲 Ranger Tools")
    
    if st.button("📍 Heatmap"): st.switch_page("pages/5_Sightings_Map.py")
    if st.button("🔍 Species Guide"): st.switch_page("pages/8_Species_Guide.py")
    if st.button("📕 Pokédex"): st.switch_page("pages/7_Pokedex.py")
    if st.button("📓 Field Notes"): st.switch_page("pages/9_Field_Notes.py")
    st.markdown("---")
    st.subheader("🛠️ Advanced")
    if st.button("🎮 Ranger Console"): st.switch_page("pages/11_Ranger_Console.py")
    if st.button("📊 QR Report Tool"): st.switch_page("pages/10_Generate_Report.py")
    if st.button("🛡️ Advanced Intel"): st.switch_page("pages/12_Advanced_Intel.py")

# --- LIVE METRICS ---
tz = pytz.timezone('Africa/Nairobi')
now = datetime.datetime.now(tz)
g = geocoder.ip('me')

c1, c2, c3 = st.columns(3)
c1.metric("Date", now.strftime("%d %b %Y"))
c2.metric("EAT Time", now.strftime("%H:%M"))
c3.metric("Location", g.city if g.city else "Rift Valley")

# --- SCANNER ---
st.divider()
img = st.camera_input("Field Scanner")
if img:
    st.info("AI identifying species... (Latin names & Facts arriving)")
    # (Your Gemini Logic here)
import streamlit as st
import google.generativeai as genai
from sqlalchemy import create_engine, text
import numpy as np
import datetime

# --- PAGE CONFIG MUST BE FIRST ---
st.set_page_config(page_title="Sentinel Hub", page_icon="🌿", layout="wide")

# --- NIGHT VISION & UI THEME ---
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

# --- SIDEBAR NAVIGATION & TOOLS ---
with st.sidebar:
    st.title("🌲 Ranger Tools")
    
    if st.button("🚨 ACTIVATED DETERRENT"):
        sample_rate = 44100
        t = np.linspace(0, 2, 2 * sample_rate, False)
        # High-frequency sound for predator deterrent
        note = np.sin(15000 * t * 2 * np.pi) 
        st.audio(note, sample_rate=sample_rate, autoplay=True)
        st.toast("Deterrent Sound Emitted!", icon="🔊")
    
    st.markdown("---")
    st.subheader("🚀 Quick Navigation")
    if st.button("📍 Sightings Map"): st.switch_page("pages/5_Sightings_Map.py")
    if st.button("🔍 Species Guide"): st.switch_page("pages/8_Species_Guide.py")
    if st.button("📕 My Pokédex"): st.switch_page("pages/7_Pokedex.py")
    if st.button("📓 Field Notes"): st.switch_page("pages/9_Field_Notes.py")

# --- MAIN INTERFACE ---
st.title(f"🌿 Sentinel Hub: {st.session_state.get('user', 'Ranger Wolf')}")
img = st.camera_input("Scan Wildlife for ID")

species_detected = "Waiting for scan..."

if img:
    try:
        genai.configure(api_key=st.secrets["gemini"]["api_key"])
        model = genai.GenerativeModel('gemini-1.5-flash')
        res = model.generate_content(["ID species and 1 ecology fact.", img]).text
        species_detected = res.split('\n')[0].replace("**", "").strip()
        
        # Priority Alert for Endangered Species
        if any(crit in species_detected for crit in ["Bongo", "Rhino", "Elephant", "Crane"]):
            st.error(f"🚨 PRIORITY ALERT: {species_detected} Detected!")
            st.balloons()
        
        st.write(res)
    except Exception as e:
        st.warning("Scanner warming up... Please check API key in secrets.")

# --- COMMUNITY TICKER ---
st.markdown(f"""<div class="ticker-wrap"><div class="ticker">
    LIVE FEED: Ranger Wolf logged a {species_detected} • Angela spotted a Lion near Maasai Mara • Weather: 24°C Sunny • Drone Status: Ready for Flight
    </div></div>""", unsafe_allow_html=True)
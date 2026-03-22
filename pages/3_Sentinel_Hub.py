import streamlit as st
import google.generativeai as genai
from sqlalchemy import create_engine, text
import numpy as np
import datetime

st.set_page_config(page_title="Sentinel Hub", page_icon="🌿", layout="wide")

# --- NIGHT VISION & CSS ---
night_mode = st.sidebar.toggle("🌙 Night Vision Mode")
bg_color = "linear-gradient(135deg, #051605, #0a200a)" if night_mode else "linear-gradient(135deg, #0f2027, #203a43, #2c5364)"
text_color = "#00FF00" if night_mode else "white"

st.markdown(f"""
<style>
    .stApp {{ background: {bg_color}; color: {text_color}; }}
    [data-testid="stSidebar"] {{ background-color: rgba(0,20,0,0.9); border-right: 2px solid #00f2fe; }}
    /* Scrolling Ticker */
    .ticker-wrap {{ width: 100%; overflow: hidden; background: rgba(0,0,0,0.5); padding: 10px; border-top: 1px solid #00f2fe; position: fixed; bottom: 0; left: 0; }}
    .ticker {{ display: inline-block; white-space: nowrap; animation: ticker 20s linear infinite; color: #00f2fe; font-weight: bold; }}
    @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}
</style>
""", unsafe_allow_html=True)

# --- DETERRENT MODE (High Frequency Sound) ---
if st.sidebar.button("🚨 ACTIVATED DETERRENT"):
    sample_rate = 44100
    t = np.linspace(0, 2, 2 * sample_rate, False)
    note = np.sin(15000 * t * 2 * np.pi) # 15kHz High Pitch
    st.audio(note, sample_rate=sample_rate, autoplay=True)
    st.toast("Deterrent Sound Emitted!", icon="🔊")

# --- MAIN HUB ---
st.title(f"🌿 Sentinel Hub: {st.session_state.get('user', 'Ranger')}")
img = st.camera_input("Scan Wildlife")

if img:
    genai.configure(api_key=st.secrets["gemini"]["api_key"])
    model = genai.GenerativeModel('gemini-1.5-flash')
    res = model.generate_content(["ID species and 1 ecology fact.", img]).text
    species = res.split('\n')[0].replace("**", "").strip()
    
    # Endangered Alert
    if any(crit in species for crit in ["Bongo", "Rhino", "Elephant"]):
        st.error(f"🚨 PRIORITY ALERT: {species} Detected!")
        st.balloons()
    
    st.write(res)

# --- COMMUNITY TICKER ---
st.markdown(f"""<div class="ticker-wrap"><div class="ticker">
    LATEST LOGS: Ranger Angela spotted a Lion near Maasai Mara ... Ranger Wolf logged a Black Rhino ... Weather: 24°C Sunny
    </div></div>""", unsafe_allow_html=True)
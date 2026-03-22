import streamlit as st
import requests
import datetime
import pytz

# 1. SET KENYA TIME & AUTO-NIGHT LOGIC
kenya_tz = pytz.timezone('Africa/Nairobi')
hour = datetime.datetime.now(kenya_tz).hour
is_night = hour >= 18 or hour < 6

# 43. WEATHER-SENSING LOGIC
def get_weather():
    try:
        # Fetching live Nairobi weather via Open-Meteo
        res = requests.get("https://api.open-meteo.com/v1/forecast?latitude=-1.29&longitude=36.82&current_weather=True").json()
        return res['current_weather']['weathercode']
    except: return 0

weather_code = get_weather()
# Codes for rain in Open-Meteo
is_raining = weather_code in [51, 53, 55, 61, 63, 65, 80, 81, 82]

st.set_page_config(page_title="Sentinel Alpha", page_icon="🛡️", layout="centered")

# 31. HOLOGRAPHIC HUD & GLASSMORPHISM CSS
st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(0, 20, 0, 0.8), rgba(0, 5, 0, 0.9)), 
                    url('https://www.transparenttextures.com/patterns/carbon-fibre.png');
        background-attachment: fixed;
        color: white;
    }}
    /* Glassmorphism Containers */
    [data-testid="stVerticalBlock"] > div:has(div.stMetric), .stAlert {{
        background: rgba(0, 255, 0, 0.05) !important;
        backdrop-filter: blur(12px);
        border: 1px solid rgba(0, 255, 0, 0.2) !important;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 0 15px rgba(0, 255, 0, 0.1);
    }}
    /* Cyber-Glowing Buttons */
    div.stButton > button {{
        border: 2px solid #00f2fe !important;
        background-color: transparent !important;
        color: white !important;
        box-shadow: 0 0 10px #00f2fe;
        text-transform: uppercase;
        font-weight: bold;
    }}
    /* 43. Digital Rain Animation (Triggered by Nairobi Weather) */
    { ".stApp::before { content: '💧'; position: fixed; top: -50px; left: 0; width: 100%; height: 100%; opacity: 0.2; pointer-events: none; z-index: 999; font-size: 24px; animation: rain 2s linear infinite; } @keyframes rain { to { transform: translateY(100vh); } }" if is_raining else "" }
</style>
""", unsafe_allow_html=True)

st.title("🛡️ Sentinel Alpha: Mission Start")
st.subheader("ようこそ (Welcome), Ranger Wolf")

# Login & Language Toggle
lang = st.sidebar.selectbox("🌐 Language / 言語", ["English", "Kiswahili", "日本語 (Japanese)"])
welcome_msg = {"English": "Initialize Link", "Kiswahili": "Anza Muunganisho", "日本語 (Japanese)": "リンクを初期化する"}

u = st.text_input("Enter Ranger Callsign", placeholder="e.g. Wolf")
if st.button(welcome_msg[lang]):
    st.session_state.user = u
    st.session_state.lang = lang
    st.switch_page("pages/3_Sentinel_Hub.py")
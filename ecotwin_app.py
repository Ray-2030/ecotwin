import streamlit as st
import datetime
import pytz

# --- TIME & THEME LOGIC ---
kenya_tz = pytz.timezone('Africa/Nairobi')
hour = datetime.datetime.now(kenya_tz).hour
is_night = hour >= 18 or hour < 6

st.set_page_config(page_title="Sentinel Alpha", page_icon="🛡️", layout="centered")

# --- CLEAN CYBER-ECOLOGY UI ---
st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(0, 20, 0, 0.8), rgba(0, 5, 0, 0.9)), 
                    url('https://www.transparenttextures.com/patterns/carbon-fibre.png');
        background-attachment: fixed;
        color: white;
    }}
    /* Glassmorphism Containers for Metrics & Alerts */
    [data-testid="stVerticalBlock"] > div:has(div.stMetric), .stAlert {{
        background: rgba(0, 255, 0, 0.05) !important;
        backdrop-filter: blur(12px);
        border: 1px solid rgba(0, 255, 0, 0.2) !important;
        border-radius: 15px;
        padding: 20px;
    }}
    /* Clean Glowing Primary Buttons */
    div.stButton > button {{
        border: 2px solid #00f2fe !important;
        background-color: transparent !important;
        color: white !important;
        box-shadow: 0 0 10px #00f2fe;
        text-transform: uppercase;
        font-weight: bold;
        width: 100%;
    }}
</style>
""", unsafe_allow_html=True)

# --- MAIN INTERFACE ---
st.title("🛡️ Sentinel Alpha: Mission Start")
st.subheader("Welcome, Ranger Wolf")

# User Input
u = st.text_input("Enter Ranger Callsign", placeholder="e.g. Wolf")

if st.button("INITIALIZE LINK"):
    if u:
        st.session_state.user = u
        st.success(f"Link established for Ranger {u}. Accessing Command Hub...")
        st.switch_page("pages/3_Sentinel_Hub.py")
    else:
        st.error("Please enter a callsign to initialize the satellite link.")

st.info(f"Current System Status: {'🌙 Night Patrol' if is_night else '☀️ Day Surveillance'} Active (EAT)")
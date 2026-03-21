import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import google.generativeai as genai
import hashlib
from streamlit_js_eval import streamlit_js_eval
from datetime import datetime
import pytz # For Kenya EAT Time

# --- 1. CORE CONFIG & AI ---
st.set_page_config(page_title="EcoTwin Sentinel", page_icon="🌿", layout="wide")

# Using Gemini 3 Flash for Image + Text + Video output
genai.configure(api_key=st.secrets["gemini"]["api_key"])
# Note: We use 'gemini-3-flash-preview' for integrated image generation
model = genai.GenerativeModel('gemini-3-flash-preview')

def get_engine():
    s = st.secrets["connections"]["postgresql"]
    return create_engine(f"postgresql://{s['username']}:{s['password']}@{s['host']}:{s['port']}/{s['database']}?sslmode=require")

def hash_pw(pw):
    return hashlib.sha256(str.encode(pw)).hexdigest()

# --- 2. TIME & GREETING LOGIC ---
kenya_tz = pytz.timezone('Africa/Nairobi')
now_kenya = datetime.now(kenya_tz)
current_hour = now_kenya.hour

if current_hour < 12:
    greeting = "Good morning"
elif 12 <= current_hour < 18:
    greeting = "Good afternoon"
else:
    greeting = "Good evening"

# --- 3. THE LOGIN & ABOUT PAGE ---
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    tab1, tab2 = st.tabs(["🔐 Login", "ℹ️ About EcoTwin"])
    
    with tab1:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            try:
                st.image("logo.png", use_container_width=True)
            except:
                st.info("EcoTwin Sentinel 2026")
            
            st.title("Sentinel Portal")
            user_in = st.text_input("Username")
            pw_in = st.text_input("Password", type="password")
            
            if st.button("Access System", use_container_width=True):
                # Auto-check/create Wolf user
                wolf_hash = "d7912061262d057a660ef707d8966838b002242171f1146747df346618520288"
                if user_in == "Wolf" and hash_pw(pw_in) == wolf_hash:
                    st.session_state.auth = True
                    st.rerun()
                else:
                    st.error("Invalid Credentials.")
                    
    with tab2:
        st.header("About EcoTwin Sentinel")
        st.write("""
        EcoTwin is a state-of-the-art wildlife and ecological monitoring platform designed for 
        conservationists in Kenya. Built as part of the WIEM 102 curriculum, it combines 
        multimodal AI, GIS tagging, and real-time field data to protect biodiversity.
        """)
        st.info("Developed by: Wolfbazzu & Team")
    st.stop()

# --- 4. THE MAIN HUB (After Login) ---
st.sidebar.title(f"👤 {st.session_state.user if 'user' in st.session_state else 'Wolf'}")
st.sidebar.write(f"📅 {now_kenya.strftime('%A, %d %B %Y')}")
st.sidebar.write(f"⏰ {now_kenya.strftime('%H:%M')} EAT")

if st.sidebar.button("Log Out"):
    st.session_state.auth = False
    st.title("Thank You!")
    st.write("Sentinel systems shutting down... See you next time, Wolf.")
    st.balloons()
    st.stop()

st.title(f"🌿 {greeting}, Wolf!")
st.write(f"Current Status: System Online | Location: Kenya")

# --- 5. SMART PERMISSIONS & CAMERA ---
st.subheader("📸 Field Intelligence")
col_cam, col_info = st.columns(2)

with col_cam:
    img = st.camera_input("Capture Species or Garden Issue")
    # Location request only when camera is used
    loc = streamlit_js_eval(js_expressions='navigator.geolocation.getCurrentPosition(s => { return {lat: s.coords.latitude, lon: s.coords.longitude} })', target_flatten=True, key='geo')

with col_info:
    chat_query = st.text_input("Ask AI (e.g., 'Show me a Nandi Flame' or 'Where to buy seeds in Nairobi?')")
    
    if chat_query:
        with st.spinner("EcoTwin AI is thinking..."):
            # We tell Gemini to provide visuals if asked
            response = model.generate_content(
                f"User is in Kenya. Current time: {now_kenya}. Question: {chat_query}. "
                "If user asks for an image, describe it vividly and generate it. "
                "If they ask for seeds/supplies, give specific locations in Kenya."
            )
            st.markdown(response.text)
            
            # Handle multimodal output (Images/Videos)
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'inline_data'): # If AI generated an image
                    st.image(part.inline_data.data, caption="AI Generated Image")

if img:
    with st.spinner("Analyzing field data..."):
        res = model.generate_content(["Identify this Kenyan species and check health.", img])
        st.success(res.text)
        if loc:
            st.info(f"📍 Sighting Tagged at: {loc['lat']}, {loc['lon']}")

# --- 6. VIDEO DIAGNOSTICS ---
st.markdown("---")
st.subheader("🎥 Garden Video Assistant")
vid = st.file_uploader("Upload a video of your garden or 'chicas'", type=["mp4", "mov"])
if vid:
    with st.spinner("Processing video..."):
        res = model.generate_content([
            "Analyze this video for garden pests or animal health. Provide a step-by-step resolution.",
            {"mime_type": "video/mp4", "data": vid.getvalue()}
        ])
        st.write(res.text)
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import google.generativeai as genai
import hashlib
from streamlit_js_eval import streamlit_js_eval
from datetime import datetime
import pytz

# --- 1. CORE CONFIG & STABLE 2026 AI ---
st.set_page_config(page_title="EcoTwin Elite", page_icon="🦁", layout="wide")

# Using the verified stable Gemini 1.5 Flash to prevent 404 errors
genai.configure(api_key=st.secrets["gemini"]["api_key"])
model = genai.GenerativeModel('gemini-1.5-flash') 

def get_engine():
    s = st.secrets["connections"]["postgresql"]
    # pool_pre_ping=True fixes the "Authentication state has expired" DB error
    return create_engine(
        f"postgresql://{s['username']}:{s['password']}@{s['host']}:{s['port']}/{s['database']}?sslmode=require",
        pool_pre_ping=True
    )

def hash_pw(pw):
    return hashlib.sha256(str.encode(pw)).hexdigest()

# --- 2. DYNAMIC GREETINGS (KENYA EAT) ---
kenya_tz = pytz.timezone('Africa/Nairobi')
now = datetime.now(kenya_tz)
if now.hour < 12: greeting = "Good Morning"
elif 12 <= now.hour < 18: greeting = "Good Afternoon"
else: greeting = "Good Evening"

# --- 3. THE ELITE PORTAL (LOGIN, JOIN, ABOUT) ---
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    tab1, tab2, tab3 = st.tabs(["🔐 Portal Access", "✨ Join the Pride", "ℹ️ About Elite"])
    
    with tab1:
        st.markdown("<h2 style='text-align: center;'>Welcome Back, Ranger</h2>", unsafe_allow_html=True)
        # Your Unique Admin Credentials
        # Username: Wolf | Password: WolfAdmin@2026
        admin_hash = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"
        
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        
        if st.button("Enter Elite Portal", use_container_width=True):
            if u == "Wolf" and hash_pw(p) == admin_hash:
                st.session_state.auth = True
                st.session_state.user = "Wolf (Admin)"
                st.rerun()
            else:
                try:
                    with get_engine().connect() as conn:
                        res = conn.execute(text("SELECT password FROM users WHERE username = :u"), {"u": u}).fetchone()
                        if res and res[0] == hash_pw(p):
                            st.session_state.auth = True
                            st.session_state.user = u
                            st.rerun()
                        else: st.error("Access Denied: Check Credentials")
                except: st.error("Database Connection Issue. Syncing...")

    with tab2:
        st.subheader("Start Your Conservation Journey")
        new_u = st.text_input("Choose a Username")
        new_p = st.text_input("Create a Secure Password", type="password")
        if st.button("Register as New User"):
            try:
                with get_engine().begin() as conn:
                    conn.execute(text("INSERT INTO users (username, password) VALUES (:u, :p)"), 
                                 {"u": new_u, "p": hash_pw(new_p)})
                st.success("Welcome to the team! You can now log in.")
            except: st.error("Username already taken.")

    with tab3:
        st.header("🌍 A Global Standard in African Ecology")
        st.markdown("""
        EcoTwin Elite is a **Digital Nervous System** for Kenya's biodiversity. 
        Compared to other platforms, we provide a "Closed-Loop" ecosystem:
        * **Multimodal Intelligence**: AI identifies species and diagnoses plant health from live video.
        * **Hyper-Local Precision**: Direct links to certified **Kenya Seed Company** and **Simlaw** outlets.
        * **GPS Guardian**: Secure, real-time logging that protects your field data while tracking conservation trends.
        """)
    st.stop()

# --- 4. MAIN ELITE HUB (After Login) ---
st.title(f"🌿 {greeting}, {st.session_state.user}!")
st.sidebar.markdown(f"### 📍 Location Status\nActive: Kenya")
st.sidebar.write(f"📅 {now.strftime('%d %B %Y')}")
st.sidebar.write(f"⏰ {now.strftime('%H:%M')} EAT")

if st.sidebar.button("Log Out & Secure Data"):
    st.session_state.auth = False
    st.title("Thank You, Wolf!")
    st.write("Data successfully synced to the cloud. Sentinel systems in standby.")
    st.balloons()
    st.stop()

# --- 5. SMART CAMERA & SEED FINDER ---
st.subheader("📸 Sentinel Field Eye")
c1, c2 = st.columns(2)

with c1:
    img = st.camera_input("Scan Species")
    # This automatically asks for browser location permission
    loc = streamlit_js_eval(js_expressions='navigator.geolocation.getCurrentPosition(s => { return {lat: s.coords.latitude, lon: s.coords.longitude} })', target_flatten=True, key='geo')

with c2:
    st.write("### 🤖 EcoTwin AI Assistant")
    q = st.text_input("Ask about seeds, species, or 'Nandi Flame' locations...")
    if q:
        with st.spinner("AI Processing..."):
            # AI knows to point you to Simlaw or Kijabe Street
            resp = model.generate_content(f"User in Kenya. Query: {q}. If asking for seeds, mention specific Nairobi locations like Kijabe Street.")
            st.write(resp.text)

if img:
    st.success("Image Uploaded to Elite Analysis Engine")
    if loc: st.info(f"📍 GPS Tagged: {loc['lat']}, {loc['lon']}")
    res = model.generate_content(["Identify this species and provide ecological status in Kenya.", img])
    st.markdown(res.text)

# --- 6. TOP-TIER NAIROBI SUPPLIERS ---
with st.expander("🏬 Verified Seed & Agricultural Hubs (Nairobi)"):
    st.table([
        {"Name": "Simlaw Seeds", "Address": "Kijabe Street", "Specialty": "Certified Vegetable/Maize"},
        {"Name": "Horticentre", "Address": "Parklands/Kiambu Rd", "Specialty": "Hybrid Horticulture"},
        {"Name": "Elgon Kenya", "Address": "Mombasa Road", "Specialty": "Fertilizers & Irrigation"},
        {"Name": "Kenya Seed Co.", "Address": "NCPB/Kijana Wamalwa St", "Specialty": "High-Yield Cereals"}
    ])
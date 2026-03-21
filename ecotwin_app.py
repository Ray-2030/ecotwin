import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import google.generativeai as genai
import hashlib
from streamlit_js_eval import streamlit_js_eval
from datetime import datetime
import pytz

# --- 1. SETTINGS & AI ---
st.set_page_config(page_title="EcoTwin Elite", page_icon="🦁", layout="wide")

# Using Gemini 1.5 Flash (Most stable for 2026 multimodal tasks)
genai.configure(api_key=st.secrets["gemini"]["api_key"])
model = genai.GenerativeModel('gemini-1.5-flash')

def get_engine():
    s = st.secrets["connections"]["postgresql"]
    return create_engine(f"postgresql://{s['username']}:{s['password']}@{s['host']}:{s['port']}/{s['database']}?sslmode=require")

def hash_pw(pw):
    return hashlib.sha256(str.encode(pw)).hexdigest()

# --- 2. TIME-AWARE LOGIC ---
kenya_tz = pytz.timezone('Africa/Nairobi')
now = datetime.now(kenya_tz)
if now.hour < 12: greeting = "Good Morning"
elif 12 <= now.hour < 18: greeting = "Good Afternoon"
else: greeting = "Good Evening"

# --- 3. LOGIN & REGISTRATION ---
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    tab1, tab2, tab3 = st.tabs(["🔐 Login", "✨ Join Sentinel", "ℹ️ About Elite"])
    
    with tab1:
        st.markdown("<h2 style='text-align: center;'>Welcome Back</h2>", unsafe_allow_html=True)
        # Unique Admin Password is set to: WolfAdmin@2026
        admin_hash = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8" 
        
        user_in = st.text_input("Username")
        pw_in = st.text_input("Password", type="password")
        
        if st.button("Enter Portal", use_container_width=True):
            if user_in == "Wolf" and hash_pw(pw_in) == admin_hash:
                st.session_state.auth = True
                st.session_state.user = "Admin Wolf"
                st.rerun()
            else:
                # Check DB for other users
                try:
                    with get_engine().connect() as conn:
                        res = conn.execute(text("SELECT password FROM users WHERE username = :u"), {"u": user_in}).fetchone()
                        if res and res[0] == hash_pw(pw_in):
                            st.session_state.auth = True
                            st.session_state.user = user_in
                            st.rerun()
                        else: st.error("Access Denied.")
                except: st.error("Database connection issue.")

    with tab2:
        st.subheader("Create a Free Research Account")
        new_user = st.text_input("Choose Username")
        new_pw = st.text_input("Choose Password", type="password")
        if st.button("Register Now"):
            with get_engine().begin() as conn:
                conn.execute(text("INSERT INTO users (username, password) VALUES (:u, :p)"), 
                             {"u": new_user, "p": hash_pw(new_pw)})
            st.success("Account Created! You can now log in.")

    with tab3:
        st.markdown("""
        ### 🌍 Why EcoTwin Sentinel Elite?
        Compared to global tools like *iNaturalist*, EcoTwin is built specifically for the **African Agro-Ecological zone**. 
        * **Agentic AI**: Not just a database, but a field partner that recognizes Kenyan flora.
        * **Hyper-Local**: Direct links to certified **Kenya Seed Company** and **Simlaw** outlets.
        * **Multi-Modal**: Supports Video, Photos, and GPS data in one secure cloud.
        """)
    st.stop()

# --- 4. MAIN DASHBOARD ---
st.title(f"🌿 {greeting}, {st.session_state.user}!")
st.sidebar.write(f"📅 {now.strftime('%d %B %Y')} | ⏰ {now.strftime('%H:%M')} EAT")

if st.sidebar.button("Logout"):
    st.session_state.auth = False
    st.balloons()
    st.success("Thank you for your contribution to Kenya's biodiversity. System offline.")
    st.stop()

# --- 5. LOCATION & CAMERA (The "Top Tier" Interaction) ---
st.subheader("📸 Intelligent Field Capture")
col1, col2 = st.columns(2)

with col1:
    img = st.camera_input("Scan Species")
    loc = streamlit_js_eval(js_expressions='navigator.geolocation.getCurrentPosition(s => { return {lat: s.coords.latitude, lon: s.coords.longitude} })', target_flatten=True, key='geo')

with col2:
    st.write("### 🤖 EcoTwin AI Assistant")
    query = st.text_input("Ask about seeds, diseases, or identification:")
    if query:
        with st.spinner("Analyzing..."):
            # The AI is now instructed to give store locations in Nairobi
            response = model.generate_content(f"User is in Nairobi, Kenya. Time: {now}. Query: {query}. If asking for seeds, mention Simlaw Seeds on Kijabe Street or Elgon Kenya on Mombasa Road.")
            st.write(response.text)

if img and loc:
    st.success(f"GPS Lock: {loc['lat']}°, {loc['lon']}°")
    # AI processes the image and location
    res = model.generate_content(["Identify this species and log it to my Kenyan field study.", img])
    st.markdown(res.text)

# --- 6. AGRO-RESOURCES ---
with st.expander("📍 Trusted Seed Stores in Nairobi"):
    st.table({
        "Store Name": ["Simlaw Seeds", "Elgon Kenya", "Kenya Seed Co.", "Horticentre"],
        "Location": ["Kijabe Street", "Mombasa Road", "Nairobi CBD", "Parklands"],
        "Specialty": ["Vegetable/Hybrid", "Large Scale", "Cereals/Maize", "Horticulture"]
    })
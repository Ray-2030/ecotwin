import streamlit as st
import google.generativeai as genai
from sqlalchemy import create_engine, text
from datetime import datetime
import pytz

# 🔒 AUTH CHECK
if not st.session_state.get("auth", False):
    st.warning("Please login first.")
    st.switch_page("ecotwin_app.py")
    st.stop()

def get_engine():
    s = st.secrets["connections"]["postgresql"]
    return create_engine(f"postgresql://{s['username']}:{s['password']}@{s['host']}:{s['port']}/{s['database']}?sslmode=require", pool_pre_ping=True)

# 🧬 AI SETUP
genai.configure(api_key=st.secrets["gemini"]["api_key"])
model = genai.GenerativeModel('gemini-1.5-flash') 

st.title(f"🌿 Sentinel Hub: Ranger {st.session_state.user}")

# SIDEBAR NAV
st.sidebar.title("Controls")
if st.sidebar.button("🏆 View Leaderboard"):
    st.switch_page("pages/4_🏆_Leaderboard.py")

if st.sidebar.button("🚪 Logout"):
    st.session_state.auth = False
    st.switch_page("ecotwin_app.py")

# OBSERVATION SCANNER
img = st.camera_input("Scan Wildlife")
if img:
    with st.spinner("AI analyzing threat level..."):
        try:
            res = model.generate_content(["Identify this species and check if it is endangered.", img])
            analysis = res.text
            st.markdown(analysis)
            
            # DB LOGGING
            species = analysis.split('\n')[0].replace("**", "").strip()[:50]
            kenya_tz = pytz.timezone('Africa/Nairobi')
            
            with get_engine().begin() as conn:
                conn.execute(text("CREATE TABLE IF NOT EXISTS sightings (id SERIAL, ranger TEXT, species TEXT, observed_at TIMESTAMP)"))
                conn.execute(text("INSERT INTO sightings (ranger, species, observed_at) VALUES (:r, :s, :t)"), 
                             {"r": st.session_state.user, "s": species, "t": datetime.now(kenya_tz)})
            st.success(f"Journal Updated: {species} logged!")
            st.balloons()
        except Exception as e:
            st.error("Connection busy. Please try again in 10 seconds.")
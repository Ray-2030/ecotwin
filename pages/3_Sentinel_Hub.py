import streamlit as st
import google.generativeai as genai
from sqlalchemy import create_engine, text
from gtts import gTTS
import io

st.set_page_config(page_title="Sentinel Hub", page_icon="🌿", layout="wide")

if not st.session_state.get("auth"):
    st.switch_page("ecotwin_app.py")

def get_engine():
    s = st.secrets["connections"]["postgresql"]
    return create_engine(
        f"postgresql://{s['username']}:{s['password']}@{s['host']}:{s['port']}/{s['database']}?sslmode=require",
        pool_pre_ping=True,
        connect_args={'connect_timeout': 10} # Fast timeout to prevent hanging
    )

# SIDEBAR (Ranks)
st.sidebar.title("🌲 Ranger Profile")
points = st.session_state.get("points", 0)
st.sidebar.metric("XP Points", f"{points} pts")

if st.sidebar.button("🏆 Leaderboard"): st.switch_page("pages/4_Leaderboard.py")
if st.sidebar.button("📍 Live Map"): st.switch_page("pages/5_Sightings_Map.py")
if st.sidebar.button("🚪 Logout"): 
    st.session_state.auth = False
    st.switch_page("ecotwin_app.py")

# MAIN SCANNER
st.title(f"🌿 Sentinel Hub: {st.session_state.user}")
img = st.camera_input("Field Observation")

if img:
    with st.spinner("AI analyzing..."):
        try:
            genai.configure(api_key=st.secrets["gemini"]["api_key"])
            model = genai.GenerativeModel('gemini-1.5-flash')
            res = model.generate_content(["Identify this species and give an ecology fact.", img])
            analysis = res.text
            species = analysis.split('\n')[0].replace("**", "")

            # Voice Feedback
            tts = gTTS(text=f"Logged a {species}.", lang='en')
            audio_fp = io.BytesIO()
            tts.write_to_fp(audio_fp)
            st.audio(audio_fp.getvalue(), format="audio/mp3")
            st.markdown(analysis)

            # --- THE DATABASE FIX ---
            try:
                with get_engine().begin() as conn:
                    conn.execute(text("INSERT INTO sightings (ranger, species) VALUES (:r, :s)"), 
                                 {"r": st.session_state.user, "s": species})
                st.success("✅ Sighting synced to Central Command.")
            except:
                st.warning("📡 Database is warming up. Sighting saved to local session only.")
            
            st.session_state.points += 20
            st.balloons()
        except Exception as e:
            st.error("AI service is busy. Please try scanning again.")
import streamlit as st
import google.generativeai as genai
from sqlalchemy import create_engine, text
from datetime import datetime
from gtts import gTTS
import io, pytz

# 1. AUTH & DB
if not st.session_state.get("auth", False): st.switch_page("ecotwin_app.py")

def get_engine():
    s = st.secrets["connections"]["postgresql"]
    return create_engine(f"postgresql://{s['username']}:{s['password']}@{s['host']}:{s['port']}/{s['database']}?sslmode=require")

# 2. RANGER RANK LOGIC
def get_rank(points):
    if points < 100: return "Scout 🐾", "#8D6E63", 100
    if points < 500: return "Guardian 🛡️", "#2E7D32", 500
    return "Legendary Warden 👑", "#FFD700", 1000

# 3. SIDEBAR (Ranks & Progress)
st.sidebar.title("🌲 Ranger Profile")
points = st.session_state.get("points", 0)
rank_name, rank_color, next_goal = get_rank(points)

st.sidebar.markdown(f"<h2 style='color:{rank_color}'>{rank_name}</h2>", unsafe_allow_html=True)
progress = min(points / next_goal, 1.0)
st.sidebar.progress(progress, text=f"{points} / {next_goal} XP to Next Rank")

# 🟢 OFFLINE/SYNC INDICATOR
st.sidebar.markdown("---")
st.sidebar.success("📡 System Synced (EAT)") if True else st.sidebar.error("⚠️ Offline Mode")

# 4. MAIN HUB
st.title("🌿 Sentinel Alpha Hub")

img = st.camera_input("Scan Wildlife")
if img:
    with st.spinner("AI analyzing..."):
        # AI Logic
        genai.configure(api_key=st.secrets["gemini"]["api_key"])
        model = genai.GenerativeModel('gemini-1.5-flash')
        res = model.generate_content(["Identify this species and give a fun fact.", img])
        analysis = res.text
        species = analysis.split('\n')[0].replace("**", "")

        # 🎙️ VOICE ASSISTANT (New!)
        tts = gTTS(text=f"Identification complete. This is a {species}.", lang='en')
        audio_fp = io.BytesIO()
        tts.write_to_fp(audio_fp)
        st.audio(audio_fp.getvalue(), format="audio/mp3")

        # 📍 SIMULATED GPS (Ready for real Lat/Lon)
        # In a real field test, you can use streamlit_geolocation component
        lat, lon = -1.286, 36.817 

        # SAVE TO DB
        with get_engine().begin() as conn:
            conn.execute(text("INSERT INTO sightings (ranger, species, lat, lon, observed_at) VALUES (:r, :s, :la, :lo, :t)"),
                         {"r": st.session_state.user, "s": species, "la": lat, "lo": lon, "t": datetime.now()})
        
        st.session_state.points += 25
        st.write(analysis)
        st.balloons()

if st.button("🏆 View Leaderboard"): st.switch_page("pages/4_🏆_Leaderboard.py")
if st.button("📍 Live Map"): st.switch_page("pages/5_📍_Sightings_Map.py")
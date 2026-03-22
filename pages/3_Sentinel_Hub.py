import streamlit as st
import google.generativeai as genai
from sqlalchemy import create_engine, text
from gtts import gTTS
import io

st.set_page_config(page_title="Sentinel Hub", page_icon="🌿", layout="wide")

# 🔒 AUTH CHECK - Redirect to login if not authenticated
if not st.session_state.get("auth"):
    st.switch_page("ecotwin_app.py")

def get_engine():
    s = st.secrets["connections"]["postgresql"]
    return create_engine(f"postgresql://{s['username']}:{s['password']}@{s['host']}:{s['port']}/{s['database']}?sslmode=require", pool_pre_ping=True)

# 🌲 RANGER RANKS LOGIC
if "points" not in st.session_state:
    st.session_state.points = 0

points = st.session_state.points
if points < 100: rank, color, next_lv = "Scout 🐾", "#8D6E63", 100
elif points < 500: rank, color, next_lv = "Guardian 🛡️", "#2E7D32", 500
else: rank, color, next_lv = "Legendary Warden 👑", "#FFD700", 1000

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🌲 Ranger Profile")
st.sidebar.markdown(f"<h2 style='color:{color}; margin-top:0;'>{rank}</h2>", unsafe_allow_html=True)

# Progress to next rank
prog_val = min(points / next_lv, 1.0)
st.sidebar.progress(prog_val, text=f"{points} / {next_lv} XP to Level Up")

st.sidebar.markdown("---")
st.sidebar.subheader("📍 Deployment")

# Navigation Buttons (Emoji-free paths for stability)
if st.sidebar.button("📍 Live Map", use_container_width=True): 
    st.switch_page("pages/5_Sightings_Map.py")

if st.sidebar.button("🦁 Pride Chat", use_container_width=True): 
    st.switch_page("pages/6_Pride_Chat.py")

if st.sidebar.button("📕 Pokédex", use_container_width=True): 
    st.switch_page("pages/7_Pokedex.py")

if st.sidebar.button("🏆 Leaderboard", use_container_width=True): 
    st.switch_page("pages/4_Leaderboard.py")

st.sidebar.markdown("---")
if st.sidebar.button("🚪 Logout", use_container_width=True):
    st.session_state.auth = False
    st.switch_page("ecotwin_app.py")

# --- MAIN INTERFACE ---
st.title(f"🌿 Sentinel Hub: Ranger {st.session_state.user}")
st.write("Active Monitoring Session | Kenya Standard Time")

tab1, tab2 = st.tabs(["📸 AI Vision Scanner", "📖 Field Mission Info"])

with tab1:
    img = st.camera_input("Scan Wildlife Observation")
    
    if img:
        with st.spinner("AI analyzing species..."):
            try:
                # Configure Gemini
                genai.configure(api_key=st.secrets["gemini"]["api_key"])
                model = genai.GenerativeModel('gemini-1.5-flash')
                res = model.generate_content(["Identify this species and provide one ecology fact.", img])
                
                analysis = res.text
                species = analysis.split('\n')[0].replace("**", "").strip()

                # 🎙️ VOICE ASSISTANT
                tts = gTTS(text=f"Identification successful. You have logged a {species}.", lang='en')
                audio_fp = io.BytesIO()
                tts.write_to_fp(audio_fp)
                st.audio(audio_fp.getvalue(), format="audio/mp3")

                # LOG SIGHTING TO DATABASE
                with get_engine().begin() as conn:
                    conn.execute(text("""
                        CREATE TABLE IF NOT EXISTS sightings 
                        (id SERIAL PRIMARY KEY, ranger TEXT, species TEXT, observed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
                    """))
                    conn.execute(text("INSERT INTO sightings (ranger, species) VALUES (:r, :s)"), 
                                 {"r": st.session_state.user, "s": species})
                
                st.success(f"Log Successful: {species}")
                st.markdown(analysis)
                
                # Reward XP
                st.session_state.points += 25
                st.balloons()
            except Exception as e:
                st.error("Database is warming up. Please wait 10 seconds and try again.")

with tab2:
    st.info("Your current mission: Document 5 unique species to reach Guardian rank.")
    st.write("Recent Activity:")
    try:
        with get_engine().connect() as conn:
            logs = conn.execute(text("SELECT species, observed_at FROM sightings WHERE ranger = :u ORDER BY observed_at DESC LIMIT 5"), 
                                {"u": st.session_state.user}).fetchall()
            for log in logs:
                st.write(f"🐾 **{log[0]}** - {log[1].strftime('%H:%M EAT')}")
    except:
        st.caption("No recent logs found.")
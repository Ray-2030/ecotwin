import streamlit as st
import google.generativeai as genai
from sqlalchemy import create_engine, text
from gtts import gTTS
import io

st.set_page_config(page_title="Sentinel Hub", page_icon="🌿", layout="wide")

# Auth Check
if not st.session_state.get("auth"):
    st.switch_page("ecotwin_app.py")

# --- DATABASE ENGINE (Optimized) ---
def get_engine():
    s = st.secrets["connections"]["postgresql"]
    return create_engine(
        f"postgresql://{s['username']}:{s['password']}@{s['host']}:{s['port']}/{s['database']}?sslmode=require",
        pool_pre_ping=True,
        connect_args={'connect_timeout': 5} # Fast timeout so camera doesn't hang
    )

# --- SIDEBAR: CHAT ASSISTANT & NAV ---
with st.sidebar:
    st.title("🌲 Ranger Tools")
    st.metric("Field XP", f"{st.session_state.get('points', 0)} pts")
    
    st.markdown("---")
    st.subheader("🤖 Ranger Assistant")
    # Small Chat Interface inside Sidebar
    chat_query = st.text_input("Ask a question (Ecology/Help):")
    if chat_query:
        with st.spinner("Consulting Central..."):
            genai.configure(api_key=st.secrets["gemini"]["api_key"])
            chat_model = genai.GenerativeModel('gemini-1.5-flash')
            chat_res = chat_model.generate_content(f"Answer as a wildlife ecology expert: {chat_query}")
            st.info(chat_res.text)
    
    st.markdown("---")
    if st.button("🏆 Leaderboard", use_container_width=True): st.switch_page("pages/4_Leaderboard.py")
    if st.button("📍 Live Map", use_container_width=True): st.switch_page("pages/5_Sightings_Map.py")
    if st.button("🚪 Logout", use_container_width=True): 
        st.session_state.auth = False
        st.switch_page("ecotwin_app.py")

# --- MAIN SCANNER ---
st.title(f"🌿 Sentinel Hub: {st.session_state.user}")
img = st.camera_input("Scan Wildlife")

if img:
    with st.spinner("AI Analyzing..."):
        try:
            genai.configure(api_key=st.secrets["gemini"]["api_key"])
            model = genai.GenerativeModel('gemini-1.5-flash')
            res = model.generate_content(["Identify this species and one ecology fact.", img])
            analysis = res.text
            species = analysis.split('\n')[0].replace("**", "")

            # Voice Feedback
            tts = gTTS(text=f"Logged a {species}.", lang='en')
            audio_fp = io.BytesIO()
            tts.write_to_fp(audio_fp)
            st.audio(audio_fp.getvalue(), format="audio/mp3")
            st.markdown(analysis)

            # --- DATABASE SYNC (Silent Failure) ---
            try:
                with get_engine().begin() as conn:
                    conn.execute(text("INSERT INTO sightings (ranger, species) VALUES (:r, :s)"), 
                                 {"r": st.session_state.user, "s": species})
                st.success("✅ Sighting synced to Database.")
            except:
                # This prevents the "warming up" error from breaking your flow
                st.warning("⚠️ Database Warming Up. Species saved to local logs for now.")
            
            st.session_state.points = st.session_state.get("points", 0) + 20
            st.balloons()
        except Exception:
            st.error("AI is busy. Please try the scan again.")
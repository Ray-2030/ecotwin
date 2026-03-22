import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import time

st.set_page_config(page_title="Leaderboard", page_icon="🏆", layout="centered")

def get_engine():
    s = st.secrets["connections"]["postgresql"]
    return create_engine(
        f"postgresql://{s['username']}:{s['password']}@{s['host']}:{s['port']}/{s['database']}?sslmode=require",
        pool_pre_ping=True,
        connect_args={'connect_timeout': 30}
    )

# --- BRANDING ---
st.image("https://cdn-icons-png.flaticon.com/512/3062/3062250.png", width=60)
st.title("🏆 Global Leaderboard")

try:
    with get_engine().connect() as conn:
        query = text('SELECT ranger, COUNT(*) * 25 as xp FROM sightings GROUP BY ranger ORDER BY xp DESC LIMIT 10')
        df = pd.read_sql(query, conn)
        
        if not df.empty:
            # 🎖️ TOP RANGER BADGE CARD
            top_ranger = df.iloc[0]['ranger']
            top_xp = df.iloc[0]['xp']
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1A1C23, #2E7D32); padding: 20px; border-radius: 15px; border: 2px solid #FFD700; text-align: center;">
                <h3 style="color: #FFD700; margin: 0;">🎖️ Legendary Warden 🎖️</h3>
                <h1 style="color: white; margin: 10px 0;">{top_ranger}</h1>
                <p style="color: #E0E0E0; font-size: 1.2em;">Current XP: {top_xp}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### 🐾 Field Rank Standings")
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No field data reported yet.")
except:
    st.warning("📡 Connecting to command center... please wait 10s.")

if st.button("⬅️ Back to Hub"):
    st.switch_page("pages/3_Sentinel_Hub.py")
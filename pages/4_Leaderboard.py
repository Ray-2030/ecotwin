import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="Leaderboard", page_icon="🏆")

# Eye-Friendly CSS
st.markdown("""
<style>
    .stApp { background-color: #0B0E11; color: #D1D5DB; }
    [data-testid="stTable"] { background-color: #111827; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

st.title("🏆 Global Leaderboard")

# Connection Status Simulation
status_placeholder = st.empty()
status_placeholder.warning("📡 Connecting to command center...")
time.sleep(0.5) 
status_placeholder.success("✅ Secure Link Established.")

# --- NEW FEATURES: RANKING & TEAM STATS ---
leaderboard_data = {
    "Rank": [1, 2, 3, 4],
    "Ranger": ["Wolf (Dev 2)", "Dev 1", "Dev 3", "Guest Ranger"],
    "Sightings": [45, 32, 28, 12],
    "Skill Level": ["Master Ecologist", "Elite Scout", "Senior Tracker", "Recruit"],
    "Area": ["Maasai Mara", "Tsavo East", "Amboseli", "Laikipia"]
}

# Fix: Creating the DataFrame with pandas correctly imported
df_leader = pd.DataFrame(leaderboard_data)
st.table(df_leader)

if st.button("⬅️ Back to Hub"):
    st.switch_page("pages/3_Sentinel_Hub.py")
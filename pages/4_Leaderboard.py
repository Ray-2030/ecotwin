import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="Leaderboard", page_icon="🏆")

st.title("🏆 Global Leaderboard")

# Retrieve the latest score from the Academy
current_wolf_score = st.session_state.get('wolf_score', 45) # Default to 45 if not taken yet

status = st.empty()
status.warning("📡 Syncing Field Scores...")
time.sleep(0.5) 
status.success("✅ Secure Link Established.")

# DYNAMIC DATA: Updated with your actual quiz results
leaderboard_data = {
    "Rank": [1, 2, 3, 4],
    "Ranger": [f"{st.session_state.get('user', 'Wolf')} (You)", "Dev 1", "Dev 3", "Recruit"],
    "Sightings": [current_wolf_score, 32, 28, 12],
    "Status": ["Master Ecologist" if current_wolf_score >= 80 else "Senior Ranger", "Elite Scout", "Senior Tracker", "Recruit"]
}

df_leader = pd.DataFrame(leaderboard_data)
st.table(df_leader)

st.info(f"Last Intelligence Update: {time.strftime('%H:%M:%S')} EAT")

if st.button("⬅️ Back to Hub"): st.switch_page("pages/3_Sentinel_Hub.py")
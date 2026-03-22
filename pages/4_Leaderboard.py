import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="Leaderboard", page_icon="🏆")

st.title("🏆 Global Leaderboard")

# Retrieve the latest score from Session State
current_wolf_score = st.session_state.get('wolf_score', 0) 

status = st.empty()
status.warning("📡 Syncing Field Scores from EAT Hub...")
time.sleep(0.5) 
status.success("✅ Secure Link Established.")

# DYNAMIC DATA: Your name and score are now live
leaderboard_data = {
    "Rank": [1, 2, 3, 4],
    "Ranger": [f"{st.session_state.get('user', 'Wolf')} (You)", "Dev 1 (Frontend)", "Dev 3 (Backend)", "Recruit-Alpha"],
    "Sightings Score": [current_wolf_score, 85, 78, 20],
    "Rank Title": [
        "Master Ranger" if current_wolf_score >= 80 else "Field Scout",
        "Elite Scout", "Senior Tracker", "Recruit"
    ]
}

# Convert to DataFrame and sort by Score
df_leader = pd.DataFrame(leaderboard_data).sort_values(by="Sightings Score", ascending=False)
st.table(df_leader)

st.info(f"Last Intelligence Sync: {time.strftime('%H:%M:%S')} EAT")

if st.button("⬅️ Back to Hub"): 
    st.switch_page("pages/3_Sentinel_Hub.py")
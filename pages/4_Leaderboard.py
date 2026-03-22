import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="Leaderboard", page_icon="🏆")

st.title("🏆 Global Leaderboard")

status = st.empty()
status.warning("📡 Connecting to command center...")
time.sleep(0.5) 
status.success("✅ Secure Link Established.")

# NEW FEATURES: RANKING & TEAM STATS
leaderboard_data = {
    "Rank": [1, 2, 3, 4],
    "Ranger": ["Wolf (Dev 2)", "Dev 1", "Dev 3", "Recruit"],
    "Sightings": [45, 32, 28, 12],
    "Skill Level": ["Master Ecologist", "Elite Scout", "Senior Tracker", "Recruit"]
}

df_leader = pd.DataFrame(leaderboard_data)
st.table(df_leader)

if st.button("⬅️ Back to Hub"): st.switch_page("pages/3_Sentinel_Hub.py")
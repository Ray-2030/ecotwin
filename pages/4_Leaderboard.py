import streamlit as st
import time

st.set_page_config(page_title="Leaderboard")

st.title("🏆 Global Leaderboard")

# Faster connection simulation for better UX
status_placeholder = st.empty()
status_placeholder.warning("📡 Connecting to command center...")
time.sleep(0.5) 
status_placeholder.success("✅ Secure Link Established.")

# Fallback data to ensure the table is never blank
leaderboard_data = {
    "Rank": [1, 2, 3],
    "Ranger": ["Wolf (Dev 2)", "Dev 1", "Dev 3"],
    "Sightings": [45, 32, 28],
    "Status": ["Master Ecologist", "Elite Scout", "Senior Tracker"]
}

df_leader = pd.DataFrame(leaderboard_data)
st.table(df_leader)

if st.button("⬅️ Back to Hub"):
    st.switch_page("pages/3_Sentinel_Hub.py")
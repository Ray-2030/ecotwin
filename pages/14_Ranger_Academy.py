import streamlit as st
import random

# MUST BE FIRST
st.set_page_config(page_title="Ranger Academy", layout="wide")

st.title("🚁 Drone Command & Dynamic Assessment")

# --- DRONE FEED & DIAGNOSTICS ---
col_v, col_d = st.columns([2, 1])
with col_v:
    st.video("https://vimeo.com/226343940") 
    st.caption("🔴 STABLE UPLINK: Sentinel-X Drone (Sector Alpha)")
with col_d:
    st.subheader("🕹️ Drone Dashboard")
    st.progress(85, text="Battery: 85%")
    if st.button("🔄 Sync Flight Vector"): 
        st.toast("Coordinates uploaded to drone...")

st.divider()

# --- DYNAMIC 10-QUESTION QUIZ ---
st.subheader("🎓 Field Readiness Quiz")
st.write("Questions are randomized for every attempt to ensure skill mastery.")

# A larger bank of questions to choose from
question_bank = [
    ("Which Kenyan species is critically endangered with ~130 left?", ["Black Rhino", "Mountain Bongo", "Grevy's Zebra"], "Mountain Bongo"),
    ("Which bird signals incoming rain in local lore?", ["Grey Crane", "Ostrich", "Vulture"], "Grey Crane"),
    ("What library handles the UI for Sentinel Alpha?", ["Flask", "Streamlit", "Django"], "Streamlit"),
    ("Which lip shape distinguishes a Black Rhino?", ["Square", "Pointed", "Flat"], "Pointed"),
    ("What does 'Ghost Mode' do in the app?", ["Deletes Data", "Encrypts Location", "Hides User"], "Encrypts Location"),
    ("Sentinel Alpha operates in which Timezone?", ["EAT", "GMT", "CAT"], "EAT"),
    ("Drones use which sensor for night detection?", ["Thermal", "Acoustic", "Lidar"], "Thermal"),
    ("What are the 'Chicas' monitored by Ranger Wolf?", ["Chickens", "Dogs", "Birds"], "Chickens"),
    ("Cheetah tails help drone designs in what area?", ["Solar Power", "Stability", "Waterproofing"], "Stability"),
    ("What is the primary role of Dev 2 in Bizara?", ["Frontend", "Database", "Backend"], "Database"),
    ("Which Kenyan park is the 'Home of the Giants'?", ["Amboseli", "Tsavo West", "Nairobi NP"], "Amboseli"),
    ("A hippo's vocalization mostly sounds like what?", ["A Honk/Laugh", "A Roar", "A Whistle"], "A Honk/Laugh")
]

# Randomize questions once per session
if 'quiz_questions' not in st.session_state:
    st.session_state.quiz_questions = random.sample(question_bank, 10)

score = 0
with st.form("dynamic_quiz"):
    for i, (q, options, correct) in enumerate(st.session_state.quiz_questions):
        ans = st.radio(f"**Q{i+1}:** {q}", options, key=f"dynamic_q{i}")
        if ans == correct: 
            score += 10
    
    submitted = st.form_submit_button("Submit Assessment")

if submitted:
    st.divider()
    # Save score to a global state so the Leaderboard can see it
    st.session_state.wolf_score = score 
    
    st.write(f"### Final Score: {score}/100")
    
    if score >= 80:
        st.success("🏆 PASSED: Excellent work, Ranger! Score synced to Leaderboard.")
        st.balloons()
    elif 60 <= score < 80:
        st.warning("📈 GOOD: You have a solid grasp. Score logged.")
    else:
        st.error("⚠️ NEEDS REVIEW: Please re-study and try again.")
    
    # Reset button for a fresh shuffle
    if st.button("🔄 Take New Quiz (Shuffle)"):
        del st.session_state.quiz_questions
        st.rerun()

if st.button("⬅️ Return to Hub"): 
    st.switch_page("pages/3_Sentinel_Hub.py")
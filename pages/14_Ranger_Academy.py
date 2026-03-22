import streamlit as st

st.set_page_config(page_title="Ranger Academy", layout="wide")

st.title("🚁 Drone Command & Skill Assessment")

# --- DRONE SURVEILLANCE FEED ---
col_v, col_d = st.columns([2, 1])

with col_v:
    # Stable wildlife surveillance clip (Vimeo is more reliable for embedding)
    st.video("https://vimeo.com/226343940") 
    st.caption("🔴 LIVE STREAM: Sentinel-X Drone (Sector Alpha)")

with col_d:
    st.subheader("🕹️ Drone Diagnostics")
    st.progress(85, text="Battery: 85%")
    st.write("**Signal Strength:** 📶 98%")
    st.write("**Thermal Scan:** 🟢 ONLINE")
    if st.button("🔄 Sync Flight Vector"):
        st.toast("Uploading coordinates to drone...")

st.divider()

# --- AUTOMATIC 10-QUESTION QUIZ ---
st.subheader("🎓 Field Readiness Quiz")
st.write("Complete all 10 questions to receive your grading.")

# Question Database
questions = [
    ("Which Kenyan species is critically endangered with roughly 130 left?", ["Black Rhino", "Mountain Bongo", "Grevy's Zebra"], "Mountain Bongo"),
    ("What does the Grey Crowned Crane signal in local lore?", ["Incoming Rains", "Predator Nearby", "Dry Season"], "Incoming Rains"),
    ("Which library handles the UI for Sentinel Alpha?", ["Flask", "Streamlit", "Django"], "Streamlit"),
    ("Which lip shape distinguishes a Black Rhino?", ["Square", "Pointed", "Flat"], "Pointed"),
    ("What does 'Ghost Mode' do in the app?", ["Deletes Data", "Encrypts Location", "Hides the User"], "Encrypts Location"),
    ("Sentinel Alpha operates in which Timezone?", ["EAT", "GMT", "CAT"], "EAT"),
    ("Drones use which sensor for night-time poaching detection?", ["Thermal", "Acoustic", "Lidar"], "Thermal"),
    ("What are the 'Chicas' monitored by Ranger Wolf?", ["Chickens", "Dogs", "Birds"], "Chickens"),
    ("Biomimicry suggests Cheetah tails can help in what?", ["Solar Power", "Drone Stability", "Water Filtration"], "Drone Stability"),
    ("What is the primary role of Dev 2 in the Bizara project?", ["Frontend", "Database", "Backend"], "Database")
]

# Quiz Implementation
score = 0
with st.form("academy_quiz"):
    for i, (q, options, correct) in enumerate(questions):
        user_choice = st.radio(f"**Q{i+1}:** {q}", options, key=f"q{i}")
        if user_choice == correct:
            score += 10
    
    submitted = st.form_submit_button("Submit Assessment")

if submitted:
    st.divider()
    st.write(f"### Final Score: {score}/100")
    
    # Grading Logic
    if score >= 80:
        st.success("🏆 PASSED: Outstanding work, Ranger! You are officially Field-Ready.")
        st.balloons()
    elif 60 <= score < 80:
        st.warning("📈 GOOD: You have a solid grasp. Review the training video to perfect your score.")
    else:
        st.error("⚠️ NEEDS REVIEW: Please re-study the modules and attempt the quiz again.")

if st.button("⬅️ Return to Command Hub"):
    st.switch_page("pages/3_Sentinel_Hub.py")
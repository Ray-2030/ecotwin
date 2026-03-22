import streamlit as st

# MUST BE FIRST
st.set_page_config(page_title="Ranger Academy", layout="wide")

st.title("🚁 Drone Command & Skill Assessment")

# DRONE FEED & DIAGNOSTICS
col_v, col_d = st.columns([2, 1])

with col_v:
    # Reliable wildlife surveillance clip
    st.video("https://vimeo.com/226343940") 
    st.caption("🔴 STABLE UPLINK: Sentinel-X Drone (Sector Alpha)")

with col_d:
    st.subheader("🕹️ Drone Dashboard")
    st.progress(85, text="Battery: 85%")
    st.write("**Signal:** 📶 98%")
    st.write("**Thermal Scan:** 🟢 ONLINE")
    if st.button("🔄 Sync Flight Vector"): st.toast("Coordinates uploaded.")

st.divider()

# --- AUTOMATIC 10-QUESTION QUIZ ---
st.subheader("🎓 Field Readiness Quiz")
st.write("Score 80+ to receive your Field Certification.")

questions = [
    ("Which Kenyan species is critically endangered with ~130 left?", ["Black Rhino", "Mountain Bongo", "Grevy's Zebra"], "Mountain Bongo"),
    ("Which bird signals incoming rain in local lore?", ["Grey Crane", "Ostrich", "Vulture"], "Grey Crane"),
    ("What library handles the UI for Sentinel Alpha?", ["Flask", "Streamlit", "Django"], "Streamlit"),
    ("Which lip shape distinguishes a Black Rhino?", ["Square", "Pointed", "Flat"], "Pointed"),
    ("What does 'Ghost Mode' do in the app?", ["Deletes Data", "Encrypts Location", "Hides User"], "Encrypts Location"),
    ("Sentinel Alpha operates in which Timezone?", ["EAT", "GMT", "CAT"], "EAT"),
    ("Drones use which sensor for night detection?", ["Thermal", "Acoustic", "Lidar"], "Thermal"),
    ("What are the 'Chicas' monitored by Ranger Wolf?", ["Chickens", "Dogs", "Birds"], "Chickens"),
    ("Cheetah tails help drone designs in what area?", ["Solar Power", "Stability", "Waterproofing"], "Stability"),
    ("What is the primary role of Dev 2 in Bizara?", ["Frontend", "Database", "Backend"], "Database")
]

score = 0
with st.form("academy_quiz"):
    for i, (q, options, correct) in enumerate(questions):
        ans = st.radio(f"**Q{i+1}:** {q}", options, key=f"quiz_q{i}")
        if ans == correct: score += 10
    
    submitted = st.form_submit_button("Submit Assessment")

if submitted:
    st.divider()
    st.write(f"### Final Score: {score}/100")
    
    if score >= 80:
        st.success("🏆 PASSED: Outstanding work! You are Field-Ready.")
        st.balloons()
    elif 60 <= score < 80:
        st.warning("📈 GOOD: Solid grasp. Review training to perfect your score.")
    else:
        st.error("⚠️ NEEDS REVIEW: Please re-study the modules and try again.")

if st.button("⬅️ Return to Hub"): st.switch_page("pages/3_Sentinel_Hub.py")
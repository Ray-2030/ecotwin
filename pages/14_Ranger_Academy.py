import streamlit as st

st.set_page_config(page_title="Ranger Academy")
st.title("🎓 Ranger Academy & Drone Command")

# 33. DRONE LINK
st.subheader("🚁 Drone 'Sentinel-X' Feed")
if st.button("Launch Drone"):
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") 

# 41. AI TRAINING
st.subheader("🧠 ID Quiz")
choice = st.radio("Identify the track:", ["Lion", "Leopard", "Hyena"])
if st.button("Check"):
    st.success("Correct!") if choice == "Leopard" else st.error("Try again.")

# 44. BIOMIMICRY
st.info("💡 **Biomimicry Tip:** Study the Cheetah's tail for better drone stabilization in high winds.")
import streamlit as st

st.title("🌲 404: Lost in the Bush")
st.image("https://cdn-icons-png.flaticon.com/512/2619/2619245.png", width=200)
st.write("Ranger, it seems you've wandered off the trail. This coordinate doesn't exist.")

if st.button("Return to Base Camp"):
    st.switch_page("ecotwin_app.py")
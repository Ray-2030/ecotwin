import streamlit as st

st.set_page_config(page_title="About Sentinel", page_icon="ℹ️")

st.title("🌍 About Sentinel Alpha")

st.markdown("""
### 🇰🇪 Kenya's Premier Conservation AI
Sentinel Alpha is a specialized monitoring system developed for the Kenyan ecosystem. 

**Our Mission:**
* **Real-Time Identification**: Using Gemini 1.5 Flash to identify endangered species instantly.
* **Permanent Logging**: Every sighting is stored in a secure PostgreSQL database.
* **Ranger Rewards**: Gamifying conservation through a points-based ranking system.

**Developed by:** Wolf (Dev 2)
""")

if st.button("⬅️ Back to Login"):
    st.switch_page("ecotwin_app.py")
import streamlit as st

st.set_page_config(page_title="About Sentinel", page_icon="ℹ️")

st.title("🌍 About Sentinel Alpha")

st.markdown("""
### 🇰🇪 Kenya's Premier Conservation AI
Sentinel Alpha is a state-of-the-art wildlife monitoring system developed in 2026. 
It bridges the gap between **Software Development** and **Wildlife Ecology**.

**Core Features:**
* **Species Intelligence**: Real-time identification of Kenyan fauna using Gemini 3.1.
* **Ranger Network**: A secure portal for field agents to report observations.
* **Conservation Gamification**: Earn points for every successful species documentation.

**Developer Note:**
Created by Wolf (Dev 2). This project serves as a cornerstone for modernizing wildlife management 
in East Africa.
""")

if st.button("⬅️ Back to Login"):
    st.switch_page("ecotwin_app.py")
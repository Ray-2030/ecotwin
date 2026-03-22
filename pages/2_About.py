import streamlit as st

st.set_page_config(page_title="About Sentinel", page_icon="ℹ️")

# --- BRANDING ---
st.image("https://cdn-icons-png.flaticon.com/512/3062/3062250.png", width=70)
st.title("🛡️ Sentinel Alpha Project")

st.markdown("""
### 🌿 Bridging Ecology & Technology
Developed as a specialized tool for **Wildlife Ecology and Management (WIEM 102)**, Sentinel Alpha 
digitizes the process of species classification and habitat monitoring in Kenya.

**Project Objectives:**
* **Species Identification**: Using Gemini AI to identify Kenyan fauna in real-time.
* **Data Logging**: Creating a permanent digital record of sightings for conservation research.
* **Field Safety**: Integrated weather and coordination tools for Rangers.

**Academic Context:**
* **Course**: Wildlife Ecology & Management
* **Focus**: Endangered species classification & GPS habitat mapping.
* **Developer**: Wolf (Software Development & Wildlife Ecology Student)
""")

st.info("💡 This app is a prototype designed to assist Rangers in the field with rapid identification and reporting.")

if st.button("⬅️ Return to Hub"):
    st.switch_page("pages/3_Sentinel_Hub.py")
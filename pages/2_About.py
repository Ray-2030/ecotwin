import streamlit as st

st.set_page_config(page_title="About Sentinel", page_icon="ℹ️")

st.title("🌍 Sentinel Alpha Mission")
st.markdown("""
### 🇰🇪 Kenya's Advanced Conservation AI
Sentinel Alpha is a specialized ecosystem monitoring tool built for the **Global Conservation Initiative**.

**Technological Core:**
* **Gemini 1.5 Flash**: Real-time species identification.
* **PostgreSQL (Aiven)**: Permanent field journal logging.
* **Ranger Network**: Secure coordination for field agents.

**Developer:** Wolf (Dev 2) | Wildlife Ecology & Software Development
""")

if st.button("⬅️ Back to Portal"):
    st.switch_page("ecotwin_app.py")
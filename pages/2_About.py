import streamlit as st

st.set_page_config(page_title="About Sentinel", page_icon="ℹ️")

# --- BRANDING ---
st.image("https://cdn-icons-png.flaticon.com/512/3062/3062250.png", width=70)
st.title("🛡️ Sentinel Alpha Project")

# --- ACADEMIC CONTEXT ---
st.markdown("""
### 🌿 WIEM 102: Wildlife Ecology & Management
This platform was developed to digitize field observations for the **Wildlife Ecology (WIEM 102)** course. 
By combining Python with Gemini AI, we can monitor Kenyan biodiversity with high precision.

**Key Mission Areas:**
* **Species Identification**: Instant classification of Kenyan fauna.
* **Habitat Mapping**: Monitoring range-land shifts in the Rift Valley.
* **Digital Logging**: Moving from paper field notes to a secure cloud database.
""")

# --- 🚨 NEW: ENDANGERED SPECIES ALERTS (2026 UPDATE) ---
st.error("### 🚨 2026 Endangered Species Alerts")
st.markdown("""
According to the latest **National Wildlife Census**, please prioritize reporting for:
1. **Mountain Bongo**: Critically endangered. Only ~130 individuals remain in the wild.
2. **Hirola (Hunter's Antelope)**: High priority near the Somalia border.
3. **Black Rhinoceros**: Monitor for poaching activity in protected zones.
4. **Grevy's Zebra**: Populations are declining due to habitat fragmentation.
""")

st.info("💡 Developed by **Wolf (Dev 2)** — Software Dev & Wildlife Ecology Student.")

if st.button("⬅️ Return to Hub"):
    st.switch_page("pages/3_Sentinel_Hub.py")
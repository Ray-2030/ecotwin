import streamlit as st
import pandas as pd

st.title("🎮 Ranger Command Console")

# --- 12. CSV EXPORT ---
data = {"Date": ["2026-03-21"], "Ranger": ["Wolf"], "Species": ["Black Rhino"], "Location": ["Rift Valley"]}
df = pd.DataFrame(data)
st.download_button("📥 Download sightings for Lecturer (Excel/CSV)", df.to_csv(), "field_report.csv")

# --- 20. GAMIFIED RANKS ---
xp = 450 # This would pull from your DB
rank = "Master Ecologist" if xp > 400 else "Novice Tracker"
st.success(f"🏅 Current Rank: {rank}")

# --- 19. AUTOMATED CITE GENERATOR ---
st.subheader("📚 Citation Generator")
species_name = st.text_input("Enter Species for Citation:", "Black Rhino")
st.code(f"World Wildlife Fund. (2026). {species_name} Conservation Status. Retrieved from Sentinel Alpha Hub.")

# --- 23. GITHUB INTEGRATION ---
st.sidebar.link_button("📂 View Source Code (GitHub)", "https://github.com/Ray-2030/ecotwin")
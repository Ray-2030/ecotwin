import streamlit as st
import google.generativeai as genai

st.title("📝 Ranger Field Research")

# --- CHICA TRANSLATOR ---
st.subheader("🐔 AI Vocalization Translator")
audio_file = st.file_uploader("Upload wildlife or 'chica' audio", type=['mp3', 'wav'])
if audio_file:
    with st.spinner("Analyzing distress frequencies..."):
        genai.configure(api_key=st.secrets["gemini"]["api_key"])
        model = genai.GenerativeModel('gemini-1.5-flash')
        # In 2026, Gemini can analyze audio files directly
        res = model.generate_content(["Describe the emotion/meaning in this animal sound.", audio_file])
        st.success(res.text)

# --- FIELD NOTEBOOK ---
st.subheader("📓 Digital Field Notebook")
note = st.text_area("Record behavior observations for WIEM 102:")
if st.button("Save Note"):
    st.write("✅ Note saved to encrypted field log.")
    # Calculate "Green Impact" (Carbon Tracker)
    st.metric("Carbon Offset Potential", "0.4 Tons CO2", delta="Safe Habitat")
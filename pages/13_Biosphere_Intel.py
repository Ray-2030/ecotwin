import streamlit as st
import random

st.set_page_config(page_title="Biosphere Intel")
st.title("🧬 Biosphere Intelligence")

col1, col2 = st.columns(2)

with col1:
    # 32. DNA BARCODING
    st.subheader("🧪 DNA Barcoding")
    dna = st.text_input("Input Sample ID")
    if st.button("Analyze DNA"):
        st.write("🧬 **Result:** Match found - *Diceros bicornis*")
    
    # 34. CARBON CREDIT
    st.subheader("🌱 Carbon Credits")
    st.metric("Credits Earned", f"{random.uniform(1,5):.2f} ECO", "+0.2")

with col2:
    # 39. PLANETARY HEALTH
    st.subheader("🌍 Health Score")
    st.slider("Biodiversity Index", 0, 100, 78)
    
    # 45. ANCESTRAL KNOWLEDGE
    with st.expander("📜 Ancestral Knowledge"):
        st.write("Traditional Kenyan lore regarding species protection and rainfall patterns.")
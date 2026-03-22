import streamlit as st
from sqlalchemy import create_engine, text

st.set_page_config(page_title="Ranger Pokédex", page_icon="📕")

def get_engine():
    s = st.secrets["connections"]["postgresql"]
    return create_engine(f"postgresql://{s['username']}:{s['password']}@{s['host']}:{s['port']}/{s['database']}?sslmode=require")

st.title("📕 The Sentinel Pokédex")
st.write("Your personal collection of documented Kenyan wildlife.")

try:
    with get_engine().connect() as conn:
        query = text("SELECT DISTINCT species FROM sightings WHERE ranger = :u")
        species_list = conn.execute(query, {"u": st.session_state.user}).fetchall()
        
        if species_list:
            cols = st.columns(3)
            for i, s in enumerate(species_list):
                with cols[i % 3]:
                    st.info(f"🦁 {s[0]}")
        else:
            st.warning("Your Pokédex is empty! Go to the Hub and scan some wildlife.")
except:
    st.error("Pokédex offline. Database connecting...")

if st.button("⬅️ Back to Hub"):
    st.switch_page("pages/3_🌿_Sentinel_Hub.py")
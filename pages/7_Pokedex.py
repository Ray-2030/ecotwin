import streamlit as st
from sqlalchemy import create_engine, text

st.set_page_config(page_title="Ranger Pokédex", page_icon="📕")

# Auth Check
if not st.session_state.get("auth"):
    st.switch_page("ecotwin_app.py")

def get_engine():
    s = st.secrets["connections"]["postgresql"]
    return create_engine(f"postgresql://{s['username']}:{s['password']}@{s['host']}:{s['port']}/{s['database']}?sslmode=require")

st.title("📕 The Sentinel Pokédex")
st.write("Your documented collection of Kenya's biodiversity.")

try:
    with get_engine().connect() as conn:
        # Get unique species for the logged-in user
        query = text("SELECT DISTINCT species FROM sightings WHERE ranger = :u ORDER BY species ASC")
        my_species = conn.execute(query, {"u": st.session_state.user}).fetchall()
        
        if my_species:
            st.write(f"You have documented **{len(my_species)}** unique species.")
            
            # Create a clean grid display
            cols = st.columns(3)
            for i, s in enumerate(my_species):
                with cols[i % 3]:
                    st.markdown(f"""
                    <div style="background-color: #1A1C23; padding: 20px; border-radius: 10px; border-left: 5px solid #2E7D32; margin-bottom: 10px;">
                        <p style="margin: 0; color: #E0E0E0; font-weight: bold;">🐾 {s[0]}</p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("Your Pokédex is empty! Head to the Hub to start scanning.")
            
except:
    st.error("Pokédex records are temporarily unavailable.")

if st.button("⬅️ Back to Hub"):
    st.switch_page("pages/3_Sentinel_Hub.py")
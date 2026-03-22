import streamlit as st
import pandas as pd

st.set_page_config(page_title="Join the Pride", page_icon="🦁")

st.title("🦁 Join the Sentinel Pride")
st.markdown("Register your Ranger ID to sync field sightings with the team.")

# --- REGISTRATION FORM ---
with st.form("ranger_reg"):
    ranger_name = st.text_input("Ranger Name (e.g., Wolf)", placeholder="Enter your callsign...")
    role = st.selectbox("Field Role", ["Wildlife Ecologist", "Software Dev", "Data Analyst", "Lead Ranger"])
    location_pref = st.text_input("Primary Observation Post", value="Rift Valley")
    
    submit = st.form_submit_button("Initialize Sync")

if submit:
    if ranger_name:
        # Saving to session_state so other pages (like the Hub) know who is logged in
        st.session_state.logged_in = True
        st.session_state.ranger_id = ranger_name
        st.session_state.role = role
        
        st.success(f"Welcome to the Pride, Ranger {ranger_name}! Connection established.")
        st.balloons()
        
        # Redirect to the Hub
        if st.button("Go to Command Hub"):
            st.switch_page("pages/3_Sentinel_Hub.py")
    else:
        st.error("Please enter a Ranger Name to continue.")

st.info("💡 Tip: Your Ranger ID will be attached to every sighting you log in the Field Notes.")
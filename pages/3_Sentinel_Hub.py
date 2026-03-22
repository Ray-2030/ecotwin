with st.sidebar:
    st.title("🌲 Ranger Tools")
    # ... (other code) ...
    
    if st.button("🔍 Species Guide", use_container_width=True): 
        st.switch_page("pages/6_Species_Guide.py")
        
    if st.button("📕 My Pokédex", use_container_width=True): 
        st.switch_page("pages/7_Pokedex.py")
        
    if st.button("📓 Field Research", use_container_width=True): 
        st.switch_page("pages/8_Field_Notes.py")
        
    if st.button("🏆 Leaderboard", use_container_width=True): 
        st.switch_page("pages/4_Leaderboard.py")
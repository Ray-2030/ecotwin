import streamlit as st
import hashlib
from sqlalchemy import create_engine, text

st.set_page_config(page_title="Sentinel Alpha Portal", page_icon="🚨", layout="centered")

def get_engine():
    s = st.secrets["connections"]["postgresql"]
    return create_engine(
        f"postgresql://{s['username']}:{s['password']}@{s['host']}:{s['port']}/{s['database']}?sslmode=require",
        pool_pre_ping=True, 
        connect_args={'connect_timeout': 60} 
    )

def hash_pw(pw):
    return hashlib.sha256(str.encode(pw)).hexdigest()

if "auth" not in st.session_state: st.session_state.auth = False

st.title("🚨 Sentinel Alpha Portal")

with st.container(border=True):
    u_in = st.text_input("Ranger ID").strip()
    p_in = st.text_input("Security Key", type="password").strip()
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Unlock Portal", use_container_width=True, type="primary"):
            # --- THE FIX: ADMIN BYPASS ---
            # Type 'Wolf' as ID and 'WolfAdmin@2026' as Key
            admin_h = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"
            
            if u_in.lower() == "wolf" and hash_pw(p_in) == admin_h:
                st.session_state.auth, st.session_state.user = True, "Wolf (Admin)"
                st.switch_page("pages/3_🌿_Sentinel_Hub.py")
            else:
                try:
                    with get_engine().connect() as conn:
                        res = conn.execute(text("SELECT password FROM users WHERE username = :u"), {"u": u_in}).fetchone()
                        if res and res[0] == hash_pw(p_in):
                            st.session_state.auth, st.session_state.user = True, u_in
                            st.switch_page("pages/3_🌿_Sentinel_Hub.py")
                        else: st.error("Access Denied.")
                except: st.error("Database is warming up... try in 10s")
                
    with c2:
        if st.button("Join the Pride", use_container_width=True):
            # This handles the StreamlitAPIException path error
            try:
                st.switch_page("pages/1_✨_Join_Pride.py")
            except:
                st.error("Error: Check if file 'pages/1_✨_Join_Pride.py' exists on GitHub!")
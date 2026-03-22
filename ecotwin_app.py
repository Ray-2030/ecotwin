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
            
            # --- EMERGENCY ADMIN BYPASS (NO HASHING) ---
            # This will work even if the database is dead
            if u_in.lower() == "wolf" and p_in == "WolfAdmin@2026":
                st.session_state.auth = True
                st.session_state.user = "Wolf (Admin)"
                st.success("Admin Bypass Successful!")
                st.switch_page("pages/3_🌿_Sentinel_Hub.py")
            
            # --- REGULAR USER LOGIN ---
            else:
                try:
                    with get_engine().connect() as conn:
                        res = conn.execute(text("SELECT password FROM users WHERE username = :u"), {"u": u_in}).fetchone()
                        if res and res[0] == hash_pw(p_in):
                            st.session_state.auth = True
                            st.session_state.user = u_in
                            st.switch_page("pages/3_🌿_Sentinel_Hub.py")
                        else: 
                            st.error("Access Denied: Check your Key.")
                except: 
                    st.error("Database is warming up... try again in 10s")
                
    with c2:
        if st.button("Join the Pride", use_container_width=True):
            try:
                st.switch_page("pages/1_✨_Join_Pride.py")
            except:
                st.error("Path Error: Ensure pages/1_✨_Join_Pride.py exists on GitHub.")
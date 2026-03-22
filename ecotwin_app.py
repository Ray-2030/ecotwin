import streamlit as st
import hashlib
from sqlalchemy import create_engine, text

# 1. PAGE CONFIG
st.set_page_config(page_title="Sentinel Alpha | Login", page_icon="🔐", layout="centered")

# 2. DATABASE ENGINE (Fixed for Aiven Cold Starts)
def get_engine():
    s = st.secrets["connections"]["postgresql"]
    return create_engine(
        f"postgresql://{s['username']}:{s['password']}@{s['host']}:{s['port']}/{s['database']}?sslmode=require",
        pool_pre_ping=True, 
        connect_args={'connect_timeout': 60} 
    )

def hash_pw(pw):
    return hashlib.sha256(str.encode(pw)).hexdigest()

# 3. INITIALIZE AUTH STATE
if "auth" not in st.session_state:
    st.session_state.auth = False
if "user" not in st.session_state:
    st.session_state.user = None

# --- IMPORTANT: OLD PAGE LOGIC (if page == ...) HAS BEEN REMOVED ---

# 4. LOGIN INTERFACE
st.title("🚨 Sentinel Alpha Portal")
st.write("Secure Gateway for Kenya Wildlife Rangers")

with st.container(border=True):
    u_in = st.text_input("Ranger ID (Username)").strip()
    p_in = st.text_input("Security Key (Password)", type="password").strip()
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Unlock Portal", use_container_width=True, type="primary"):
            # ADMIN MASTER BYPASS: Wolf | WolfAdmin@2026
            admin_h = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"
            
            if u_in.lower() == "wolf" and hash_pw(p_in) == admin_h:
                st.session_state.auth = True
                st.session_state.user = "Wolf (Admin)"
                st.success("Admin Access Granted!")
                # This command teleports you to the Hub file in the pages/ folder
                st.switch_page("pages/3_🌿_Sentinel_Hub.py")
            else:
                try:
                    with get_engine().connect() as conn:
                        query = text("SELECT password FROM users WHERE username = :u")
                        result = conn.execute(query, {"u": u_in}).fetchone()
                        
                        if result and result[0] == hash_pw(p_in):
                            st.session_state.auth = True
                            st.session_state.user = u_in
                            st.switch_page("pages/3_🌿_Sentinel_Hub.py")
                        else:
                            st.error("Invalid Ranger ID or Key.")
                except Exception as e:
                    st.error("Database is warming up. Please wait 10 seconds and try again.")

    with col2:
        # Sends you to the Registration page
        if st.button("Join the Pride", use_container_width=True):
            st.switch_page("pages/1_✨_Join_Pride.py")

# 5. FOOTER & ABOUT LINK
st.divider()
st.markdown("Developed by Wolf (Dev 2) for the Global Conservation Initiative.")
if st.button("ℹ️ Learn About Sentinel Alpha", type="secondary"):
    st.switch_page("pages/2_ℹ️_About.py")
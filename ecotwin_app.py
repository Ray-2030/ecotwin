import streamlit as st
import hashlib
from sqlalchemy import create_engine, text
import time

# --- INITIAL APP CONFIG ---
st.set_page_config(page_title="Sentinel Alpha Portal", page_icon="🛡️", layout="centered")

# --- BRANDING SECTION ---
# This adds your logo and title to the main login page
logo_url = "https://cdn-icons-png.flaticon.com/512/3062/3062250.png"
col1, col2 = st.columns([1, 4])
with col1:
    st.image(logo_url, width=80)
with col2:
    st.title("Sentinel Alpha")
    st.caption("Kenya Wildlife Monitoring & Reconnaissance")

# --- DATABASE ENGINE ---
def get_engine():
    try:
        s = st.secrets["connections"]["postgresql"]
        return create_engine(
            f"postgresql://{s['username']}:{s['password']}@{s['host']}:{s['port']}/{s['database']}?sslmode=require",
            pool_pre_ping=True,
            connect_args={'connect_timeout': 30}
        )
    except Exception as e:
        return None

def hash_pw(pw):
    return hashlib.sha256(str.encode(pw)).hexdigest()

# --- SYSTEM STATUS CHECK ---
db_ready = False
try:
    engine = get_engine()
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    db_ready = True
    st.success("🟢 System Online: Secure Connection Established")
except:
    st.warning("🟡 System Warming Up: Database link initializing... (15s)")

# --- LOGIN PORTAL ---
with st.container(border=True):
    st.subheader("Ranger Authentication")
    u_in = st.text_input("Ranger ID (Username)").strip()
    p_in = st.text_input("Security Key (Password)", type="password").strip()
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        if st.button("Unlock Portal", use_container_width=True, type="primary"):
            # --- ADMIN BYPASS ---
            if u_in.lower() == "wolf" and p_in == "WolfAdmin@2026":
                st.session_state.auth = True
                st.session_state.user = "Wolf (Admin)"
                st.session_state.points = 1000  # Admin starts at Warden rank
                st.switch_page("pages/3_Sentinel_Hub.py")
            
            # --- STANDARD USER LOGIN ---
            elif db_ready:
                try:
                    with get_engine().connect() as conn:
                        res = conn.execute(text("SELECT password FROM users WHERE username = :u"), {"u": u_in}).fetchone()
                        if res and res[0] == hash_pw(p_in):
                            st.session_state.auth = True
                            st.session_state.user = u_in
                            st.switch_page("pages/3_Sentinel_Hub.py")
                        else:
                            st.error("Invalid credentials. Please retry.")
                except Exception as e:
                    st.error("Database busy. Please wait 10 seconds.")
            else:
                st.error("System is still warming up. Please wait for the green light.")

    with col_b:
        if st.button("Join the Pride", use_container_width=True):
            st.switch_page("pages/1_Join_Pride.py")

# --- FOOTER ---
st.markdown("---")
st.caption("Developed by Dev 2 (Wolf) | Wildlife Ecology & Software Dev Project")
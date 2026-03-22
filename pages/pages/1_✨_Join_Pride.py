import streamlit as st
import hashlib
from sqlalchemy import create_engine, text

st.set_page_config(page_title="Join the Pride", page_icon="✨")

def get_engine():
    s = st.secrets["connections"]["postgresql"]
    return create_engine(f"postgresql://{s['username']}:{s['password']}@{s['host']}:{s['port']}/{s['database']}?sslmode=require", pool_pre_ping=True)

st.title("✨ Join the Sentinel Pride")
st.write("Register your Ranger ID to start protecting Kenya's wildlife.")

with st.form("registration_form"):
    new_u = st.text_input("Choose Ranger ID (Username)").strip()
    new_p = st.text_input("Choose Security Key (Password)", type="password").strip()
    submit = st.form_submit_button("Register Account")

if submit:
    if new_u and new_p:
        try:
            with get_engine().begin() as conn:
                conn.execute(text("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)"))
                h_pw = hashlib.sha256(new_p.encode()).hexdigest()
                conn.execute(text("INSERT INTO users (username, password) VALUES (:u, :p)"), {"u": new_u, "p": h_pw})
            st.success("Registration successful! Please go to the Login page.")
        except:
            st.error("This Ranger ID is already taken.")
    else:
        st.warning("Please fill in both fields.")

if st.button("⬅️ Back to Login"):
    st.switch_page("ecotwin_app.py")
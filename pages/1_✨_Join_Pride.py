import streamlit as st
import hashlib
from sqlalchemy import create_engine, text

st.set_page_config(page_title="Join the Pride", page_icon="✨")

def get_engine():
    s = st.secrets["connections"]["postgresql"]
    return create_engine(f"postgresql://{s['username']}:{s['password']}@{s['host']}:{s['port']}/{s['database']}?sslmode=require")

st.title("✨ Join the Sentinel Pride")
st.write("Register as a new Ranger to begin monitoring.")

with st.form("reg_form"):
    new_u = st.text_input("Choose Ranger ID").strip()
    new_p = st.text_input("Choose Security Key", type="password").strip()
    submit = st.form_submit_button("Register")

if submit:
    if new_u and new_p:
        try:
            with get_engine().begin() as conn:
                conn.execute(text("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)"))
                h_pw = hashlib.sha256(new_p.encode()).hexdigest()
                conn.execute(text("INSERT INTO users (username, password) VALUES (:u, :p)"), {"u": new_u, "p": h_pw})
            st.success("Registration successful! Go back to the Login page.")
        except:
            st.error("Ranger ID already exists.")
    else:
        st.warning("Please fill all fields.")
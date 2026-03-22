import streamlit as st
from sqlalchemy import create_engine, text
from datetime import datetime

st.set_page_config(page_title="Pride Chat", page_icon="🦁")

def get_engine():
    s = st.secrets["connections"]["postgresql"]
    return create_engine(f"postgresql://{s['username']}:{s['password']}@{s['host']}:{s['port']}/{s['database']}?sslmode=require")

st.title("🦁 Pride Chat")
st.write("Share live field updates with other Rangers.")

# Send Message
with st.container(border=True):
    msg = st.text_input("Broadcast a message (e.g., 'Rhino spotted at Gate A!')")
    if st.button("Send to Pride"):
        with get_engine().begin() as conn:
            conn.execute(text("CREATE TABLE IF NOT EXISTS chat (user_name TEXT, message TEXT, sent_at TIMESTAMP)"))
            conn.execute(text("INSERT INTO chat VALUES (:u, :m, :t)"), {"u": st.session_state.user, "m": msg, "t": datetime.now()})
        st.success("Message broadcasted!")

# Display Feed
st.markdown("---")
with get_engine().connect() as conn:
    feed = conn.execute(text("SELECT user_name, message, sent_at FROM chat ORDER BY sent_at DESC LIMIT 10")).fetchall()
    for f in feed:
        st.markdown(f"**{f[0]}**: {f[1]} *({f[2].strftime('%H:%M')})*")
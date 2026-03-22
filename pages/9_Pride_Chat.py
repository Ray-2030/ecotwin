import streamlit as st
from sqlalchemy import create_engine, text
from datetime import datetime
import pytz

st.set_page_config(page_title="Pride Chat", page_icon="🦁")

# Auth Check
if not st.session_state.get("auth"):
    st.switch_page("ecotwin_app.py")

def get_engine():
    s = st.secrets["connections"]["postgresql"]
    return create_engine(f"postgresql://{s['username']}:{s['password']}@{s['host']}:{s['port']}/{s['database']}?sslmode=require", pool_pre_ping=True)

st.title("🦁 Pride Chat")
st.write("Live coordination feed for Kenyan Wildlife Rangers.")

# Message Input
with st.container(border=True):
    msg = st.text_input("Broadcast to the Pride (e.g., 'Elephants near Gate B')")
    if st.button("Send Broadcast", use_container_width=True, type="primary"):
        if msg:
            try:
                kenya_tz = pytz.timezone('Africa/Nairobi')
                now = datetime.now(kenya_tz)
                with get_engine().begin() as conn:
                    conn.execute(text("CREATE TABLE IF NOT EXISTS chat (user_name TEXT, message TEXT, sent_at TIMESTAMP)"))
                    conn.execute(text("INSERT INTO chat (user_name, message, sent_at) VALUES (:u, :m, :t)"), 
                                 {"u": st.session_state.user, "m": msg, "t": now})
                st.toast("Message Sent!")
            except:
                st.error("Comms down. Check database.")

# Display Feed
st.markdown("---")
try:
    with get_engine().connect() as conn:
        feed = conn.execute(text("SELECT user_name, message, sent_at FROM chat ORDER BY sent_at DESC LIMIT 15")).fetchall()
        for f in feed:
            with st.chat_message("user" if f[0] != st.session_state.user else "assistant"):
                st.write(f"**{f[0]}**: {f[1]}")
                st.caption(f"{f[2].strftime('%H:%M')} EAT")
except:
    st.info("The Pride is currently quiet. Be the first to speak!")

if st.button("⬅️ Back to Hub"):
    st.switch_page("pages/3_Sentinel_Hub.py")
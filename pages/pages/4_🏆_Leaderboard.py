import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text

st.set_page_config(page_title="Leaderboard", page_icon="🏆")

def get_engine():
    s = st.secrets["connections"]["postgresql"]
    return create_engine(f"postgresql://{s['username']}:{s['password']}@{s['host']}:{s['port']}/{s['database']}?sslmode=require")

st.title("🏆 Global Ranger Leaderboard")

try:
    with get_engine().connect() as conn:
        query = text("""
            SELECT ranger, COUNT(*) * 20 as score 
            FROM sightings 
            GROUP BY ranger 
            ORDER BY score DESC 
            LIMIT 10
        """)
        df = pd.read_sql(query, conn)
        
        if not df.empty:
            st.dataframe(df, use_container_width=True)
            st.success(f"Top Ranger: {df['ranger'].iloc[0]}!")
        else:
            st.info("No sightings logged yet.")
except:
    st.error("Leaderboard is waking up...")

if st.button("⬅️ Back to Hub"):
    st.switch_page("pages/3_🌿_Sentinel_Hub.py")
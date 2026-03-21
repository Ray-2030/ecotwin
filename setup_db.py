import psycopg2
import streamlit as st

def create_table():
    conn = psycopg2.connect(
        host=st.secrets["connections"]["postgresql"]["host"],
        port=st.secrets["connections"]["postgresql"]["port"],
        database=st.secrets["connections"]["postgresql"]["database"],
        user=st.secrets["connections"]["postgresql"]["username"],
        password=st.secrets["connections"]["postgresql"]["password"],
        sslmode="require"
    )
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS eco_logs (
            log_id SERIAL PRIMARY KEY,
            garden_id INT DEFAULT 1,
            recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            temperature_c FLOAT,
            humidity_pct FLOAT,
            soil_moisture_pct FLOAT
        );
    """)
    conn.commit()
    print("✅ Table created successfully in the cloud!")
    cur.close()
    conn.close()

if __name__ == "__main__":
    create_table()
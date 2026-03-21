import psycopg2
import streamlit as st

def create_table():
    try:
        # Tries to use secrets first, falls back to manual entry if needed
        try:
            conn = psycopg2.connect(
                host=st.secrets["connections"]["postgresql"]["host"],
                port=st.secrets["connections"]["postgresql"]["port"],
                database=st.secrets["connections"]["postgresql"]["database"],
                user=st.secrets["connections"]["postgresql"]["username"],
                password=st.secrets["connections"]["postgresql"]["password"],
                sslmode="require"
            )
        except:
            print("Secret file not found, using manual connection...")
            conn = psycopg2.connect(
                host="pg-16825ecc-ecotwin.c.aivencloud.com",
                port=10442,
                database="defaultdb",
                user="avnadmin",
                password="PASTE_YOUR_PASSWORD_HERE",
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
        print("✅ Success! The cloud table 'eco_logs' is ready.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    create_table()
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import google.generativeai as genai
from PIL import Image
from io import BytesIO
from datetime import datetime

# --- 1. DATABASE & AI SETUP ---
def get_engine():
    user = st.secrets["connections"]["postgresql"]["username"]
    pw = st.secrets["connections"]["postgresql"]["password"]
    host = st.secrets["connections"]["postgresql"]["host"]
    port = st.secrets["connections"]["postgresql"]["port"]
    db = st.secrets["connections"]["postgresql"]["database"]
    db_url = f"postgresql://{user}:{pw}@{host}:{port}/{db}?sslmode=require"
    return create_engine(db_url)

# Setup Gemini AI
genai.configure(api_key=st.secrets["gemini"]["api_key"])
# Using 2.5 Flash for the best multimodal/image performance
model = genai.GenerativeModel('gemini-2.5-flash')

# Utility: Convert DataFrame to CSV
@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

# --- 2. APP LAYOUT ---
st.set_page_config(page_title="EcoTwin AI", page_icon="🌿", layout="wide")
st.title("🌿 EcoTwin AI: Visual Ecology Monitor")
st.caption(f"Wolf's Wildlife Ecology Project • {datetime.now().strftime('%Y')}")

# --- 3. SIDEBAR: DATA ENTRY & EXPORT ---
with st.sidebar:
    st.header("📍 Field Data Entry")
    temp = st.number_input("Temp (°C)", value=25.0)
    hum = st.number_input("Humidity (%)", value=50.0)
    soil = st.number_input("Soil Moisture (%)", value=30.0)
    
    if st.button("Push to Aiven Cloud"):
        try:
            engine = get_engine()
            with engine.begin() as conn:
                query = text("INSERT INTO eco_logs (temperature_c, humidity_pct, soil_moisture_pct) VALUES (:t, :h, :s)")
                conn.execute(query, {"t": temp, "h": hum, "s": soil})
            st.success("✅ Data Synced!")
            st.balloons()
        except Exception as e:
            st.error(f"Sync Failed: {e}")

    st.markdown("---")
    st.header("📊 Export Report")
    try:
        engine = get_engine()
        full_df = pd.read_sql("SELECT * FROM eco_logs ORDER BY recorded_at DESC", engine)
        if not full_df.empty:
            st.download_button("📥 Download CSV", data=convert_df(full_df), file_name="ecotwin_data.csv")
    except:
        pass

# --- 4. MAIN DASHBOARD ---
try:
    engine = get_engine()
    df = pd.read_sql("SELECT recorded_at, temperature_c, humidity_pct, soil_moisture_pct FROM eco_logs ORDER BY recorded_at DESC LIMIT 50", engine)
    
    if not df.empty:
        latest = df.iloc[0]
        col1, col2, col3 = st.columns(3)
        col1.metric("Temperature", f"{latest['temperature_c']}°C")
        col2.metric("Humidity", f"{latest['humidity_pct']}%")
        col3.metric("Soil Moisture", f"{latest['soil_moisture_pct']}%")
        
        st.subheader("Ecological Trends")
        st.line_chart(df.set_index('recorded_at')[['temperature_c', 'humidity_pct', 'soil_moisture_pct']])

        st.markdown("---")
        
        # --- 5. NEW: VISUAL SOIL ANALYSIS ---
        st.subheader("📸 AI Visual Soil Analysis")
        st.write("Upload a photo of the soil to estimate moisture and health.")
        
        img_file = st.file_uploader("Capture soil photo", type=["jpg", "jpeg", "png"])
        
        if img_file:
            img = Image.open(img_file)
            st.image(img, caption="Field Sample", width=400)
            
            if st.button("Analyze Soil with Gemini"):
                with st.spinner("Analyzing textures and color gradients..."):
                    # Multi-modal prompt: Text + Image
                    prompt = """
                    As a Wildlife Ecology expert, analyze this soil image. 
                    1. Estimate the moisture percentage based on color and clumping.
                    2. Identify the soil type (Sandy, Loamy, Clay).
                    3. Give a brief 'Eco-Health' recommendation for plants.
                    """
                    try:
                        response = model.generate_content([prompt, img])
                        st.success("Analysis Complete")
                        st.info(response.text)
                    except Exception as e:
                        st.error(f"AI Error: {e}")

        # --- 6. STANDARD CHAT ---
        st.markdown("---")
        st.subheader("🤖 Ecology Advisor Chat")
        u_query = st.text_input("Ask a question about your environment:")
        if u_query:
            context = f"Current Data: Temp {latest['temperature_c']}°C, Soil {latest['soil_moisture_pct']}%."
            res = model.generate_content(f"{u_query}. {context}")
            st.write(res.text)

except Exception as e:
    st.error(f"System Error: {e}")
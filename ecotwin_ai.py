from google.genai import Client
import mysql.connector
import csv
import re
from datetime import datetime

# 1. Setup
client = Client(api_key="AIzaSyCjd8e9jtM1we9sMX_r8o-dBn78q3RMe5Y")

def get_db_connection():
    return mysql.connector.connect(host='127.0.0.1', database='ecotwin_db', user='root', password='')

def export_to_csv():
    """Generates a CSV report file from the database."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT log_id, recorded_at, temperature_c, humidity_pct, soil_moisture_pct FROM eco_logs")
        rows = cursor.fetchall()
        
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        filename = f"eco_report_{timestamp}.csv"
        
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Log ID', 'Timestamp', 'Temp (C)', 'Humidity (%)', 'Soil Moisture (%)'])
            writer.writerows(rows)
        
        conn.close()
        return filename
    except Exception as e:
        return None

def ask_ecotwin(user_query):
    internal_note = ""
    
    # --- TRIGGER 1: Export Logic ---
    if "export" in user_query.lower() or "download" in user_query.lower():
        report_file = export_to_csv()
        if report_file:
            internal_note += f" [SUCCESS: Report generated as {report_file}]"
        else:
            internal_note += " [ERROR: Export failed]"

    # --- TRIGGER 2: Existing Sensor Logic (Regex) ---
    nums = re.findall(r"[-+]?\d*\.\d+|\d+", user_query)
    if "temperature" in user_query.lower() and len(nums) >= 1:
        # (Existing logging logic here...)
        internal_note += " [SYSTEM: Data logged]"

    context = f"You are a Kenyan Wildlife Ecology expert. Internal Data Flags: {internal_note}"
    response = client.models.generate_content(model="gemini-2.5-flash", contents=f"{context}\n\nUser: {user_query}")
    return response.text

# --- MAIN LOOP ---
if __name__ == "__main__":
    print("🌿 EcoTwin AI 5.0: The Enterprise Edition Online!")
    print("Commands: 'The temp is 30', 'Give me a trend', 'Export my data'")
    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() in ['quit', 'exit']: break
            print(f"\nEcoTwin: {ask_ecotwin(user_input)}")
        except KeyboardInterrupt: break
        except Exception as e: print(f"Error: {e}")
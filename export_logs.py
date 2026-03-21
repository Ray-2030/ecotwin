import mysql.connector
import csv
from datetime import datetime

def export_to_csv():
    try:
        # 1. Connect to your database
        conn = mysql.connector.connect(
            host='127.0.0.1',
            database='ecotwin_db',
            user='root',
            password=''
        )
        cursor = conn.cursor()

        # 2. Fetch all data from eco_logs
        query = "SELECT log_id, recorded_at, temperature_c, humidity_pct, soil_moisture_pct FROM eco_logs"
        cursor.execute(query)
        rows = cursor.fetchall()

        # 3. Define the filename with a timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        filename = f"garden_report_{timestamp}.csv"

        # 4. Write to CSV
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write the Header Row
            writer.writerow(['Log ID', 'Timestamp', 'Temp (C)', 'Humidity (%)', 'Soil Moisture (%)'])
            # Write the Data Rows
            writer.writerows(rows)

        print(f"✅ Success! Your report has been saved as: {filename}")
        
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"❌ Error exporting data: {e}")

if __name__ == "__main__":
    export_to_csv()
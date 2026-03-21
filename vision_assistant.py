import google.generativeai as genai
import mysql.connector
import os

# 1. SETUP - Get your API key from https://aistudio.google.com/
genai.configure(api_key="YOUR_GEMINI_API_KEY")

def connect_db():
    return mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='', # Leave empty for XAMPP default
        database='ecotwin_db'
    )

def identify_and_add_plant(image_path):
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # We ask the AI to identify the plant AND give us the ID from your species list
    # Logic: The AI checks if it's one of your 4 seeded species
    prompt = """
    Identify this plant. 
    If it is a 'Fever Tree', 'Hibiscus', 'Aloe Vera', or 'Nandi Flame', return ONLY the name.
    If it is something else, provide the common name and a 1-sentence ecology tip.
    """
    
    # For now, let's use text-based identification to test the bridge
    # (You can swap this for image processing once you have the key)
    response = model.generate_content(prompt)
    plant_name = response.text.strip()
    
    print(f"EcoTwin Vision identified: {plant_name}")
    
    # 2. DATABASE BRIDGE - Auto-inserting into your MySQL
    try:
        db = connect_db()
        cursor = db.cursor()
        
        # First, find the species_id for the identified plant
        cursor.execute("SELECT species_id FROM plant_species WHERE common_name LIKE %s", (f"%{plant_name}%",))
        result = cursor.fetchone()
        
        if result:
            species_id = result[0]
            # Add to your 'Wolfs Eco-Zone' (Garden ID 1)
            sql = "INSERT INTO my_plants (garden_id, species_id, date_planted, current_status) VALUES (1, %s, CURDATE(), 'Growing')"
            cursor.execute(sql, (species_id,))
            db.commit()
            print(f"✅ Success! {plant_name} has been added to your Digital Twin.")
        else:
            print(f"❌ The AI found '{plant_name}', but it's not in your 'plant_species' library yet.")
            
    except Exception as e:
        print(f"Database Error: {e}")
    finally:
        db.close()

# TEST IT
if __name__ == "__main__":
    # You can pass an image path here later!
    identify_and_add_plant("hibiscus_photo.jpg")
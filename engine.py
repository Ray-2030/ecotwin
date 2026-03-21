import mysql.connector
from mysql.connector import Error

def get_garden_data():
    try:
        # Update these with your actual MySQL credentials
        connection = mysql.connector.connect(
            host='localhost',
            database='ecotwin_db',
            user='root', 
            password='your_password' 
        )

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            # This query joins our 'my_plants' with 'plant_species' to get the bee scores
            query = """
            SELECT p.common_name, s.bee_attraction_level 
            FROM my_plants p
            JOIN plant_species s ON p.species_id = s.species_id
            WHERE p.garden_id = 1;
            """
            cursor.execute(query)
            return cursor.fetchall()

    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def run_simulation():
    plants = get_garden_data()
    if not plants:
        print("No plants found in the digital twin yet!")
        return

    total_bee_boost = sum(p['bee_attraction_level'] for p in plants)
    print(f"🚀 EcoTwin Analysis for your garden:")
    print(f"Current Biodiversity Boost: {total_bee_boost}%")
    print(f"Future Prediction: Your local ecosystem will stabilize by {total_bee_boost * 0.2}% next month.")

if __name__ == "__main__":
    run_simulation()
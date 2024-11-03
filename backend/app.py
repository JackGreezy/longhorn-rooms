from datetime import datetime
from flask import Flask, jsonify
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# MongoDB configuration
MONGO_USERNAME = os.getenv("MONGO_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_CLUSTER_URL = os.getenv("MONGO_CLUSTER_URL")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

# MongoDB connection URI
connection_string = f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_CLUSTER_URL}/?retryWrites=true&w=majority&appName={MONGO_DB_NAME}"
client = MongoClient(connection_string)
db = client[MONGO_DB_NAME]
collection = db["structured_room_schedule"]

# Utility function to get today's day and current time
def get_current_day_and_time():
    now = datetime.now()
    current_day = now.strftime("%A")
    current_time = now.time()
    return current_day, current_time

# Endpoint to get available room count for each building
@app.route('/api/building_availability', methods=['GET'])
def get_building_availability():
    try:
        building_availability = {}
        current_day, current_time = get_current_day_and_time()

        # Fetch the single document containing all building data
        building_data = collection.find_one()
        if not building_data or "buildings" not in building_data:
            print("No building data found or 'buildings' key missing.")
            return jsonify({"error": "No building data found"}), 404

        # Loop through each building in the "buildings" array
        for building_info in building_data["buildings"]:
            building_name = building_info.get("name")
            total_rooms = building_info.get("total_rooms", 0)
            available_count = 0

            # Check each room in the building
            for room in building_info.get("rooms", []):
                room_number = room.get("room_number")
                schedules = room.get("schedule", [])
                is_available = True

                # Check if the room is available at the current time
                for schedule in schedules:
                    if schedule["day"] == current_day:
                        start_time = datetime.strptime(schedule["start_time"], "%I:%M %p").time()
                        end_time = datetime.strptime(schedule["end_time"], "%I:%M %p").time()
                        if start_time <= current_time <= end_time:
                            is_available = False
                            break

                if is_available:
                    available_count += 1

            building_availability[building_name] = {
                "total_rooms": total_rooms,
                "available_count": available_count
            }

        # Return the building availability data
        return jsonify(building_availability)

    except Exception as e:
        print(f"Internal server error: {e}")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

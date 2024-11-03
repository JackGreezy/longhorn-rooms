import requests
import os
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# MongoDB configuration
MONGO_USERNAME = os.getenv("MONGO_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_CLUSTER_URL = os.getenv("MONGO_CLUSTER_URL")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

# ArcGIS API configuration
ARCGIS_API_KEY = os.getenv("ARCGIS_API_KEY")
FEATURE_LAYER_URL = "https://services.arcgis.com/YOUR_LAYER_URL/arcgis/rest/services/YOUR_LAYER_NAME/FeatureServer/0/applyEdits"

# MongoDB connection URI
connection_string = f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_CLUSTER_URL}/?retryWrites=true&w=majority"
client = MongoClient(connection_string)
db = client[MONGO_DB_NAME]
collection = db["structured_room_schedule"]

# Utility function to get today's day and current time
def get_current_day_and_time():
    now = datetime.now()
    current_day = now.strftime("%A")
    current_time = now.time()
    return current_day, current_time

# Fetch room availability and update ArcGIS
def update_feature_layer():
    building_availability = []
    current_day, current_time = get_current_day_and_time()

    # Fetch the single document containing all building data
    building_data = collection.find_one()
    if not building_data or "buildings" not in building_data:
        print("No building data found or 'buildings' key missing.")
        return

    features = []
    # Loop through each building in the "buildings" array
    for building_info in building_data["buildings"]:
        building_name = building_info.get("name")
        total_rooms = building_info.get("total_rooms", 0)
        coordinates = building_info.get("coordinates")
        latitude = coordinates.get("latitude")
        longitude = coordinates.get("longitude")

        available_count = 0

        # Check each room in the building
        for room in building_info.get("rooms", []):
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

        # Create a feature to update in the ArcGIS feature layer
        feature = {
            "attributes": {
                "name": building_name,
                "total_rooms": total_rooms,
                "available_rooms": available_count  # Add available count as a field
            },
            "geometry": {
                "x": longitude,
                "y": latitude
            }
        }
        features.append(feature)

    # Prepare the payload for the API request
    payload = {
        "updates": features,
        "f": "json",
        "token": ARCGIS_API_KEY
    }

    # Send the request to update the feature layer
    response = requests.post(FEATURE_LAYER_URL, json=payload)
    if response.status_code == 200:
        print("Feature layer updated successfully!")
    else:
        print(f"Error updating feature layer: {response.text}")

# Run the update
update_feature_layer()

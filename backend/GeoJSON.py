import json
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB credentials from environment variables
MONGO_USERNAME = os.getenv("MONGO_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_CLUSTER_URL = os.getenv("MONGO_CLUSTER_URL")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

# MongoDB connection URI
connection_string = f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_CLUSTER_URL}/?retryWrites=true&w=majority"
client = MongoClient(connection_string)
db = client[MONGO_DB_NAME]
collection = db["structured_room_schedule"]

# Initialize the GeoJSON structure
geojson = {
    "type": "FeatureCollection",
    "features": []
}

building_data = collection.find_one()
if not building_data or "buildings" not in building_data:
    print("No building data found or 'buildings' key missing.")
else:
    # Loop through each building in the "buildings" array
    for building_info in building_data["buildings"]:
        building_name = building_info.get("name")


        # Only process if the building is WCP
        total_rooms = building_info.get("total_rooms", 0)

        if total_rooms == 0:
            continue
        coordinates = building_info.get("coordinates")

        if not coordinates:
            print(f"Skipping building due to missing coordinates: {building_name}")
            continue

        latitude = coordinates.get("latitude")
        longitude = coordinates.get("longitude")

        rooms = building_info.get("rooms") 
            
    

        # Create GeoJSON feature
        geojson_feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [longitude, latitude]
            },
            "properties": {
                "name": building_name,
                "total_rooms": total_rooms,
                "rooms": rooms
            }

        }
        geojson["features"].append(geojson_feature)
        print(f"Added feature for building: {building_name}")

# Debugging: Confirm features array is populated
print(f"Total features added: {len(geojson['features'])}")

# Write the GeoJSON data to a file
with open("output_geojson.json", "w") as f:
    json.dump(geojson, f, indent=4)

print("GeoJSON data has been written to output_geojson_test.json")

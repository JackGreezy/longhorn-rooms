from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MongoDB credentials from environment variables
MONGO_USERNAME = os.getenv("MONGO_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_CLUSTER_URL = os.getenv("MONGO_CLUSTER_URL")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

# MongoDB connection URI
connection_string = f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_CLUSTER_URL}/?retryWrites=true&w=majority&appName={MONGO_DB_NAME}"
client = MongoClient(connection_string)
db = client["rooms_db"]
collection = db["structured_room_schedule"]

# Define the dummy coordinates and building name
latitude = 30.28493000207699
longitude = -97.73676103806903
abbreviation = "WCP"

# Debug: Find and print the document structure for WCP
existing_building = collection.find_one({"buildings.name": abbreviation})
if existing_building:
    print("Found existing building structure:")
    # print(existing_building)
else:
    print(f"No document found with building name {abbreviation}")

# Update or add coordinates to the WCP building
result = collection.update_one(
    {"buildings.name": abbreviation},
    {
        "$set": {
            "buildings.$[elem].coordinates": {"latitude": latitude, "longitude": longitude}
        }
    },
    array_filters=[{"elem.name": abbreviation}],
    upsert=True
)

# Check if the operation was successful
if result.modified_count > 0:
    print(f"Updated {abbreviation} with coordinates ({latitude}, {longitude})")
elif result.upserted_id:
    print(f"Inserted new entry for {abbreviation} with coordinates ({latitude}, {longitude})")
else:
    print(f"No changes made to {abbreviation}")

print("Completed updating MongoDB.")

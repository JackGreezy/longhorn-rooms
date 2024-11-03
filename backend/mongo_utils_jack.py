import os
import json
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get MongoDB credentials from environment variables
MONGO_CLUSTER_URL = os.getenv("MONGO_CLUSTER_URL")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
MONGO_USERNAME = os.getenv("MONGO_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")

# MongoDB connection URI
uri = f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_CLUSTER_URL}/?retryWrites=true&w=majority&appName={MONGO_DB_NAME}"

# Connect to MongoDB
client = MongoClient(uri) 
db = client[MONGO_DB_NAME]
collection = db["room_schedules"]  # Name the collection where you want to upload the data

# Load the JSON data from file
with open("backend/structured_room_schedule.json") as file:
    data = json.load(file)

# Insert the JSON data into MongoDB
if isinstance(data, dict):
    # If data is a dictionary, insert it as a single document
    result = collection.insert_one(data)
    print(f"Inserted document with ID: {result.inserted_id}")
elif isinstance(data, list):
    # If data is a list, insert each item as a separate document
    result = collection.insert_many(data)
    print(f"Inserted {len(result.inserted_ids)} documents")
else:
    print("Unexpected data format. Expected a dictionary or list of dictionaries.")

# Close the MongoDB connection
client.close()

from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment variables
load_dotenv()

# MongoDB credentials
MONGO_CLUSTER_URL = os.getenv("MONGO_CLUSTER_URL")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")

# Connect to MongoDB
def get_mongo_data():
    connection_string = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_CLUSTER_URL}/{MONGO_DB_NAME}?retryWrites=true&w=majority"
    client = MongoClient(connection_string)
    db = client[MONGO_DB_NAME]
    collection = db["room_schedules"]

    # Fetch all room schedule data
    room_data = {}
    for building in collection.find():
        building_name = building["_id"]
        room_data[building_name] = {
            "total_rooms": building.get("total_rooms", 0),
            "rooms": [
                {
                    "room_number": room_number,
                    "schedule": room_schedule
                }
                for room_number, room_schedule in building["rooms"].items()
            ]
        }

    client.close()
    return room_data

# Sample function to check room availability
def is_room_available(room_schedule, day, start_time, end_time):
    for schedule in room_schedule:
        if schedule["day"] == day:
            sched_start = datetime.strptime(schedule["start_time"], "%I:%M %p").time()
            sched_end = datetime.strptime(schedule["end_time"], "%I:%M %p").time()
            # Check for any overlap in scheduled time and requested time
            if (sched_start <= end_time and sched_end >= start_time):
                return False
    return True

# Function to get available rooms in a specific building within a time range
def get_available_rooms(building_name, day, start_time, end_time):
    room_data = get_mongo_data()  # Fetch real data from MongoDB
    available_rooms = []
    
    if building_name in room_data:
        for room in room_data[building_name]["rooms"]:
            room_schedule = room["schedule"]
            if is_room_available(room_schedule, day, start_time, end_time):
                available_rooms.append(room["room_number"])
    
    return available_rooms

# Example usage
if __name__ == "__main__":
    day = "Monday"
    start_time = datetime.strptime("04:00 PM", "%I:%M %p").time()
    end_time = datetime.strptime("06:00 PM", "%I:%M %p").time()
    building_name = "RLP"

    available_rooms = get_available_rooms(building_name, day, start_time, end_time)
    print(f"Available rooms in {building_name} from {start_time} to {end_time} on {day}: {available_rooms}")

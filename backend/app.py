from flask import Flask, jsonify, request
from pymongo import MongoClient
from datetime import datetime, timedelta
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

day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# Utility function to get today's day and current time
def get_current_day_and_time():
    now = datetime.now()
    current_day = now.strftime("%A")
    current_time = now.time()
    return current_day, current_time

# Endpoint 1: Get available rooms at the current time
@app.route('/api/available_rooms', methods=['GET'])
def get_available_rooms():
    # Fetch all documents in "room_schedules" collection
    room_schedules = list(db.room_schedules.find({}))
    data = [{**room, "_id": str(room["_id"])} for room in room_schedules]  # Convert ObjectIds to strings
    return jsonify(data)

# def get_available_rooms():
#     building_availability = {}
#     current_day, current_time = get_current_day_and_time()

#     # Query the database for each building and room schedule
#     for building in collection.find():
#         building_name = building["_id"]
#         total_rooms = building["total_rooms"]
#         available_rooms = []
        
#         for room_number, schedules in building["rooms"].items():
#             # Check if room is available at the current time
#             is_available = True
#             for schedule in schedules:
#                 if schedule["day"] == current_day:
#                     start_time = datetime.strptime(schedule["start_time"], "%I:%M %p").time()
#                     end_time = datetime.strptime(schedule["end_time"], "%I:%M %p").time()
#                     if start_time <= current_time <= end_time:
#                         is_available = False
#                         break
#             if is_available:
#                 available_rooms.append(room_number)

#         # Store availability count and room numbers
#         building_availability[building_name] = {
#             "total_rooms": total_rooms,
#             "available_rooms": available_rooms,
#             "available_count": len(available_rooms)
#         }

#     return jsonify(building_availability)

# Endpoint 2: Get available rooms within a specified time range
@app.route('/api/available_rooms_in_range', methods=['GET'])
def get_available_rooms_in_range():
    try:
        day = request.args.get('day')  # Example: "Monday"
        start_time_str = request.args.get('start_time')  # Example: "13:00"
        end_time_str = request.args.get('end_time')  # Example: "15:00"
        
        start_time = datetime.strptime(start_time_str, "%H:%M").time()
        end_time = datetime.strptime(end_time_str, "%H:%M").time()

        building_availability = {}

        # Query the database for each building and room schedule
        for building in collection.find():
            building_name = building["_id"]
            total_rooms = building["total_rooms"]
            available_rooms = []

            for room_number, schedules in building["rooms"].items():
                # Check if room is available within the specified time range
                is_available = True
                for schedule in schedules:
                    if schedule["day"] == day:
                        sched_start = datetime.strptime(schedule["start_time"], "%I:%M %p").time()
                        sched_end = datetime.strptime(schedule["end_time"], "%I:%M %p").time()
                        if not (sched_end <= start_time or sched_start >= end_time):
                            is_available = False
                            break
                if is_available:
                    available_rooms.append(room_number)

            building_availability[building_name] = {
                "total_rooms": total_rooms,
                "available_rooms": available_rooms,
                "available_count": len(available_rooms)
            }

        return jsonify(building_availability)

    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

import os
import json
import re
from datetime import datetime, timedelta
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get MongoDB credentials from environment variables
MONGO_USERNAME = os.getenv("MONGO_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_CLUSTER_URL = os.getenv("MONGO_CLUSTER_URL")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

# MongoDB connection URI
connection_string = f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_CLUSTER_URL}/?retryWrites=true&w=majority&appName={MONGO_DB_NAME}"
client = MongoClient(connection_string)
db = client["rooms_db"]
collection = db["structured_room_schedule"]

# Define helper functions for parsing
def parse_time(time_str):
    time_str = time_str.lower().replace(".", "")  # Remove periods
    match = re.match(r"(\d{1,2}:\d{2})\s*(am|pm)", time_str)
    if match:
        time_str = f"{match.group(1)} {match.group(2).upper()}"
        try:
            return datetime.strptime(time_str, "%I:%M %p").time()
        except ValueError as e:
            print(f"Time format error: '{time_str}' does not match expected format '%I:%M %p'")
            return None
    else:
        print(f"Time format error: '{time_str}' is not in a recognized format")
        return None

def split_days(days_str):
    day_map = {"M": "Monday", "T": "Tuesday", "W": "Wednesday", "TH": "Thursday", "F": "Friday", "S": "Saturday"}
    days = []
    i = 0
    while i < len(days_str):
        if days_str[i:i+2] == "TH":
            days.append(day_map["TH"])
            i += 2
        else:
            days.append(day_map[days_str[i]])
            i += 1
    return days

# Load and structure the course data
with open("backend/ut_courses.json", "r") as file:
    course_data = json.load(file)

structured_data = {}

for course in course_data:
    if not course.get("rooms") or not course.get("days") or not course.get("hours"):
        continue

    building_name, room_number = course["rooms"].split(" ", 1)
    days = split_days(course["days"])
    time_split_char = "–" if "–" in course["hours"] else "-"
    start_time_str, end_time_str = course["hours"].split(time_split_char)
    start_time = parse_time(start_time_str.strip())
    end_time = parse_time(end_time_str.strip())

    if start_time is None or end_time is None:
        continue

    if building_name not in structured_data:
        structured_data[building_name] = {"total_rooms": 0, "rooms": {}}

    if room_number not in structured_data[building_name]["rooms"]:
        structured_data[building_name]["rooms"][room_number] = []
        structured_data[building_name]["total_rooms"] += 1

    for day in days:
        structured_data[building_name]["rooms"][room_number].append({
            "day": day,
            "start_time": start_time.strftime("%I:%M %p"),
            "end_time": end_time.strftime("%I:%M %p"),
            "course_name": course.get("course_name", "Unknown"),
            "instructor": course.get("instructor", "Unknown")
        })

day_order = {
    "Monday": 1,
    "Tuesday": 2,
    "Wednesday": 3,
    "Thursday": 4,
    "Friday": 5,
    "Saturday": 6,
    "Sunday": 7
}

def sort_schedule_by_day_and_time(structured_data):
    for building_name, building_data in structured_data.items():
        for room, schedule in building_data["rooms"].items():
            structured_data[building_name]["rooms"][room].sort(
                key=lambda x: (day_order[x["day"]], datetime.strptime(x["start_time"], "%I:%M %p"))
            )

sort_schedule_by_day_and_time(structured_data)

# Upload structured data to MongoDB
try:
    if isinstance(structured_data, dict):
        result = collection.insert_one(structured_data)
        print(f"Structured data inserted with ID: {result.inserted_id}")
    elif isinstance(structured_data, list):
        result = collection.insert_many(structured_data)
        print(f"Inserted {len(result.inserted_ids)} documents")
    else:
        print("Unexpected data format. Expected a dictionary or list of dictionaries.")
except Exception as e:
    print(f"Error inserting data into MongoDB: {e}")

# Close the MongoDB client
client.close()

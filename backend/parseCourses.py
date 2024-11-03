import os
import json
import re
from datetime import datetime
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

# Initialize structured data with a list of buildings
structured_data = []

# Temporary dictionary to hold buildings for easy access before sorting
temp_buildings = {}

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

    if building_name not in temp_buildings:
        temp_buildings[building_name] = {"name": building_name, "rooms": {}}

    if room_number not in temp_buildings[building_name]["rooms"]:
        temp_buildings[building_name]["rooms"][room_number] = []

    for day in days:
        temp_buildings[building_name]["rooms"][room_number].append({
            "day": day,
            "start_time": start_time.strftime("%I:%M %p"),
            "end_time": end_time.strftime("%I:%M %p"),
            "course_name": course.get("course_name", "Unknown"),
            "instructor": course.get("instructor", "Unknown")
        })

# Function to define a custom sorting key for room numbers
def room_sort_key(room):
    # Use regex to extract numbers from the room number, if any
    numbers = re.findall(r'\d+', room)
    # Convert extracted numbers to integers for sorting, fill with large value if missing part
    main_number = int(numbers[0]) if numbers else float('inf')
    sub_number = int(numbers[1]) if len(numbers) > 1 else float('inf')
    return (main_number, sub_number)

# Sort rooms and convert buildings to the final structure
for building_name in sorted(temp_buildings):
    building = temp_buildings[building_name]
    sorted_rooms = sorted(building["rooms"].items(), key=lambda x: room_sort_key(x[0]))  # Sort rooms by custom key
    structured_data.append({
        "name": building_name,
        "total_rooms": len(sorted_rooms),
        "rooms": [
            {
                "room_number": room_number,
                "schedule": schedule
            }
            for room_number, schedule in sorted_rooms
        ]
    })

# Function to sort schedule by day and time
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
    for building in structured_data:
        for room in building["rooms"]:
            room["schedule"].sort(
                key=lambda x: (day_order[x["day"]], datetime.strptime(x["start_time"], "%I:%M %p"))
            )

# Apply sorting to the schedules
sort_schedule_by_day_and_time(structured_data)

# Upload structured data to MongoDB
try:
    collection.delete_many({})  # Clear any existing data
    result = collection.insert_one({"buildings": structured_data})
    print(f"Structured data inserted with ID: {result.inserted_id}")
except Exception as e:
    print(f"Error inserting data into MongoDB: {e}")

# Close the MongoDB client
client.close()

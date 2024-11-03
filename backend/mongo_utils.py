from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from datetime import datetime, timezone
import os
from dotenv import load_dotenv
import json
from datetime import timedelta

load_dotenv()

MONGO_USERNAME = os.getenv("MONGO_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_CLUSTER_URL = os.getenv("MONGO_CLUSTER_URL")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

day_mapping = {
    "M": 0,  # Monday
    "T": 1,  # Tuesday
    "W": 2,  # Wednesday
    "TH": 3,  # Thursday
    "F": 4,  # Friday
    "S": 5,  # Saturday
    "SU": 6  # Sunday
}

def connect_to_mongo():
    try:
        connection_string = f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_CLUSTER_URL}/?retryWrites=true&w=majority&appName={MONGO_DB_NAME}"
        print(connection_string)
        client = MongoClient(connection_string, ssl=True)
        print(client.list_database_names())  # This will raise an error if the connection fails
        return client
    except ConnectionFailure as e:
        print(f"Connection failed: {e}")
        return None

def parse_time_range(time_range):
    # Splitting the hours field to extract start and end times
    start_time_str, end_time_str = time_range.split('-')
    
    # Normalize the time strings by removing periods in AM/PM
    start_time_str = start_time_str.replace('.', '').strip()
    end_time_str = end_time_str.replace('.', '').strip()
    
    # Parse the time strings with the updated format
    start_time = datetime.strptime(start_time_str, '%I:%M %p')
    end_time = datetime.strptime(end_time_str, '%I:%M %p')
    return start_time, end_time

def get_class_datetimes(course_data):
    days_str = course_data["days"].upper()
    time_range = course_data["hours"]

    # Parsing the start and end times
    start_time, end_time = parse_time_range(time_range)

    # Creating datetime objects for each class day
    current_date = datetime.now().date()
    class_dates = []
    parsed_days = []

    # Handle cases where days include "TH" for Thursday
    i = 0
    while i < len(days_str):
        if i < len(days_str) - 1 and days_str[i:i+2] == "TH":
            parsed_days.append("TH")
            i += 2
        else:
            parsed_days.append(days_str[i])
            i += 1

    for day in parsed_days:
        if day in day_mapping:
            # Find the next date matching the course day
            days_ahead = (day_mapping[day] - current_date.weekday() + 7) % 7
            class_date = current_date + timedelta(days=days_ahead)
            
            # Creating datetime objects with the parsed time
            class_start_datetime = datetime.combine(class_date, start_time.time())
            class_end_datetime = datetime.combine(class_date, end_time.time())
            
            class_dates.append((class_start_datetime, class_end_datetime))
    
    return class_dates

def get_club_datetime(event_data):
    date_time_str = event_data["date_time"].replace(" at", "")
    date_time_parts = date_time_str.rsplit(' ', 1)[0]  # Remove the time zone abbreviation

    # Parse the date without the year defaulting to 1900
    event_datetime = datetime.strptime(date_time_parts, '%A, %B %d %I:%M%p')

    # Set the correct year
    current_year = datetime.now().year
    event_datetime = event_datetime.replace(year=current_year)

    # Return a tuple similar to class datetimes
    event_end_datetime = event_datetime + timedelta(hours=1)  # Assuming 1-hour event duration

    return event_datetime, event_end_datetime

def upload_data():
    client = connect_to_mongo()

    db = client["rooms_db"]  # Name of your database
    courseRooms = db["course_rooms"]  # Name of your collection
    clubRooms = db["club_rooms"]

    # load courses json
    with open('ut_courses.json') as courseJson:
        courseJson_data = json.load(courseJson)

        for element in courseJson_data:
            if "flags" in element:
                del element["flags"]
            if "status" in element:
                del element["status"]
            if "core" in element:
                del element["core"]

        # fix datetime to standard format
        for i in range(len(courseJson_data)):
            if(courseJson_data[i]["days"] is not None):
                courseJson_data[i]["datetime"] = get_class_datetimes(courseJson_data[i])
                # print(courseJson_data[i]["datetime"])

    # load clubs json
    with open('ut_club_events.json') as clubJson:
        clubJson_data = json.load(clubJson)

        # fix datetime to standard format
        for i in range(len(clubJson_data)):
            clubJson_data[i]["datetime"] = get_club_datetime(clubJson_data[i])
            # print(clubJson_data[i]["datetime"])


    if isinstance(courseJson_data, list):
        courseRooms.insert_many(courseJson_data)
    else:
        courseRooms.insert_one(courseJson_data)

    if isinstance(clubJson_data, list):
        clubRooms.insert_many(clubJson_data)
    else:
        clubRooms.insert_one(clubJson_data)

    client.close()

def get_course_data():
    client = connect_to_mongo()
    db = client["rooms_db"]
    course_rooms_db = db["course_rooms"]
    
    course_rooms = course_rooms_db.find()  # Get all documents in the collection

    print(course_rooms)

    client.close()

    return course_rooms

def get_club_data():
    client = connect_to_mongo()
    db = client["rooms_db"]
    club_rooms_db = db["club_rooms"]

    club_rooms = club_rooms_db.find()

    print(club_rooms)

    client.close()

    return club_rooms

def clear_course_data():
    client = connect_to_mongo()

    if not client:
        print("Failed to connect to MongoDB")
        return []

    db = client["rooms_db"]
    course_data = db["course_rooms"]

    course_data.delete_many({})

    client.close()

    print("All documents in the 'course' collection have been deleted.")

def clear_club_data():
    client = connect_to_mongo()

    if not client:
        print("Failed to connect to MongoDB")
        return []

    db = client["rooms_db"]
    club_data = db["club_rooms"]

    club_data.delete_many({})

    client.close()

    print("All documents in the 'club' collection have been deleted.")

upload_data()
# clear_club_data()
# clear_course_data()
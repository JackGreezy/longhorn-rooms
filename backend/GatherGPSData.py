from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
import time
import requests
from urllib.parse import quote
import geocoder
import os

# Initialize the MongoDB client

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

# Initialize the Selenium driver
driver = webdriver.Chrome()  # Or use webdriver.Firefox() if preferred
driver.get("https://utdirect.utexas.edu/apps/campus/buildings/nlogon/facilities/")

# List to store building abbreviations
building_abbreviations = []

try:
    # Scraping all building abbreviations
    while True:
        # Wait for rows to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table tbody tr.odd, table tbody tr.even"))
        )

        # Collect building abbreviations
        building_rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr.odd, table tbody tr.even")
        for row in building_rows:
            abbreviation = row.find_element(By.CSS_SELECTOR, "th a").text
            building_abbreviations.append(abbreviation)

        # Click the Next button if available
        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Next"))
            )
            next_button.click()
            WebDriverWait(driver, 10).until(
                EC.staleness_of(building_rows[0])
            )
        except:
            print("Reached the last page.")
            break

finally:
    driver.quit()

# Convert Address to Coordinates Function


import requests
from urllib.parse import quote
import time

# Convert Address to Coordinates Function with Headers and Throttling
def get_coordinates(address):
    try:
        # Use geocoder.arcgis instead of geocoder.osm to avoid 403 errors
        g = geocoder.arcgis(address)
        print(g.latlng)
        
        if g.ok:
            return g.latlng  # Returns a tuple (lat, lon)
        else:
            print(f"No results found for address: {address}")
            return None, None

    except Exception as e:
        print(f"Geocoding failed for address '{address}': {e}")
        return None, None
    finally:
        # Throttle requests to avoid rate limiting
        time.sleep(1)  # Adjust delay as needed


# Loop through each building abbreviation and extract GPS coordinates
for abbreviation in building_abbreviations:
    # Construct the building URL
    building_url = f"https://utdirect.utexas.edu/apps/campus/buildings/nlogon/facilities/utm/{abbreviation}/"
    print(building_url)
    response = requests.get(building_url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Extract the address based on the HTML structure
        address_tag = soup.select_one("h3").text.strip()

        print(address_tag)
        
        if address_tag:
            # Convert the address to GPS coordinates
            lat, lon = get_coordinates(address_tag)
            
            if lat is not None and lon is not None:
                # Check if the building already exists in MongoDB
                building = collection.find_one({"buildings.name": abbreviation})
                
                if building:
                    # Update coordinates for the existing building entry
                    collection.update_one(
                        {"buildings.name": abbreviation},
                        {"$set": {
                            "buildings.$.coordinates": {"latitude": lat, "longitude": lon}
                        }}
                    )
                else:
                    # Add a new building entry
                    collection.update_one(
                        {"buildings": {"$exists": True}},
                        {"$push": {
                            "buildings": {
                                "name": abbreviation,
                                "coordinates": {"latitude": lat, "longitude": lon},
                                "total_rooms": 0,
                                "rooms": []
                            }
                        }},
                        upsert=True
                    )
                print(f"Added/Updated {abbreviation} with coordinates ({lat}, {lon})")
            else:
                print(f"Coordinates not found for address: {address_tag}")
        else:
            print(f"Address not found for {abbreviation}")
    else:
        print(f"Failed to retrieve data for {abbreviation}, status code: {response.status_code}")

print("Completed updating MongoDB.")

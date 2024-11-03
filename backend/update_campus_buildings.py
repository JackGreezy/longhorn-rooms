from arcgis.gis import GIS
from arcgis.features import FeatureLayer
import requests
import os

# ArcGIS credentials and settings
GIS_URL = "https://www.arcgis.com"  # Change if using ArcGIS Enterprise
USERNAME = os.getenv("ARCGIS_USERNAME")
PASSWORD = os.getenv("ARCGIS_PASSWORD")

# Initialize GIS connection
gis = GIS(GIS_URL, USERNAME, PASSWORD)

# URL of the Campus_Building layer
CAMPUS_BUILDING_LAYER_URL = "YOUR_CAMPUS_BUILDING_LAYER_URL"  # Replace with your feature layer URL
campus_building_layer = FeatureLayer(CAMPUS_BUILDING_LAYER_URL)

# API URL to get real-time building availability data
API_URL = "https://www.longhornrooms.com/api/building_availability_json"

def update_campus_building_layer():
    # Step 1: Fetch data from your API
    response = requests.get(API_URL)
    building_data = response.json()

    # Step 2: Iterate through each building and update the layer
    for building in building_data:
        building_abbr = building["Building_Abbr"]
        available_count = building["available_count"]
        total_rooms = building["total_rooms"]

        # Query to find the matching feature in the Campus_Building layer
        query = f"Building_Abbr='{building_abbr}'"
        features = campus_building_layer.query(where=query).features

        if features:
            # Update available_count and total_rooms fields
            feature = features[0]
            feature.attributes["available_count"] = available_count
            feature.attributes["total_rooms"] = total_rooms
            campus_building_layer.edit_features(updates=[feature])

    print("Campus building layer updated with room availability data.")

# Run the update function
if __name__ == "__main__":
    update_campus_building_layer()

import requests
from token_manager import get_access_token

def fetch_feature_layer_data():
    # Get the access token
    access_token = get_access_token()
    if not access_token:
        print("Access token is missing.")
        return None
    
    # Define the feature layer URL
    feature_layer_url = "https://ut-austin.maps.arcgis.com/home/item.html?id=48754e1434bf4319aa6168fad6c80a10"
    
    # Set the headers with the token
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    # Define parameters for the request
    params = {
        "where": "1=1",  # Get all records
        "outFields": "*",  # Get all fields
        "f": "json"       # Response format
    }
    
    # Make the request
    response = requests.get(feature_layer_url, headers=headers, params=params)
    
    # Debugging: Print raw response details
    print("Status Code:", response.status_code)
    print("Raw response:", response.text)

    # Check for a successful response and parse the JSON
    if response.status_code == 200:
        try:
            data = response.json()
            print("Feature Layer Data:", data)
            return data
        except requests.exceptions.JSONDecodeError:
            print("Failed to decode JSON. Response might not be in JSON format.")
            return None
    else:
        print("Failed to fetch feature layer data.")
        print("Response status code:", response.status_code)
        print("Response content:", response.text)
        return None

# Example usage and debugging entry point
if __name__ == "__main__":
    print("Testing token generation and API request...")
    feature_data = fetch_feature_layer_data()
    if feature_data:
        print("Data successfully retrieved.")
    else:
        print("Data retrieval failed.")

import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ArcGIS OAuth credentials
CLIENT_ID = os.getenv("ARCGIS_CLIENT_ID")
CLIENT_SECRET = os.getenv("ARCGIS_CLIENT_SECRET")
TOKEN_URL = "https://www.arcgis.com/sharing/rest/oauth2/token"

def get_access_token():
    # Prepare the payload
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials",
        "f": "json"
    }
    
    # Request the token
    response = requests.post(TOKEN_URL, data=payload)
    
    # Debugging: Print response details
    print("Token request status code:", response.status_code)
    print("Token response:", response.text)
    
    # Check if the token was successfully generated
    if response.status_code == 200:
        try:
            data = response.json()
            access_token = data.get("access_token")
            if access_token:
                print("Access token successfully generated.")
                return access_token
            else:
                print("Access token not found in the response.")
                return None
        except requests.exceptions.JSONDecodeError:
            print("Failed to decode JSON for token generation.")
            return None
    else:
        print("Failed to generate token. Status code:", response.status_code)
        return None

# Test token generation separately
if __name__ == "__main__":
    print("Testing token generation...")
    token = get_access_token()
    if token:
        print("Token:", token)
    else:
        print("Failed to retrieve token.")

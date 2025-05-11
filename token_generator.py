import os
import requests
from kiteconnect import KiteConnect
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Step 1: Get credentials from environment
api_key = os.getenv("KITE_API_KEY")
api_secret = os.getenv("KITE_API_SECRET")
request_token = os.getenv("REQUEST_TOKEN")
render_api_key = os.getenv("RENDER_API_KEY")
render_service_id = os.getenv("RENDER_SERVICE_ID")

# Step 2: Generate access token
kite = KiteConnect(api_key=api_key)
session = kite.generate_session(request_token, api_secret=api_secret)
access_token = session["access_token"]
print("\U00002705 Access token generated:", access_token)

# Step 3: Update access token in Render environment
def update_access_token_to_render():
    url = f"https://api.render.com/v1/services/{render_service_id}/env-vars"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {render_api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "values": {
            "KITE_ACCESS_TOKEN": access_token
        }
    }
    response = requests.put(url, headers=headers, json=payload)
    if response.status_code == 200:
        print("\U00002705 Access token successfully updated in Render bot service.")
    else:
        print("\U0000274C Failed to update access token. Status code:", response.status_code)
        print(response.text)

# Run the update
update_access_token_to_render()

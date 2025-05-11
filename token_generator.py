import os
import requests
from kiteconnect import KiteConnect
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Step 1: Kite API credentials
api_key = os.getenv("KITE_API_KEY")
api_secret = os.getenv("KITE_API_SECRET")
request_token = os.getenv("REQUEST_TOKEN")

# Step 2: Generate session and access token
kite = KiteConnect(api_key=api_key)
session = kite.generate_session(request_token, api_secret=api_secret)
access_token = session["access_token"]
print("✅ Access token generated:", access_token)

# Step 3: Update RENDER environment variable using API
render_api_key = os.getenv("RENDER_API_KEY")
render_service_id = os.getenv("RENDER_SERVICE_ID")

if not render_api_key or not render_service_id:
    print("❌ Missing RENDER_API_KEY or RENDER_SERVICE_ID")
    exit()

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
    print("✅ Access token updated in Render environment.")
else:
    print("❌ Failed to update access token. Status code:", response.status_code)
    print(response.text)

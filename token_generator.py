import os
import json
import requests
from kiteconnect import KiteConnect
from dotenv import load_dotenv

load_dotenv()

# Fetch credentials
api_key = os.getenv("KITE_API_KEY")
api_secret = os.getenv("KITE_API_SECRET")
request_token = os.getenv("REQUEST_TOKEN")
render_api_key = os.getenv("RENDER_API_KEY")
render_service_id = os.getenv("RENDER_SERVICE_ID")

# Step 1: Generate access token from request token
kite = KiteConnect(api_key=api_key)
try:
    session = kite.generate_session(request_token, api_secret=api_secret)
    access_token = session["access_token"]
    print("✅ Access token generated:", access_token)
except Exception as e:
    print("❌ Failed to generate access token:", str(e))
    exit(1)

# Step 2: Update access token in Render environment
url = f"https://api.render.com/v1/services/{render_service_id}/env-vars"

headers = {
    "Authorization": f"Bearer {render_api_key}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

payload = {
    "envVars": [
        {
            "key": "KITE_ACCESS_TOKEN",
            "value": access_token
        }
    ]
}

try:
    response = requests.patch(url, headers=headers, json=payload)
    if response.status_code == 200:
        print("✅ Access token updated successfully in Render service.")
    else:
        print(f"❌ Failed to update access token. Status code: {response.status_code}")
        print("Response:", response.text)
except Exception as e:
    print("❌ Error updating token to Render:", str(e))

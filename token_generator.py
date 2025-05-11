import os
import requests
from kiteconnect import KiteConnect
from dotenv import load_dotenv

load_dotenv()

# Step 1: Get all necessary environment variables
api_key = os.getenv("KITE_API_KEY")
api_secret = os.getenv("KITE_API_SECRET")
request_token = os.getenv("REQUEST_TOKEN")
render_api_key = os.getenv("RENDER_API_KEY")
render_service_id = os.getenv("RENDER_SERVICE_ID")

# Step 2: Generate access token from Kite
kite = KiteConnect(api_key=api_key)
try:
    session = kite.generate_session(request_token, api_secret=api_secret)
    access_token = session["access_token"]
    print(f"✅ Access token generated: {access_token}")
except Exception as e:
    print(f"❌ Failed to generate access token:\n{e}")
    exit()

# Step 3: Update Render Environment variable using POST
url = f"https://api.render.com/v1/services/{render_service_id}/env-vars"
headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {render_api_key}",
    "Content-Type": "application/json"
}
payload = {
    "envVars": [
        {
            "key": "KITE_ACCESS_TOKEN",
            "value": access_token,
            "previewValue": access_token
        }
    ]
}

try:
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print("✅ KITE_ACCESS_TOKEN successfully updated in Render")
    else:
        print(f"❌ Failed to update token. Status: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"❌ Exception occurred while updating token:\n{e}")

import os
import json
import requests
from kiteconnect import KiteConnect
from dotenv import load_dotenv

load_dotenv()

# Load credentials
api_key = os.getenv("KITE_API_KEY")
api_secret = os.getenv("KITE_API_SECRET")
request_token = os.getenv("REQUEST_TOKEN")
render_api_key = os.getenv("RENDER_API_KEY")
render_service_id = os.getenv("RENDER_SERVICE_ID")

# Generate session and access token
kite = KiteConnect(api_key=api_key)
try:
    session = kite.generate_session(request_token, api_secret=api_secret)
    access_token = session["access_token"]
    print("✅ Access token generated:", access_token)
except Exception as e:
    print("❌ Failed to generate access token:", str(e))
    exit(1)

# Update CE-PE-NIFTY environment variable via Render API
url = f"https://api.render.com/v1/services/{render_service_id}/env-vars"

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {render_api_key}"
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
    response = requests.patch(url, headers=headers, data=json.dumps(payload))
    if response.status_code in [200, 201]:
        print("✅ Access token updated in CE-PE-NIFTY environment.")
    else:
        print(f"❌ Failed to update access token. Status code: {response.status_code}")
        print("Response:", response.text)
except Exception as e:
    print("❌ Exception during environment update:", str(e))

import os
import json
import requests
from kiteconnect import KiteConnect
from dotenv import load_dotenv

load_dotenv()

# Load env vars
api_key = os.getenv("KITE_API_KEY")
api_secret = os.getenv("KITE_API_SECRET")
request_token = os.getenv("REQUEST_TOKEN")
render_api_key = os.getenv("RENDER_API_KEY")
render_service_id = os.getenv("RENDER_SERVICE_ID")

# Generate access token
kite = KiteConnect(api_key=api_key)
try:
    session = kite.generate_session(request_token, api_secret=api_secret)
    access_token = session["access_token"]
    print("✅ Access token generated:", access_token)
except Exception as e:
    print("❌ Token generation failed:", str(e))
    exit(1)

# Correct PUT request to Render API
url = f"https://api.render.com/v1/services/{render_service_id}/env-vars"
headers = {
    "Authorization": f"Bearer {render_api_key}",
    "Content-Type": "application/json"
}
payload = {
    "envVars": [
        {
            "key": "KITE_ACCESS_TOKEN",
            "value": access_token,
            "alias": None
        }
    ]
}

try:
    response = requests.put(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        print("✅ Access token updated in CE-PE-NIFTY env.")
    else:
        print(f"❌ Failed to update token. Status: {response.status_code}")
        print("Response:", response.text)
except Exception as e:
    print("❌ Exception during update:", str(e))

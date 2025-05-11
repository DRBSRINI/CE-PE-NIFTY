import os
import requests
from kiteconnect import KiteConnect
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Fetch from env
api_key = os.getenv("KITE_API_KEY")
api_secret = os.getenv("KITE_API_SECRET")
request_token = os.getenv("REQUEST_TOKEN")
render_api_key = os.getenv("RENDER_API_KEY")
render_service_id = os.getenv("RENDER_SERVICE_ID")

# Authenticate with Kite
kite = KiteConnect(api_key=api_key)

try:
    session = kite.generate_session(request_token, api_secret=api_secret)
    access_token = session["access_token"]
    print(f"✅ Access token generated: {access_token}")
except Exception as e:
    print(f"❌ Failed to generate access token:\n{e}")
    exit()

# PATCH to Render API to update KITE_ACCESS_TOKEN env var
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
            "value": access_token
        }
    ]
}

try:
    res = requests.patch(url, headers=headers, json=payload)
    if res.status_code == 200:
        print("✅ KITE_ACCESS_TOKEN updated in Render bot service.")
    else:
        print(f"❌ Failed to update token. Status: {res.status_code}\n{res.text}")
except Exception as e:
    print(f"❌ Exception while updating token:\n{e}")

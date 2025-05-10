import os
import requests
from kiteconnect import KiteConnect
from dotenv import load_dotenv

load_dotenv()

# Kite details
api_key = os.getenv("KITE_API_KEY")
api_secret = os.getenv("KITE_API_SECRET")
request_token = os.getenv("REQUEST_TOKEN")

# Render details
render_api_key = os.getenv("RENDER_API_KEY")
render_service_id = os.getenv("RENDER_SERVICE_ID")
render_api_url = f"https://api.render.com/v1/services/{render_service_id}/envVars"

kite = KiteConnect(api_key=api_key)
session = kite.generate_session(request_token, api_secret=api_secret)
access_token = session["access_token"]

# Update Render environment
headers = {
    "Authorization": f"Bearer {render_api_key}",
    "Content-Type": "application/json"
}

payload = [{
    "key": "KITE_ACCESS_TOKEN",
    "value": access_token
}]

response = requests.patch(render_api_url, headers=headers, json=payload)

if response.ok:
    print("✅ Access token updated successfully in Render environment")
else:
    print(f"❌ Failed to update Render environment: {response.status_code} {response.text}")

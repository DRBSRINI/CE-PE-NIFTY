import os
import requests
import pyotp
from kiteconnect import KiteConnect
from urllib.parse import urlparse, parse_qs

# 1. Load from Render ENV
api_key = os.getenv("KITE_API_KEY")
api_secret = os.getenv("KITE_API_SECRET")
user_id = os.getenv("KITE_USER_ID")
password = os.getenv("KITE_PASSWORD")
totp_key = os.getenv("KITE_TOTP")

render_service_id = os.getenv("RENDER_SERVICE_ID")  # CE-PE-NIFTY
render_api_key = os.getenv("RENDER_API_KEY")        # Your Render API Key

# 2. Create session
session = requests.Session()
totp = pyotp.TOTP(totp_key)
totp_code = totp.now()

# 3. Step-by-step login
try:
    res = session.post("https://kite.zerodha.com/api/login", data={"user_id": user_id, "password": password})
    request_id = res.json().get("data", {}).get("request_id")
    if not request_id:
        raise Exception("Login failed. Check password or ID.")

    session.post("https://kite.zerodha.com/api/twofa", data={"user_id": user_id, "request_id": request_id, "twofa_value": totp_code})
    redirect_res = session.get(f"https://kite.trade/connect/login?api_key={api_key}")
    parsed = urlparse(redirect_res.url)
    request_token = parse_qs(parsed.query).get("request_token", [None])[0]
    if not request_token:
        raise Exception("Request token missing in redirect URL.")

    # 4. Get access token
    kite = KiteConnect(api_key=api_key)
    data = kite.generate_session(request_token=request_token, api_secret=api_secret)
    access_token = data["access_token"]
    print("✅ Access Token:", access_token)

        # 5. PATCH Render env var
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
    patch_url = f"https://api.render.com/v1/services/{render_service_id}/env-vars"
    response = requests.patch(patch_url, headers=headers, json=payload)

    if response.status_code == 200:
        print("✅ Access token updated in Render service.")
    else:
        print(f"❌ Failed to update token. Status {response.status_code}. Message: {response.text}")

# token_generator.py (Render Cron Job Script)

import os
import sys
import pyotp
import requests
from urllib.parse import urlparse, parse_qs
from kiteconnect import KiteConnect

# --- Load credentials from Render environment ---
username = os.environ.get("KITE_USER_ID")
password = os.environ.get("KITE_PASSWORD")
totp_key = os.environ.get("KITE_TOTP")
api_key = os.environ.get("KITE_API_KEY")
api_secret = os.environ.get("KITE_API_SECRET")
render_service_id = os.environ.get("RENDER_SERVICE_ID")
render_api_key = os.environ.get("RENDER_API_KEY")

kite = KiteConnect(api_key=api_key)


def generate_access_token():
    try:
        session = requests.Session()

        # Step 1: Kite login
        login_resp = session.post("https://kite.zerodha.com/api/login", data={
            "user_id": username,
            "password": password
        }).json()
        request_id = login_resp["data"]["request_id"]

        # Step 2: Submit TOTP
        otp = pyotp.TOTP(totp_key).now()
        session.post("https://kite.zerodha.com/api/twofa", data={
            "user_id": username,
            "request_id": request_id,
            "twofa_value": otp
        })

        # Step 3: Fetch request token from redirect URL
        auth_resp = session.get(f"https://kite.trade/connect/login?api_key={api_key}")
        parsed = urlparse(auth_resp.url)
        request_token = parse_qs(parsed.query)["request_token"][0]

        # Step 4: Generate access token
        session_data = kite.generate_session(request_token, api_secret=api_secret)
        access_token = session_data["access_token"]
        print("✅ Access Token Generated:", access_token)

        update_render_env(access_token)

    except Exception as e:
        print("❌ Failed to generate access token:", str(e))
        sys.exit(1)


def update_render_env(access_token):
    try:
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

        response = requests.patch(url, json=payload, headers=headers)

        if response.status_code == 200:
            print("✅ Access token updated in Render env.")
        else:
            print("❌ Failed to update token. Status:", response.status_code)
            print("Response:", response.text)

    except Exception as e:
        print("❌ Error updating token in Render:", str(e))
        sys.exit(1)


if __name__ == "__main__":
    generate_access_token()

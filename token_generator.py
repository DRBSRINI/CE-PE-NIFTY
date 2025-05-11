import os
import pyotp
import requests
from kiteconnect import KiteConnect

# Load environment variables
kite_user = os.environ.get("KITE_USER_ID")
kite_pwd = os.environ.get("KITE_PASSWORD")
kite_totp = os.environ.get("KITE_TOTP")
kite_api_key = os.environ.get("KITE_API_KEY")
kite_api_secret = os.environ.get("KITE_API_SECRET")

kite = KiteConnect(api_key=kite_api_key)

def generate_access_token():
    try:
        print("🔐 Initiating login session...")
        session = requests.Session()

        # Step 1: Login and fetch request_id
        resp = session.post("https://kite.zerodha.com/api/login", {
            "user_id": kite_user,
            "password": kite_pwd
        })
        request_id = resp.json()["data"]["request_id"]

        # Step 2: 2FA verification using TOTP
        session.post("https://kite.zerodha.com/api/twofa", {
            "user_id": kite_user,
            "request_id": request_id,
            "twofa_value": pyotp.TOTP(kite_totp).now()
        })

        # Step 3: Redirect to request_token
        login_url = f"https://kite.trade/connect/login?api_key={kite_api_key}"
        response = session.get(login_url, allow_redirects=False)
        location = response.headers.get("Location")
        request_token = location.split("request_token=")[1].split("&")[0]

        # Step 4: Exchange for access_token
        data = kite.generate_session(request_token, api_secret=kite_api_secret)
        access_token = data["access_token"]

        # Save to file instead of .env
        with open("access_token.txt", "w") as f:
            f.write(access_token)

        print("✅ Access token generated and saved.")
        return access_token

    except Exception as e:
        print(f"❌ Failed: {e}")
        return None

if __name__ == "__main__":
    generate_access_token()

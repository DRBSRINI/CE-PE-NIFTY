import os
from kiteconnect import KiteConnect
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("KITE_API_KEY")
api_secret = os.getenv("KITE_API_SECRET")
request_token = os.getenv("REQUEST_TOKEN")

kite = KiteConnect(api_key=api_key)
try:
    session = kite.generate_session(request_token, api_secret=api_secret)
    access_token = session["access_token"]
    print("✅ Access token generated:", access_token)

    # Update .env file (Option 1)
    with open(".env", "r") as f:
        lines = f.readlines()

    with open(".env", "w") as f:
        for line in lines:
            if line.startswith("KITE_ACCESS_TOKEN="):
                f.write(f"KITE_ACCESS_TOKEN={access_token}\n")
            else:
                f.write(line)
    print("✅ Access token updated in .env")

except Exception as e:
    print("❌ Failed to generate access token:", e)

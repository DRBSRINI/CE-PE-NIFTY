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
    print(f"✅ Access token generated: {access_token}")

    # Update .env file
    updated = False
    with open(".env", "r") as file:
        lines = file.readlines()

    with open(".env", "w") as file:
        for line in lines:
            if line.startswith("KITE_ACCESS_TOKEN"):
                file.write(f"KITE_ACCESS_TOKEN={access_token}\n")
                updated = True
            else:
                file.write(line)
        if not updated:
            file.write(f"KITE_ACCESS_TOKEN={access_token}\n")

    print("✅ Access token updated in .env")

except Exception as e:
    print("❌ Failed to generate access token.")
    print(f"Error: {e}")

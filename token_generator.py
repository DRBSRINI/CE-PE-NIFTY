import os
from kiteconnect import KiteConnect
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("KITE_API_KEY")
api_secret = os.getenv("KITE_API_SECRET")
request_token = os.getenv("REQUEST_TOKEN")

kite = KiteConnect(api_key=api_key)

try:
    print("🔑 Step 1: Attempting to generate session...")
    session = kite.generate_session(request_token, api_secret=api_secret)
    print(f"✅ Step 2: Session response: {session}")

    access_token = session.get("access_token")
    if not access_token:
        print("❌ ERROR: Access token missing from session response.")
        exit(1)
    else:
        print(f"✅ Access token generated: {access_token}")

    if os.path.exists(".env"):
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

        print("✅ Access token successfully written into .env file.")
    else:
        print("❌ ERROR: .env file not found; cannot write access token.")

except Exception as e:
    print("❌ ERROR: Exception occurred during access token generation.")
    print(f"Details: {e}")

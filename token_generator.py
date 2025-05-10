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
except Exception as e:
    print(f"❌ Failed to generate access token: {e}")

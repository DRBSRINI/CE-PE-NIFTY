import os
import json
import logging
import pyotp
from kiteconnect import KiteConnect
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_KEY = os.getenv("KITE_API_KEY")
API_SECRET = os.getenv("KITE_API_SECRET")
KITE_USER_ID = os.getenv("KITE_USER_ID")
KITE_PASSWORD = os.getenv("KITE_PASSWORD")
KITE_TOTP = os.getenv("KITE_TOTP")
RENDER_API_KEY = os.getenv("RENDER_API_KEY")
RENDER_SERVICE_ID = os.getenv("RENDER_SERVICE_ID")

if not all([API_KEY, API_SECRET, KITE_USER_ID, KITE_PASSWORD, KITE_TOTP, RENDER_API_KEY, RENDER_SERVICE_ID]):
    raise EnvironmentError("Missing required environment variables")

kite = KiteConnect(api_key=API_KEY)

# Generate TOTP
totp = pyotp.TOTP(KITE_TOTP).now()

try:
    request_token = kite.generate_session(
        request_token=None,  # None for TOTP login
        api_secret=API_SECRET,
    )
except Exception as e:
    logger.error(f"Login failed: {str(e)}")
    raise

access_token = kite.access_token
logger.info(f"Access Token: {access_token}")

# Update Render env variable
import requests

url = f"https://api.render.com/v1/services/{RENDER_SERVICE_ID}/env-vars"
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {RENDER_API_KEY}"
}

payload = {
    "envVars": [
        {
            "key": "ACCESS_TOKEN",
            "value": access_token
        }
    ]
}

try:
    response = requests.patch(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        logger.info("ACCESS_TOKEN updated successfully on Render.")
    else:
        logger.error(f"Failed to update token. Status {response.status_code}. Message: {response.text}")
except Exception as e:
    logger.error(f"Exception while updating ACCESS_TOKEN: {str(e)}")

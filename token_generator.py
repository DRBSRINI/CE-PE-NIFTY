import os
import json
import logging
import pyotp
import requests
from kiteconnect import KiteConnect
from dotenv import load_dotenv

load_dotenv()

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
API_KEY = os.getenv("KITE_API_KEY")
API_SECRET = os.getenv("KITE_API_SECRET")
USER_ID = os.getenv("KITE_USER_ID")
PASSWORD = os.getenv("KITE_PASSWORD")
TOTP_SECRET = os.getenv("KITE_TOTP")
RENDER_API_KEY = os.getenv("RENDER_API_KEY")
RENDER_SERVICE_ID = os.getenv("RENDER_SERVICE_ID")

# Safety check
required_vars = [API_KEY, API_SECRET, USER_ID, PASSWORD, TOTP_SECRET, RENDER_API_KEY, RENDER_SERVICE_ID]
if not all(required_vars):
    raise EnvironmentError("Missing one or more required environment variables.")

# Setup KiteConnect
kite = KiteConnect(api_key=API_KEY)

# Generate TOTP
totp = pyotp.TOTP(TOTP_SECRET).now()

try:
    session_data = kite.login_with_credentials(
        user_id=USER_ID,
        password=PASSWORD,
        twofa=totp
    )
    access_token = session_data["access_token"]
    logger.info(f"Access Token: {access_token}")
except Exception as e:
    logger.error(f"Login failed: {str(e)}")
    raise

# Update ACCESS_TOKEN in Render Environment
render_url = f"https://api.render.com/v1/services/{RENDER_SERVICE_ID}/env-vars"
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
    response = requests.patch(render_url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        logger.info("ACCESS_TOKEN updated successfully on Render.")
    else:
        logger.error(f"Failed to update token. Status {response.status_code}. Message: {response.text}")
except Exception as e:
    logger.error(f"Error during ACCESS_TOKEN update: {str(e)}")

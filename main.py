import os
import logging
from kiteconnect import KiteConnect
from datetime import datetime
import pytz
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NiftyBot")

API_KEY = os.getenv("KITE_API_KEY")
ACCESS_TOKEN = os.getenv("KITE_ACCESS_TOKEN")

kite = KiteConnect(api_key=API_KEY)
kite.set_access_token(ACCESS_TOKEN)

def run_strategy():
    try:
        ltp = kite.ltp("NSE:NIFTY 50")["NSE:NIFTY 50"]["last_price"]
        logger.info(f"NIFTY LTP: {ltp}")
    except Exception as e:
        logger.error(f"Strategy execution failed: {e}")

if __name__ == "__main__":
    run_strategy()

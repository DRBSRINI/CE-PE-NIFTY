import os
from kiteconnect import KiteConnect
from datetime import datetime
import pytz
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NiftyBot")

API_KEY = os.getenv("KITE_API_KEY")
ACCESS_TOKEN = os.getenv("KITE_ACCESS_TOKEN")

kite = KiteConnect(api_key=API_KEY)
kite.set_access_token(ACCESS_TOKEN)

IST = pytz.timezone('Asia/Kolkata')

def run_strategy():
    now = datetime.now(IST)
    logger.info(f"Running strategy at {now}")
    # Strategy logic placeholder

if __name__ == "__main__":
    scheduler = BlockingScheduler(timezone="Asia/Kolkata")
    scheduler.add_job(run_strategy, 'interval', minutes=1)
    logger.info("🚀 Nifty Options Zerodha Bot Started")
    run_strategy()
    scheduler.start()

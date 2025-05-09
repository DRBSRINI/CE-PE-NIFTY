import os
import logging
from kiteconnect import KiteConnect
from datetime import datetime
import pytz
from apscheduler.schedulers.blocking import BlockingScheduler
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("NiftyBot")

API_KEY = os.getenv("KITE_API_KEY")
ACCESS_TOKEN = os.getenv("KITE_ACCESS_TOKEN")
kite = KiteConnect(api_key=API_KEY)
kite.set_access_token(ACCESS_TOKEN)

IST = pytz.timezone('Asia/Kolkata')

def is_market_hours():
    now = datetime.now(IST)
    logger.debug(f"Current time: {now}")
    in_hours = now.hour >= 9 and (now.hour < 15 or (now.hour == 15 and now.minute <= 15))
    logger.debug(f"Is market open? {in_hours}")
    return in_hours

def get_nifty_atm_option_tokens():
    try:
        ltp_data = kite.ltp("NSE:NIFTY 50")
        nifty_price = ltp_data["NSE:NIFTY 50"]["last_price"]
        atm_strike = round(nifty_price / 50) * 50
        logger.debug(f"NIFTY price: {nifty_price}, ATM Strike: {atm_strike}")

        instruments = kite.instruments("NFO")
        expiry_dates = sorted(set([e["expiry"] for e in instruments if e["name"] == "NIFTY" and "CE" in e["tradingsymbol"]]))
        weekly_expiry = expiry_dates[0].strftime("%d%b%y").upper()

        ce_symbol = f"NIFTY{weekly_expiry}{atm_strike}CE"
        pe_symbol = f"NIFTY{weekly_expiry}{atm_strike}PE"
        logger.debug(f"Looking for CE: {ce_symbol}, PE: {pe_symbol}")

        tokens = {e["tradingsymbol"]: e["instrument_token"] for e in instruments if e["tradingsymbol"] in [ce_symbol, pe_symbol]}
        logger.debug(f"Fetched tokens: {tokens}")
        return tokens
    except Exception as e:
        logger.error(f"Failed to fetch tokens: {e}")
        return {}

def run_strategy():
    if not is_market_hours():
        logger.info("Outside market hours")
        return

    tokens = get_nifty_atm_option_tokens()
    if not tokens:
        logger.warning("No tokens found")
        return

    for symbol, token in tokens.items():
        try:
            quote = kite.ltp(token)
            ltp = quote[str(token)]['last_price']
            logger.debug(f"{symbol} LTP: {ltp}")

            stoploss = ltp - 20
            takeprofit = ltp + 40
            trailing_sl = ltp - 15

            logger.info(f"Strategy for {symbol}: LTP {ltp}, SL {stoploss}, TP {takeprofit}, TSL {trailing_sl}")

            # Add decision logic debug
            if ltp > stoploss + 10:
                logger.info(f"Entry condition met for {symbol}: placing order or sending alert")
            else:
                logger.debug(f"Entry condition NOT met for {symbol}")
        except Exception as e:
            logger.error(f"Error fetching LTP or processing {symbol}: {e}")

if __name__ == "__main__":
    scheduler = BlockingScheduler(timezone="Asia/Kolkata")
    scheduler.add_job(run_strategy, 'interval', minutes=1)
    logger.info("🚀 Debug Mode: Nifty Options Bot Started")
    scheduler.start()

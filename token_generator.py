import os
from kiteconnect import KiteConnect
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_access_token():
    # Load environment variables
    load_dotenv()
    
    API_KEY = os.getenv("ZERODHA_API_KEY")
    API_SECRET = os.getenv("ZERODHA_API_SECRET")
    REQUEST_TOKEN = os.getenv("ZERODHA_REQUEST_TOKEN")  # This will be manually updated
    
    if not all([API_KEY, API_SECRET, REQUEST_TOKEN]):
        logger.error("Missing required environment variables")
        return False
    
    try:
        # Initialize KiteConnect
        kite = KiteConnect(api_key=API_KEY)
        
        # Generate session data
        data = kite.generate_session(REQUEST_TOKEN, api_secret=API_SECRET)
        access_token = data["access_token"]
        
        # Update .env file with new access token
        with open(".env", "r") as f:
            env_lines = f.readlines()
        
        with open(".env", "w") as f:
            for line in env_lines:
                if line.startswith("ZERODHA_ACCESS_TOKEN="):
                    f.write(f"ZERODHA_ACCESS_TOKEN={access_token}\n")
                else:
                    f.write(line)
        
        logger.info("Successfully generated and updated access token")
        return True
    
    except Exception as e:
        logger.error(f"Error generating access token: {str(e)}")
        return False

if __name__ == "__main__":
    generate_access_token()

# communication bridge
# fetches API credentials and intializes an authenticated session with Binance

import os
import logging
from binance.client import Client
from dotenv import load_dotenv

# Set up a local logger instance for this specific module
logger = logging.getLogger(__name__)

def get_binance_client():
    """
    Loads secret environment variables and returns an initialized 
    Binance Client configured explicitly for the Futures Testnet environment.
    """

    load_dotenv()
    
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        logger.error("API credentials missing. Please check your .env file.")
        raise ValueError("Missing BINANCE_API_KEY or BINANCE_API_SECRET in the environment.")
        
    try:
        # instantiate the client and force the Testnet flag to True
        # This automatically reroutes endpoints to https://testnet.binancefuture.com
        client = Client(api_key, api_secret, testnet=True)
        
        logger.info("Binance Client successfully initialized for Futures Testnet.")
        return client
        
    except Exception as e:
        logger.error(f"Failed to initialize Binance Client: {str(e)}")
        raise e
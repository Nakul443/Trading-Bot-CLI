# the core business logic responsible for executing trades
# takes the cleaned, validated inputs from the CLI layer,
# requests an authenticated connection from client.py,
# and maps the arguments into the official Binance Futures API format
# wraps the network request in an error-handling boundary
# to catch issues (like insufficient margin or incorrect symbol format)
# and then writes receipts directly to bot.log

import logging
from binance.exceptions import BinanceAPIException
from bot.client import get_binance_client

logger = logging.getLogger(__name__)

def place_futures_order(symbol: str, side: str, order_type: str, quantity: float, price: float = None) -> dict:
    """
    Communicates with the Binance Futures Testnet to create an order.
    Handles network errors and logs API payloads safely.
    """
    # fetch the active network bridge connection
    try:
        client = get_binance_client()
    except Exception as e:
        logger.error(f"Order aborted: Could not connect to API client. Detail: {str(e)}")
        raise e

    # build the exact keyword arguments structure expected by python-binance
    order_args = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": quantity
    }

    # add the price explicitly if it is a LIMIT order
    if order_type == "LIMIT":
        order_args["price"] = str(price)
        order_args["timeInForce"] = "GTC"  # Good 'Til Cancelled (Mandatory for standard limit orders)

    # log the outbound request snapshot to the audit file BEFORE hitting the server
    logger.info(f"Sending Order Request to Binance -> Params: {order_args}")

    # transmit data over the web and catch errors defensively
    try:
        # call the actual Binance Futures endpoint: /fapi/v1/order
        response = client.futures_create_order(**order_args)
        
        # log the full inbound data payload receipt to the file
        logger.info(f"Order Executed Successfully! Server Response: {response}")
        return response

    except BinanceAPIException as api_err:
        # errors specific to Binance rules (e.g., Code -2019: Insufficient Margin)
        logger.error(f"Binance API rejected transaction: {api_err.status_code} - {api_err.message}")
        raise api_err
        
    except Exception as net_err:
        # unexpected connection errors (e.g., local Wi-Fi drops)
        logger.error(f"Network / Connectivity failure occurred: {str(net_err)}")
        raise net_err
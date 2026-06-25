# application's local firewall
# intercepts whatever user types into the command line
# and cross checks the values against strict trading rules before the bot contacts Binance
# give commands according to rules basically,
# the bot will not even attempt to send a request to Binance if the user input is invalid

import logging

logger = logging.getLogger(__name__)

def validate_order_inputs(symbol: str, side: str, order_type: str, quantity: float, price: float = None) -> dict:
    """
    Validates CLI inputs against exchange business rules before hitting the API.
    Returns a cleaned dictionary of inputs if valid, or raises ValueError.
    """
    # clean up string spacing and casing inputs automatically
    clean_symbol = symbol.strip().upper()
    clean_side = side.strip().upper()
    clean_type = order_type.strip().upper()

    # validate Symbol (Basic check: Binance futures pairs must not be blank)
    if not clean_symbol:
        logger.error("Validation Failed: Symbol cannot be empty.")
        raise ValueError("Trading symbol cannot be empty.")

    # validate Side (Must be BUY or SELL)
    if clean_side not in ["BUY", "SELL"]:
        logger.error(f"Validation Failed: Invalid side '{clean_side}'.")
        raise ValueError("Order side must be strictly 'BUY' or 'SELL'.")

    # validate Order Type (Must be MARKET or LIMIT)
    if clean_type not in ["MARKET", "LIMIT"]:
        logger.error(f"Validation Failed: Invalid order type '{clean_type}'.")
        raise ValueError("Order type must be strictly 'MARKET' or 'LIMIT'.")

    # validate Quantity (Must be greater than zero)
    if quantity <= 0:
        logger.error(f"Validation Failed: Quantity {quantity} is less than or equal to 0.")
        raise ValueError("Quantity must be a positive number greater than zero.")

    # validate Price for LIMIT orders (Price is mandatory and must be positive)
    if clean_type == "LIMIT":
        if price is None:
            logger.error("Validation Failed: LIMIT order requested but no price provided.")
            raise ValueError("A price parameter is strictly required for 'LIMIT' orders.")
        if price <= 0:
            logger.error(f"Validation Failed: LIMIT order price {price} is less than or equal to 0.")
            raise ValueError("Limit price must be a positive number greater than zero.")

    return {
        "symbol": clean_symbol,
        "side": clean_side,
        "order_type": clean_type,
        "quantity": quantity,
        "price": price
    }
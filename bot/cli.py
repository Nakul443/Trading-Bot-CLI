# CLI
# captures parameters directly from the terminal
# logging engine -> captures terminal flags
# -> validators -> oders to execute transaction -> prints clean msg

import click
import logging
from bot.logging_config import setup_logging
from bot.validators import validate_order_inputs
from bot.orders import place_futures_order

# initialize the logging engine immediately upon file read
setup_logging()
logger = logging.getLogger(__name__)

# define the main Click command group/interface
@click.command()
@click.option('--symbol', '-s', required=True, type=str, help="The trading pair, e.g., BTCUSDT")
@click.option('--side', '-d', required=True, type=click.Choice(['BUY', 'SELL', 'buy', 'sell']), help="Order direction")
@click.option('--order-type', '-t', required=True, type=click.Choice(['MARKET', 'LIMIT', 'market', 'limit']), help="Execution type")
@click.option('--quantity', '-q', required=True, type=float, help="Amount of asset to trade")
@click.option('--price', '-p', required=False, type=float, default=None, help="Trigger price (Mandatory for LIMIT orders)")
def main(symbol, side, order_type, quantity, price):
    """
    Simplified CLI Trading Bot for Binance Futures Testnet.
    """
    # print the Order Request Summary to the user screen immediately
    click.echo("\n========================================")
    click.echo("       📦 ORDER REQUEST SUMMARY        ")
    click.echo("========================================")
    click.echo(f"🔹 Symbol:     {symbol.upper()}")
    click.echo(f"🔹 Side:       {side.upper()}")
    click.echo(f"🔹 Type:       {order_type.upper()}")
    click.echo(f"🔹 Quantity:   {quantity}")
    if price:
        click.echo(f"🔹 Price:      ${price}")
    click.echo("========================================\n")

    # filter data through our local validation engine
    try:
        clean_inputs = validate_order_inputs(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price
        )
    except ValueError as val_err:
        click.secho(f" Input Validation Error: {str(val_err)}", fg="red", bold=True)
        return

    click.echo(" Transmitting trade request to Binance Futures Testnet...")
    
    try:
        response = place_futures_order(
            symbol=clean_inputs["symbol"],
            side=clean_inputs["side"],
            order_type=clean_inputs["order_type"],
            quantity=clean_inputs["quantity"],
            price=clean_inputs["price"]
        )

        # extract target evaluation keys and display success payload to user
        click.secho("\n ORDER EXECUTED SUCCESSFULLY!", fg="green", bold=True)
        click.echo("----------------------------------------")
        click.echo(f" Order ID:      {response.get('orderId')}")
        click.echo(f" Status:        {response.get('status')}")
        click.echo(f" Executed Qty:  {response.get('executedQty')}")
        click.echo(f" Order Type:   {response.get('type')}")
        click.echo("----------------------------------------\n")

    except Exception as err:
        click.secho("\n ORDER EXECUTION FAILED!", fg="red", bold=True)
        click.secho(f"Reason: {str(err)}", fg="yellow")
        click.echo("Check 'bot.log' for deep network diagnostic logs.\n")

if __name__ == '__main__':
    main()
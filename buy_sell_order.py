from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException


def create_limit_order(client, symbol, side, quantity, price):
    try:
        order = client.create_order(
            symbol=symbol,
            side=side,
            type='LIMIT',
            timeInForce='GTC',
            quantity=round(quantity,4),
            price=round(price,4))
        return order
    except BinanceAPIException as e:
        # error handling goes here
        print(e)
        return None
    except BinanceOrderException as e:
        # error handling goes here
        print(e)
        return None

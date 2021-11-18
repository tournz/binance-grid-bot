import os
from binance.client import Client

# Initialize the client
api_key = os.environ['BINANCE_API']
api_secret = os.environ['BINANCE_SECRET']
client = Client(api_key, api_secret)

base_currency = input('Base currency:')
quote_currency = input('Quote currency: ')
pair = base_currency + quote_currency
open_orders = client.get_open_orders(symbol=pair)
for order in open_orders:
    client.cancel_order(symbol=pair, orderId=order['orderId'])

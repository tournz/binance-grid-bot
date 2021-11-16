import os, time, datetime, pandas as pd
from binance.client import Client

# init
api_key = os.environ['BINANCE_API']
api_secret = os.environ['BINANCE_SECRET']
client = Client(api_key, api_secret)
current_timestamp = 1000*time.time()
current_timestamp_minus_1_minute = current_timestamp - 6000000

# check what orders are standing
# PUT ALL TRADING PAIRS IN 1 SINGLE ARRAY AND LOOP OVER IT
orders = client.get_all_orders(symbol='ETHTRY')
# list the ones which were executed
newly_filled_orders = []
for order in orders:
  if order['status'] == 'FILLED':
    if order['updateTime'] > current_timestamp_minus_1_minute:
        newly_filled_orders.append(order)

print(newly_filled_orders)
for order in newly_filled_orders:
# print(datetime.datetime.fromtimestamp(order['updateTime']/1000))
'''What if we crossed the line while going upwards:
    That means we completed a SELL order
    And we need to place a BUY order at 1 interval lower than order['price']'''
    # if client.get_symbol_ticker(symbol=pair)['price'] > order['price']:
'''What if we crossed the line while going downwards:
    That means we completed a BUY order
    And we need to place a SELL order at 1 interval higher than order['price']'''
    # else:

# HOW DO WE FIND THE INTERVAL THAT WE NEED TO PLACE THE NEW ORDER ?? ANALYZE THE EXISTING GRID ?

import os, time, datetime, pickle, pandas as pd
from binance.client import Client
from buy_sell_order import create_limit_order
from grid_bot import Gridbot

# Initialize the client
api_key = os.environ['BINANCE_API']
api_secret = os.environ['BINANCE_SECRET']
client = Client(api_key, api_secret)

# Settings
current_timestamp = 1000*time.time()
current_timestamp_minus_1_minute = current_timestamp - 60000

# Retrieve the bot associated with the currency pair
base_currency = input('Base currency: ')
quote_currency = input('Quote currency: ')
pair = base_currency + quote_currency
BOT_STORAGE = f'/Users/zacharietournant/Desktop/Coding/Binance Bot/{pair}_gridbot.dat'
with open(BOT_STORAGE,'rb') as f:
    gridbot = pickle.load(f)

# Put the newly executed orders in a list
all_orders = client.get_all_orders(symbol=gridbot.pair)
newly_filled_orders = [order for order in all_orders if order['status']=='FILLED' and order['updateTime'] > current_timestamp_minus_1_minute]
newly_filled_orders = sorted(newly_filled_orders, key=lambda d: d['updateTime'])

# Inform the user of the newly filled orders and replace them
print(f'There are {len(newly_filled_orders)} newly filled orders:')
for order in newly_filled_orders:
    print(f"{order['side']} at {order['price']} at {order['updateTime']}")
    gridbot.replace_order(client, order)

# Show the user the new grid
gridbot.detect_grid(client)
print('Your order grid is now the following:')
for sell in gridbot.sell_prices:
    print(f'SELL AT ----- {sell}')
print('CURRENT PRICE '+ client.get_symbol_ticker(symbol=gridbot.pair)['price'])
for buy in gridbot.buy_prices:
    print(f'BUY AT ------ {buy}')


'''exchange_info = client.get_exchange_info()
for pair_dic in exchange_info['symbols']:
    pair = pair_dic['symbol']
    print(pair)'''

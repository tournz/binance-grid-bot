import os, time, datetime, pickle, pandas as pd
from binance.client import Client
from buy_sell_order import create_limit_order
from grid_bot import Gridbot

BOT_STORAGE = '/Users/zacharietournant/Desktop/Coding/Binance Bot/gridbot.dat'

# Initialize the client
api_key = os.environ['BINANCE_API']
api_secret = os.environ['BINANCE_SECRET']
client = Client(api_key, api_secret)

# Settings
current_timestamp = 1000*time.time()
current_timestamp_minus_1_minute = current_timestamp - 60000

with open(BOT_STORAGE,'rb') as f:
    gridbot = pickle.load(f)

print(f'{gridbot.pair}')

all_orders = client.get_all_orders(symbol=gridbot.pair)

# Put the newly executed orders in a list
newly_filled_orders = [order for order in all_orders if order['status']=='FILLED' and order['updateTime'] > current_timestamp_minus_1_minute]
print(f'There are {len(newly_filled_orders)} newly filled orders')
print('---------------------------------------------------------------------------------------')

for order in newly_filled_orders:
    gridbot.detect_grid(client)
    print(f'In this grid, there are {len(gridbot.grid_buy_orders)} buy orders and {len(gridbot.grid_sell_orders)} sell orders remaining')
    print(f"Buying at:    {gridbot.buy_prices}   ------- {order['side']} at {order['price']} -------   {gridbot.sell_prices}    :Selling at")
    gridbot.replace_order(client, order)
    print('Your new order grid is the following:')
    print(f"Buying at:    {gridbot.buy_prices}   ------- {client.get_symbol_ticker(symbol=gridbot.pair)['price']} -------   {gridbot.sell_prices}    :Selling at")
    print('---------------------------------------------------------------------------------------')






'''exchange_info = client.get_exchange_info()
for pair_dic in exchange_info['symbols']:
    pair = pair_dic['symbol']
    print(pair)'''

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
#base_currency = input('Base currency: ')
#quote_currency = input('Quote currency: ')
#pair = base_currency + quote_currency
pair = 'ETHTRY'
BOT_STORAGE = f'/root/code/binance_bot/gridbots/{pair}_gridbot.dat'
with open(BOT_STORAGE,'rb') as f:
    gridbot = pickle.load(f)

# Put the newly executed orders in a list
all_orders = client.get_all_orders(symbol=gridbot.pair)
newly_filled_orders = [order for order in all_orders if order['status']=='FILLED' and order['updateTime'] > current_timestamp_minus_1_minute]
newly_filled_orders = sorted(newly_filled_orders, key=lambda d: d['updateTime'])

# Replace the newly executed orders
for order in newly_filled_orders:
    gridbot.replace_order(client, order)

# Log the operations into the log file
gridbot.detect_grid(client)

logfile = open('/root/code/binance_bot/logs.txt', 'a')
logfile.write('--------------------------------------\nAccessed on ' + str(datetime.datetime.now()) +'\n')
logfile.write(f'{len(newly_filled_orders)} orders were filled:\n')
for order in newly_filled_orders:
    logfile.write(f"{order['side']} at {order['price']} was executed at {datetime.datetime.fromtimestamp(int(order['updateTime']/1000))}\n")
logfile.write('\nThe order grid is now as follows:\n')
for sell in gridbot.sell_prices:
    logfile.write(f'SELL AT ----- {sell}\n')
logfile.write('CURRENT PRICE '+ client.get_symbol_ticker(symbol=gridbot.pair)['price'] +'\n')
for buy in gridbot.buy_prices:
    logfile.write(f'BUY AT ------ {buy}\n')
logfile.close()

'''exchange_info = client.get_exchange_info()
for pair_dic in exchange_info['symbols']:
    pair = pair_dic['symbol']
    print(pair)'''

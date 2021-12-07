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

# Loop over the currency pairs
# exchange_info = client.get_exchange_info()
# for pair_dic in exchange_info['symbols']:
for pair_dic in ['ETHTRY']:
    # pair = pair_dic['symbol']
    pair = pair_dic # to take out once I really loop

    # Get the active gridbots for the pair
    FOLDER_PATH = f'/root/code/binance_bot/gridbots/{pair}'
    active_gridbots_files = [bot_file for bot_file in os.listdir(FOLDER_PATH) if bot_file[:6]=='ACTIVE' and bot_file[-11:-4]=='gridbot']

    # Put the newly executed orders in a list
    all_pair_orders = client.get_all_orders(symbol=pair)
    newly_filled_pair_orders = [order for order in all_pair_orders if order['status']=='FILLED' and order['updateTime'] > current_timestamp_minus_1_minute]
    newly_filled_pair_orders = sorted(newly_filled_pair_orders, key=lambda d: d['updateTime'])

    # Loop over the active gridbots
    for gridbot_file in active_gridbots_files:
        BOT_FILE_PATH = FOLDER_PATH + '/' + gridbot_file
        with open(BOT_FILE_PATH, 'rb') as f:
            gridbot = pickle.load(f)
        grid_orders_ids = [order['orderId'] for order in gridbot.grid_orders]
        gridbot_executed_orders = [order for order in newly_filled_pair_orders if order['orderId'] in grid_orders_ids]
        # Replace the newly executed orders related to the gridbot
        for order in gridbot_executed_orders:
            gridbot.replace_order(client, order)

        # Log the operations into the log file
        gridbot.detect_binance_grid(client)
        current_price = client.get_symbol_ticker(symbol=gridbot.pair)['price']
        logfile = open(FOLDER_PATH + '/' + gridbot_file[:-11] + 'logs.txt', 'a')
        logfile.write('--------------------------------------\nAccessed on ' + str(datetime.datetime.now()) +'\n')
        logfile.write(f'{len(gridbot_executed_orders)} orders were filled:\n')
        for order in gridbot_executed_orders:
            logfile.write(f"{order['side']} at {order['price']} was executed at {datetime.datetime.fromtimestamp(int(order['updateTime']/1000))}\n")
        logfile.write('\nThe order grid is now as follows:\n')
        for sell in gridbot.binance_sell_prices:
            logfile.write(f'SELL AT ----- {sell}\n')
        logfile.write('CURRENT PRICE '+ current_price +'\n')
        for buy in gridbot.binance_buy_prices:
            logfile.write(f'BUY AT ------ {buy}\n')
        logfile.close()

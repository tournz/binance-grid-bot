import os, time, datetime, pickle, pandas as pd
from binance.client import Client
from buy_sell_order import create_limit_order
from grid_bot import Gridbot
from functions import initialize_client

# Write down program start time and set end time
t_start = time.time()
t_end = t_start + 60

# Initialize the client
client = initialize_client()

# Loop over the currency pairs
# exchange_info = client.get_exchange_info()

filled_orders_dic = {}
loop_times_pairs = {}
loop_times_all = [datetime.datetime.now()]

# for pair_dic in exchange_info['symbols']:
for pair_dic in ['ETHTRY']:
    # pair = pair_dic['symbol']
    pair = pair_dic # to take out once I really loop
    loop_times_pairs[pair] = [datetime.datetime.now()]
    filled_orders_dic[pair] = []

while time.time() < t_end:
    loop_times_all.append(time.time())
    print(f'Was added to the loop_times_all list: {loop_times_all}')
    # for pair_dic in exchange_info['symbols']:
    for pair_dic in ['ETHTRY']:
        # pair = pair_dic['symbol']
        pair = pair_dic # to take out once I really loop

        # Get the active gridbots for the pair
        FOLDER_PATH = f'/root/code/binance_bot/gridbots/{pair}'
        active_gridbots_files = [bot_file for bot_file in os.listdir(FOLDER_PATH) if bot_file[:6]=='ACTIVE' and bot_file[-11:-4]=='gridbot']

        # Put the newly executed orders in a list
        all_pair_orders = client.get_all_orders(symbol=pair)
        loop_times_pairs[pair].append(time.time())
        pair_filled_orders_id = [order['orderId'] for order in filled_orders_dic[pair]]
        newly_filled_pair_orders = [order for order in all_pair_orders if order['status']=='FILLED' and order['orderId'] not in pair_filled_orders_id and order['updateTime'] > 1000*t_start]
        newly_filled_pair_orders = sorted(newly_filled_pair_orders, key=lambda d: d['updateTime'])
        filled_orders_dic[pair].append(newly_filled_pair_orders)

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
            logfile = open(FOLDER_PATH + '/' + gridbot_file[:-11] + 'logs.txt', 'a')
            logfile.write('--------------------------------------\nAccessed on ' + str(datetime.datetime.now()) +'\n')
            logfile.write(f'{len(gridbot_executed_orders)} orders were filled:\n')
            for order in gridbot_executed_orders:
                logfile.write(f"{order['side']} at {order['price']} was executed at {datetime.datetime.fromtimestamp(int(order['updateTime']/1000))}\n")
            logfile.write('\nThe order grid is now as follows:\n')

            # Update with the latest Binance grid data
            gridbot.detect_binance_grid(client)
            current_price = client.get_symbol_ticker(symbol=gridbot.pair)['price']

            # Finish writing in the log file with the current order grid
            for sell in gridbot.binance_sell_prices:
                logfile.write(f'SELL AT ----- {sell}\n')
            logfile.write('CURRENT PRICE '+ current_price +'\n')
            for buy in gridbot.binance_buy_prices:
                logfile.write(f'BUY AT ------ {buy}\n')
            logfile.close()

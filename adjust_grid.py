import os, time, datetime, pandas as pd
from binance.client import Client
from buy_sell_order import create_limit_order

# Initialize the client
api_key = os.environ['BINANCE_API']
api_secret = os.environ['BINANCE_SECRET']
client = Client(api_key, api_secret)

# Set the timestamps
current_timestamp = 1000*time.time()
current_timestamp_minus_1_minute = current_timestamp - 7200000

all_orders = client.get_all_orders(symbol='ETHTRY')

# Put the newly executed orders in a list
newly_filled_orders = [order for order in all_orders if order['status']=='FILLED' and order['updateTime'] > current_timestamp_minus_1_minute]
print(f'There are {len(newly_filled_orders)} newly filled orders')
print('---------------------------------------------------------------------------------------')

for order in newly_filled_orders:
    # We want to figure out the grid's interval
    # Identify the other orders of the grid and place them in a list
    all_standing_orders = client.get_open_orders(symbol=order['symbol'])
    grid_orders = [one_order for one_order in all_standing_orders if str(one_order['time'])[:7] == str(order['time'])[:7]]
    grid_buy_orders = [one_order for one_order in grid_orders if one_order['side'] == 'BUY']
    grid_sell_orders = [one_order for one_order in grid_orders if one_order['side'] == 'SELL']
    buy_prices = sorted([float(buy_order['price']) for buy_order in grid_buy_orders])
    sell_prices = sorted([float(sell_order['price']) for sell_order in grid_sell_orders])

    print(f'In this grid, there are {len(grid_buy_orders)} buy orders and {len(grid_sell_orders)} sell orders remaining')
    print(f"Buying at:    {buy_prices}   ------- {order['side']} at {order['price']} -------   {sell_prices}    :Selling at")

    # Once the list is constituted, we analyze the intervals among the BUY and SELL orders
    if len(buy_prices) > 1:
        print('The interval is set using the buy prices')
        interval = buy_prices[1] - buy_prices[0]
        for i in range(len(buy_prices) - 1):
            if buy_prices[i+1] - buy_prices[i] != interval:
                print('There is irregularity in the interval setting')
    elif len(sell_prices) > 1:
        print('The interval is set using the sell prices')
        interval = sell_prices[1] - sell_prices[0]
        for i in range(len(sell_prices) - 1):
            if sell_prices[i+1] - sell_prices[i] != interval:
                print('There is irregularity in the interval setting')
    else:
        print('There is no grid so to speak')

    quantity = grid_orders[0]['origQty']
    print(f'Quantity: {quantity}')
    print(f'Interval: {interval}')

    # print(datetime.datetime.fromtimestamp(order['updateTime']/1000))
    if order['side'] == 'SELL':
        # create_limit_order(client, order['pair'], 'BUY', quantity, order['price'] - interval)
        print(f"create_limit_order(client, order['pair'], 'BUY', {quantity}, {float(order['price']) - interval})")
    elif order['side'] == 'BUY':
        # create_limit_order(client, order['pair'], 'SELL', quantity, order['price'] + interval)
        print(f"create_limit_order(client, order['pair'], 'SELL', {quantity}, {float(order['price']) + interval})")

    print('---------------------------------------------------------------------------------------')

# HOW DO WE FIND THE INTERVAL THAT WE NEED TO PLACE THE NEW ORDER ?? ANALYZE THE EXISTING GRID ?

'''exchange_info = client.get_exchange_info()
for pair_dic in exchange_info['symbols']:
    pair = pair_dic['symbol']
    print(pair)'''

import os, time, pandas as pd
from binance.client import Client
from websocket import run_price_websocket
from buy_sell_order import create_limit_order
from get_latest_data import get_all_trade_data
from grid_bot import Gridbot

# init
api_key = os.environ['BINANCE_API']
api_secret = os.environ['BINANCE_SECRET']
client = Client(api_key, api_secret)

print(f"Free ETH balance:{client.get_asset_balance(asset='ETH')['free']} ETH")
print(f"Free TRY balance: {client.get_asset_balance(asset='TRY')['free']} TRY")

gridbot = Gridbot(client, 'ETHTRY', 120, 30500, 40500, 8)
if hasattr(gridbot, 'sufficient_balance'):
    gridbot.create_order_grid(client)
else:
    print('Try and rebalance your account to be able to launch the bot')

'''print('Your order has been sent:')
print(order)

if order != None:
    if order['fills'] == []:
        print('Your order is pending execution')
    else:
        print('Your order has been filled')

    # cancel previous orders
    cancel = client.cancel_order(symbol='ETHTRY', orderId=order['orderId'])
    print('Your order has been cancelled')
    print(cancel)

df = get_all_trade_data(client, 'ETHTRY', '12h')
print(df.head)'''

'''info = client.get_symbol_info('ETHTRY')
print(info)

# get balances for all assets & some account information
print(client.get_account())

# get balance for a specific asset only (BTC)
print(client.get_asset_balance(asset='ETH'))

# get latest price from Binance API
eth_try_price = client.get_symbol_ticker(symbol="ETHTRY")
# print full output (dictionary)
print(eth_try_price)
print(eth_try_price['price'])


run_price_websocket('ETHTRY', 15)'''

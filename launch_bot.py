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

base_currency = input('Choose your base currency: ')
quote_currency = input('Choose your quote currency: ')
pair = base_currency + quote_currency
initial_pair_price = client.get_symbol_ticker(symbol=pair)['price']
print(f"The current price of the pair is {client.get_symbol_ticker(symbol=pair)['price']}")
print(f"Free {base_currency} balance:{client.get_asset_balance(asset=base_currency)['free']} {base_currency} equalling {float(client.get_asset_balance(asset=base_currency)['free']) * float(initial_pair_price)} {quote_currency}")
print(f"Free {quote_currency} balance: {client.get_asset_balance(asset=quote_currency)['free']} {quote_currency}")
max_quote_currency_amount = min(float(client.get_asset_balance(asset=base_currency)['free']) * float(initial_pair_price), float(client.get_asset_balance(asset=quote_currency)['free']))
total_amount_quote_currency = input(f'Amount of quote currency you want to invest on each side (max amount: {max_quote_currency_amount} {quote_currency}): ')
lower_boundary = input('Lower end of the range: ')
upper_boundary = input('Upper end of the range: ')
grid_number = input('Number of lines in the grid: ')

gridbot = Gridbot(client, pair, total_amount_quote_currency, lower_boundary, upper_boundary, grid_number)
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

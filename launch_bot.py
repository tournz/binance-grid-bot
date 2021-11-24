import os, time, datetime, pickle, pandas as pd
from binance.client import Client
from websocket import run_price_websocket
from buy_sell_order import create_limit_order
from get_latest_data import get_all_trade_data
from grid_bot import Gridbot
from crontab import CronTab

# init
api_key = os.environ['BINANCE_API']
api_secret = os.environ['BINANCE_SECRET']
client = Client(api_key, api_secret)

# Choose the currency
base_currency = input('Choose your base currency: ')
quote_currency = input('Choose your quote currency: ')
pair = base_currency + quote_currency

# Get the price and balance info from the client
pair_price = float(client.get_symbol_ticker(symbol=pair)['price'])
base_currency_balance = float(client.get_asset_balance(asset=base_currency)['free'])
base_currency_balance_in_quote_amount = float(client.get_asset_balance(asset=base_currency)['free']) * float(pair_price)
quote_currency_balance = float(client.get_asset_balance(asset=quote_currency)['free'])
max_quote_currency_amount = min(base_currency_balance_in_quote_amount,quote_currency_balance)

# Inform the user
print(f"The current price of the pair is {pair_price}")
print(f"Free {base_currency} balance:{base_currency_balance} {base_currency} equalling {base_currency_balance_in_quote_amount} {quote_currency}")
print(f"Free {quote_currency} balance: {quote_currency_balance} {quote_currency}")

# Give the user the option to rebalance the pair before launching the bot
if base_currency_balance_in_quote_amount < 0.95 * quote_currency_balance or base_currency_balance_in_quote_amount > 1.05 * quote_currency_balance:
    equalizing_order = input('Do you want to pass an order to equalize the amounts? (Y/N)')
    if equalizing_order == 'Y':
        quantity = round((abs(quote_currency_balance - base_currency_balance_in_quote_amount)/2)/pair_price, 4)
        if base_currency_balance_in_quote_amount < quote_currency_balance:
            client.order_market_buy(symbol=pair, quantity=quantity)
        elif base_currency_balance_in_quote_amount > quote_currency_balance:
            client.order_market_sell(symbol=pair, quantity=quantity)
        time.sleep(1)

        # Get the updated price and balance info from the client
        pair_price = float(client.get_symbol_ticker(symbol=pair)['price'])
        base_currency_balance = float(client.get_asset_balance(asset=base_currency)['free'])
        base_currency_balance_in_quote_amount = float(client.get_asset_balance(asset=base_currency)['free']) * float(pair_price)
        quote_currency_balance = float(client.get_asset_balance(asset=quote_currency)['free'])
        max_quote_currency_amount = min(base_currency_balance_in_quote_amount,quote_currency_balance)

        # Re-inform the user
        print(f"The current price of the pair is {pair_price}")
        print(f"Free {base_currency} balance:{base_currency_balance} {base_currency} equalling {base_currency_balance_in_quote_amount} {quote_currency}")
        print(f"Free {quote_currency} balance: {quote_currency_balance} {quote_currency}")

# Set up the bot
total_amount_quote_currency = input(f'Amount of quote currency you want to invest on each side (max amount: {max_quote_currency_amount} {quote_currency}): ')
lower_boundary = input('Lower end of the range: ')
upper_boundary = input('Upper end of the range: ')
grid_number = input('Number of lines in the grid: ')

# Create the bot object
gridbot = Gridbot(client, pair, total_amount_quote_currency, lower_boundary, upper_boundary, grid_number)
if hasattr(gridbot, 'sufficient_balance'):
    gridbot.create_order_grid(client)
    # Store the gridbot object
    os.makedirs(f'/root/code/binance_bot/gridbots/{pair}', exist_ok=True)
    start_timestamp = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    BOT_STORAGE = f"/root/code/binance_bot/gridbots/{pair}/ACTIVE [{gridbot.range_start}, {gridbot.range_end}] step {gridbot.base_interval} amount_per_order {gridbot.amount_per_order_base_currency} Start:{start_timestamp} gridbot.dat"
    f= open(BOT_STORAGE, 'wb')
    pickle.dump(gridbot, f)
    f.close()
    # Create a log file
    LOG_STORAGE = f"/root/code/binance_bot/gridbots/{pair}/ACTIVE [{gridbot.range_start}, {gridbot.range_end}] step {gridbot.base_interval} amount_per_order {gridbot.amount_per_order_base_currency} Start:{start_timestamp} logs.txt"
    f=open(LOG_STORAGE, 'w')
    f.close()

    # Instruct the adjust_grid cron job to be executed every minute
    cron = CronTab(user='root')
    job = cron.new(command='python3 /root/code/binance_bot/adjust_grid.py', comment=f'{pair}')
    job.minute.every(1)
    cron.write()
    print('The cron job has been launched')

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

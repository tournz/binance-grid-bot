import os, pickle
from binance.client import Client
from grid_bot import Gridbot

# Initialize the client
api_key = os.environ['BINANCE_API']
api_secret = os.environ['BINANCE_SECRET']
client = Client(api_key, api_secret)

# Retrieve the bot associated with the currency pair
base_currency = input('Base currency: ')
quote_currency = input('Quote currency: ')
pair = base_currency + quote_currency
BOT_STORAGE = f'/Users/zacharietournant/Desktop/Coding/Binance Bot/{pair}_gridbot.dat'
with open(BOT_STORAGE,'rb') as f:
    gridbot = pickle.load(f)

# Show the user the new grid
gridbot.detect_grid(client)
print('Your order grid is now the following:')
for sell in gridbot.sell_prices:
    print(f'SELL AT ----- {sell}')
print('CURRENT PRICE '+ client.get_symbol_ticker(symbol=gridbot.pair)['price'])
for buy in gridbot.buy_prices:
    print(f'BUY AT ------ {buy}')

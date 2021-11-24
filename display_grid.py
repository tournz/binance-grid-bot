import os, pickle, inquirer, re
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
active_gridbots = [bot_file for bot_file in os.listdir(f'/root/code/binance_bot/gridbots/{pair}') if bot_file[:6]=='ACTIVE' and bot_file[-11:-4]=='gridbot']
questions = [inquirer.List('bot', message = 'Which bot do you want to check?', choices = active_gridbots)]
answers = inquirer.prompt(questions)
BOT_STORAGE = f"/root/code/binance_bot/gridbots/{pair}/{answers['bot']}"
lower_boundary = re.findall('\[(\d+.?\d*),', answers['bot'])[0]
upper_boundary = re.findall(', (\d+.?\d*)\]', answers['bot'])[0]
print(lower_boundary)
print(upper_boundary)
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

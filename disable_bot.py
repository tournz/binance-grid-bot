import os, pickle
from binance.client import Client
from crontab import CronTab

# Initialize the client
api_key = os.environ['BINANCE_API']
api_secret = os.environ['BINANCE_SECRET']
client = Client(api_key, api_secret)

# Ask for the currency pair
base_currency = input('Base currency: ')
quote_currency = input('Quote currency: ')
pair = base_currency + quote_currency

# List all active gridbots for the pair
active_gridbots = [bot_file for bot_file in os.listdir(f'/root/code/binance_bot/gridbots/{pair}') if bot_file[:6]=='ACTIVE' and bot_file[-11:-4]=='gridbot']
questions = [inquirer.List('bot', message = 'Which bot do you want to disable?', choices = active_gridbots)]
answers = inquirer.prompt(questions)
BOT_STORAGE = f"/root/code/binance_bot/gridbots/{pair}/{answers['bot']}"
with open(BOT_STORAGE,'rb') as f:
    gridbot = pickle.load(f)

# See what orders are related to the bot and cancel them
gridbot.detect_grid(client)
open_orders = client.get_open_orders(symbol=pair)
for order in open_orders:
    if (order in self.buy_orders or self.sell_orders):
        client.cancel_order(symbol=pair, orderId=order['orderId'])
os.remove(BOT_STORAGE)

cron = CronTab(user='root')
job = cron.find_comment(pair)
cron.remove(job)
cron.write()

print(f'All orders for the {pair} pair have been cancelled')
print('The bot was disabled')

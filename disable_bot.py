import os, pickle, inquirer
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
FOLDER_PATH = f"/root/code/binance_bot/gridbots/{pair}/"
BOT_FILE = answers['bot']
BOT_FILE_PATH = FOLDER_PATH + BOT_FILE
LOG_FILE = BOT_FILE[:-11] + 'logs.txt'
LOG_FILE_PATH = FOLDER_PATH + LOG_FILE
with open(BOT_FILE_PATH,'rb') as f:
    gridbot = pickle.load(f)

# See what orders are related to the bot and cancel them
gridbot.detect_binance_grid(client)
open_orders = client.get_open_orders(symbol=pair)
for order in open_orders:
    if order in gridbot.binance_grid_orders:
        client.cancel_order(symbol=pair, orderId=order['orderId'])
        print(f"{order['side']} at {order['price']} has been cancelled")

# Rename the files to indicate the bot was deactivated
os.rename(BOT_FILE_PATH, FOLDER_PATH + "DISABLED " + f"{BOT_FILE[7:]}")
os.rename(LOG_FILE_PATH, FOLDER_PATH + "DISABLED " + f"{LOG_FILE[7:]}")

cron = CronTab(user='root')
job = cron.find_comment(pair)
cron.remove(job)
cron.write()

print('The bot has been disabled')

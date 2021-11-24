import os, math, pandas as pd
from binance.client import Client

# init
api_key = os.environ['BINANCE_API']
api_secret = os.environ['BINANCE_SECRET']
client = Client(api_key, api_secret)

TokenDetails = client.get_exchange_info()
ETHTRY_filters = next(dict['filters'] for dict in TokenDetails['symbols'] if dict['symbol'] == 'ETHTRY')
ETHTRY_price_filter = next(dict['tickSize'] for dict in ETHTRY_filters if dict['filterType'] == 'PRICE_FILTER')
print(ETHTRY_filters)

import os, math, pandas as pd
from binance.client import Client
from functions import initialize_client

# init
client = initialize_client()

TokenDetails = client.get_exchange_info()
ETHTRY_filters = next(dict['filters'] for dict in TokenDetails['symbols'] if dict['symbol'] == 'ETHTRY')
ETHTRY_price_filter = next(dict['tickSize'] for dict in ETHTRY_filters if dict['filterType'] == 'PRICE_FILTER')
print(ETHTRY_filters)

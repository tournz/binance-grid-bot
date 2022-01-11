import os
from binance.client import Client

def initialize_client():
    api_key = os.environ['BINANCE_API']
    api_secret = os.environ['BINANCE_SECRET']
    client = Client(api_key, api_secret)
    return client

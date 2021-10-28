import time
from time import sleep
from binance import ThreadedWebsocketManager


def trade_history(msg):
    # define how to process incoming WebSocket messages
    btc_price = {'error':False}
    if msg['e'] != 'error':
        btc_price['last'] = msg['c']
        btc_price['bid'] = msg['b']
        btc_price['last'] = msg['a']
        btc_price['error'] = False
    else:
        btc_price['error'] = True


def run_price_websocket(symbol, duration):
    # init and start the WebSocket
    bsm = ThreadedWebsocketManager()
    bsm.start()

    # subscribe to a stream
    bsm.start_symbol_ticker_socket(callback=trade_history, symbol=symbol)

    time.sleep(duration)

    # stop websocket
    bsm.stop()

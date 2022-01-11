from buy_sell_order import create_limit_order
import math

class Gridbot:
    def __init__(self, client, pair, amount_quote_currency, range_start, range_end, grid_number):
        pair_price = client.get_symbol_ticker(symbol=pair)['price']
        if float(pair_price) < float(range_start) or float(range_end) < float(pair_price) or float(range_start) > float(range_end):
            return print('Check your range values')

        if float(client.get_asset_balance(asset=pair[:3])['free']) < (float(amount_quote_currency)/float(pair_price)):
            return print(f"Base currency balance insufficient, you have the equivalent of {float(client.get_asset_balance(asset=pair[:3])['free'])*float(pair_price)} {pair[3:]} in {pair[:3]} and you need {float(amount_quote_currency)} {pair[3:]}")

        elif float(client.get_asset_balance(asset=pair[3:])['free']) < float(amount_quote_currency):
            return print(f"Quote currency balance insufficient, you have {client.get_asset_balance(asset=pair[3:])['free']} {pair[3:]} and you need {float(amount_quote_currency)} {pair[3:]}")

        elif int(grid_number) <= 1:
            return print('Your grid number is too low')

        else:
            self.sufficient_balance = True
            self.pair = pair
            self.initial_pair_price = float(pair_price)
            self.amount_quote_currency = float(amount_quote_currency)
            self.range_start = float(range_start)
            self.range_end = float(range_end)
            self.grid_number = int(grid_number)
            self.base_interval = 0.0
            self.amount_per_order_base_currency = 0
            self.grid_orders = []
            self.binance_grid_orders = []
            self.binance_grid_buy_orders = []
            self.binance_grid_sell_orders = []
            self.binance_buy_prices = []
            self.binance_sell_prices = []

    def create_order_grid(self, client):
        self.initial_pair_price = float(client.get_symbol_ticker(symbol=self.pair)['price'])
        # The rounding to 0 decimals will need to be adjusted for other pairs
        self.base_interval = round((self.range_end - self.range_start)/(self.grid_number - 1),0) if self.grid_number%2 == 0 else round((self.range_end - self.range_start)/(self.grid_number),0)
        self.amount_per_order_base_currency = round((2/self.grid_number)*(self.amount_quote_currency/self.initial_pair_price),4) # The rounding to 4 decimals will need to be adjusted for other pairs as well
        # Readjust the grid's start and end
        self.range_start = self.initial_pair_price + round((math.ceil(-self.grid_number/2))*self.base_interval, 0) # Check how to round, how many decimals are needed
        self.range_end = self.initial_pair_price + round((math.ceil(self.grid_number/2))*self.base_interval, 0) # Check how to round, how many decimals are needed
        # Send the grid orders
        for i in reversed(range(math.ceil(-self.grid_number/2), math.ceil(self.grid_number/2) + 1)):
            if i < 0:
                self.grid_orders.append(create_limit_order(client, self.pair, 'BUY', self.amount_per_order_base_currency, self.initial_pair_price + round(i*self.base_interval,0))) # Check rounding too
                print(f'BUY at {self.initial_pair_price + round(i*self.base_interval,0)}')
            elif i == 0:
                print(f'PRICE---{self.initial_pair_price}')
            elif i > 0:
                self.grid_orders.append(create_limit_order(client, self.pair, 'SELL', self.amount_per_order_base_currency, self.initial_pair_price + round(i*self.base_interval,0))) # Check rounding too
                print(f'SELL at {self.initial_pair_price + round(i*self.base_interval,0)}')
        print('Your bot has been launched')

    def detect_binance_grid(self, client):
        binance_pair_orders = client.get_open_orders(symbol=self.pair)
        gridbot_orders_ids = [order['orderId'] for order in self.grid_orders]
        self.binance_grid_orders = [order for order in binance_pair_orders if order['orderId'] in gridbot_orders_ids]
        self.binance_grid_sell_orders = [order for order in self.binance_grid_orders if order['side'] == 'SELL']
        self.binance_grid_buy_orders = [order for order in self.binance_grid_orders if order['side'] == 'BUY']
        self.binance_buy_prices = sorted([float(buy_order['price']) for buy_order in self.binance_grid_buy_orders], reverse=True)
        self.binance_sell_prices = sorted([float(sell_order['price']) for sell_order in self.binance_grid_sell_orders], reverse=True)

    def replace_order(self, client, replaced_order):
        self.grid_orders = [order for order in self.grid_orders if order != replaced_order]
        if replaced_order['side'] == 'SELL':
            self.grid_orders.append(create_limit_order(client, replaced_order['symbol'], 'BUY', float(replaced_order['origQty']), float(replaced_order['price']) - self.base_interval))
            print(f"SELL at {replaced_order['price']} has been replaced by BUY at {float(replaced_order['price'] - self.base_interval)}")
        elif replaced_order['side'] == 'BUY':
            self.grid_orders.append(create_limit_order(client, replaced_order['symbol'], 'SELL', float(replaced_order['origQty']), float(replaced_order['price']) + self.base_interval))
            print(f"BUY at {replaced_order['price']} has been replaced by SELL at {float(replaced_order['price'] + self.base_interval)}")

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
            self.grid_buy_orders = []
            self.grid_sell_orders = []
            self.buy_prices = []
            self.sell_prices = []

    def create_order_grid(self, client):
        self.initial_pair_price = float(client.get_symbol_ticker(symbol=self.pair)['price'])
        # The rounding to 0 decimals will need to be adjusted for other pairs
        self.base_interval = round((self.range_end - self.range_start)/(self.grid_number - 1),0) if self.grid_number%2 == 0 else round((self.range_end - self.range_start)/(self.grid_number),0)
        # Make the base interval even to make sure half of it is still an integer
        if self.base_interval%2 != 0:
            self.base_interval += 1
        self.amount_per_order_base_currency = round((2/self.grid_number)*(self.amount_quote_currency/self.initial_pair_price), 4)  # The rounding to 4 decimals will need to be adjusted for other pairs as well
        # Readjust the grid's start and end
        self.range_start = self.initial_pair_price + round((math.ceil(-self.grid_number/2) + 0.5)*self.base_interval, 0) # Check how to round, how many decimals are needed
        self.range_end = self.initial_pair_price + round((math.ceil(self.grid_number/2) - 0.5)*self.base_interval, 0) # Check how to round, how many decimals are needed
        # Send the grid orders
        for i in reversed(range(math.ceil(-self.grid_number/2), math.ceil(self.grid_number/2))):
            if i < 0:
                create_limit_order(client, self.pair, 'BUY', self.amount_per_order_base_currency, self.initial_pair_price + round((i+0.5)*self.base_interval,0)) # Check rounding too
                print(f'BUY at {self.initial_pair_price + round((i+0.5)*self.base_interval,0)}')
            elif i >= 0:
                create_limit_order(client, self.pair, 'SELL', self.amount_per_order_base_currency, self.initial_pair_price + round((i+0.5)*self.base_interval,0)) # Check rounding too
                print(f'SELL at {self.initial_pair_price + round((i+0.5)*self.base_interval,0)}')
        print('Your bot has been launched')

    def detect_grid(self, client):
        self.grid_orders = client.get_open_orders(symbol=self.pair)
        self.grid_sell_orders = [one_order for one_order in self.grid_orders if one_order['side'] == 'SELL' and (float(one_order['price']) - round(0.5*self.base_interval, 0) - self.initial_pair_price)%self.base_interval == 0]
        self.grid_buy_orders = [one_order for one_order in self.grid_orders if one_order['side'] == 'BUY' and (-round(0.5*self.base_interval, 0) + self.initial_pair_price - float(one_order['price']))%self.base_interval == 0]
        self.buy_prices = sorted([float(buy_order['price']) for buy_order in self.grid_buy_orders], reverse=True)
        self.sell_prices = sorted([float(sell_order['price']) for sell_order in self.grid_sell_orders], reverse=True)

    def replace_order(self, client, replaced_order):
        if replaced_order['side'] == 'SELL':
            create_limit_order(client, replaced_order['symbol'], 'BUY', float(replaced_order['origQty']), float(replaced_order['price']))
        elif replaced_order['side'] == 'BUY':
            create_limit_order(client, replaced_order['symbol'], 'SELL', float(replaced_order['origQty']), float(replaced_order['price']))

    def calculate_total_orders_amount(self, client):
        self.detect_grid
        self.pair_price = float(client.get_symbol_ticker(symbol=self.pair)['price'])
        amount_in_buy_orders, amount_in_sell_orders = 0
        for order in self.buy_orders:
            amount_in_buy_orders += float(order['origQty'])*self.pair_price
        for order in self.sell_orders:
            amount_in_sell_orders += float(order['origQty'])*self.pair_price
        print(f"You have an amount of {amount_in_buy_orders} {self.pair[3:]} in buy orders")
        print(f"You have an amount of {amount_in_sell_orders} {self.pair[3:]} in sell orders")

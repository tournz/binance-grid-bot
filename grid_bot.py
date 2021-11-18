from buy_sell_order import create_limit_order
import math

class Gridbot:
    def __init__(self, client, pair, amount_quote_currency, range_start, range_end, grid_number):
        initial_pair_price = client.get_symbol_ticker(symbol=pair)['price']
        if float(initial_pair_price) < float(range_start) or float(range_end) < float(initial_pair_price) or float(range_start) > float(range_end):
            return print('Check your range values')

        if float(client.get_asset_balance(asset=pair[:3])['free']) < (float(amount_quote_currency)/float(initial_pair_price))/2:
            return print(f"Base currency balance insufficient, you have {client.get_asset_balance(asset=pair[:3])['free']} {pair[:3]} and you need {(float(amount_quote_currency)/float(initial_pair_price))/2} {pair[:3]}")

        elif float(client.get_asset_balance(asset=pair[3:])['free']) < float(amount_quote_currency)/2:
            return print(f"Quote currency balance insufficient, you have {client.get_asset_balance(asset=pair[3:])['free']} {pair[3:]} and you need {float(amount_quote_currency)/2} {pair[3:]}")

        else:
            self.sufficient_balance = True
            self.pair = pair
            self.initial_pair_price = float(initial_pair_price)
            self.amount_quote_currency = float(amount_quote_currency)
            self.range_start = float(range_start)
            self.range_end = float(range_end)
            self.grid_number = int(grid_number)

    def create_order_grid(self, client):
        amount_in_buy_orders = 0
        amount_in_sell_orders = 0
        for i in range(math.ceil(-self.grid_number/2), math.ceil(self.grid_number/2) + 1):
            base_interval = (self.range_end - self.range_start)/self.grid_number if self.grid_number%2 == 0 else (self.range_end - self.range_start)/(self.grid_number + 1)
            if i < 0:
                create_limit_order(client, self.pair, 'BUY', (1/(round(self.grid_number/2)))*(self.amount_quote_currency/self.initial_pair_price), round(self.initial_pair_price + i*base_interval, 2))
                print(f'BUY at {round(self.initial_pair_price + i*base_interval, 2)}')
                amount_in_buy_orders += (1/(round(self.grid_number/2)))*(self.amount_quote_currency/self.initial_pair_price)
            elif i > 0:
                create_limit_order(client, self.pair, 'SELL', (1/(round(self.grid_number/2)))*(self.amount_quote_currency/self.initial_pair_price), round(self.initial_pair_price + i*base_interval, 2))
                print(f'SELL at {round(self.initial_pair_price + i*base_interval, 2)}')
                amount_in_sell_orders += (1/(round(self.grid_number/2)))*(self.amount_quote_currency/self.initial_pair_price)
        print(f"You have an amount of {amount_in_buy_orders * self.initial_pair_price} {self.pair[3:]} in buy orders")
        print(f"You have an amount of {amount_in_sell_orders * self.initial_pair_price} {self.pair[3:]} in sell orders")
        print('Your bot has been launched')

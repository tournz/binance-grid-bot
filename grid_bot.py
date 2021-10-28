from buy_sell_order import create_limit_order

class Gridbot:
    def __init__(self, client, pair, amount_quote_currency, range_start, range_end, grid_number):
        initial_pair_price = client.get_symbol_ticker(symbol=pair)['price']
        if float(initial_pair_price) < float(range_start) or float(range_end) < float(initial_pair_price) or float(range_start) > float(range_end):
            return print('Check your range values')

        if float(client.get_asset_balance(asset=pair[:3])['free']) < (float(amount_quote_currency)/float(initial_pair_price))/2:
            self.sufficient_balance = False
            return print(f"Base currency balance insufficient, you have {client.get_asset_balance(asset=pair[:3])['free']} {pair[:3]} and you need {(float(amount_quote_currency)/float(initial_pair_price))/2} {pair[:3]}")

        elif float(client.get_asset_balance(asset=pair[3:])['free']) < float(amount_quote_currency)/2:
            self.sufficient_balance = False
            return print(f"Quote currency balance insufficient, you have {client.get_asset_balance(asset=pair[3:])['free']} {pair[3:]} and you need {float(amount_quote_currency)/2} {pair[3:]}")

        else:
            self.sufficient_balance = True
            self.pair = pair
            self.initial_pair_price = float(initial_pair_price)
            self.amount_quote_currency = float(amount_quote_currency)
            self.range_start = float(range_start)
            self.range_end = float(range_end)
            self.grid_number = int(grid_number)
            self.base_interval = (self.range_end - self.range_start)/self.grid_number

    def create_order_grid(self, client):
        for i in range(-round(self.grid_number/2), round(self.grid_number/2) + 1):
            if i < 0:
                create_limit_order(client, self.pair, 'BUY', (1/(round(self.grid_number/2)))*(self.amount_quote_currency/self.initial_pair_price)/2, self.initial_pair_price + i*self.base_interval)
            elif i > 0:
                create_limit_order(client, self.pair, 'SELL', (1/(round(self.grid_number/2)))*(self.amount_quote_currency/self.initial_pair_price)/2, self.initial_pair_price + i*(self.base_interval))
        print('Your bot has been launched')

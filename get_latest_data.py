import pandas as pd

def get_all_trade_data(client, pair, interval):
    timestamp = client._get_earliest_valid_timestamp(pair, '1d')
    bars = client.get_historical_klines(pair, interval, timestamp, limit=1000)
    pair_df = pd.DataFrame(bars, columns=['date', 'open', 'high', 'low', 'close','volume','close time','quote asset volume','number of trades','taker buy base asset volume','taker buy quote asset volume','ignore'])
    pair_df.set_index('date', inplace=True)
    pair_df.index = pd.to_datetime(pair_df.index, unit='ms')
    pair_df['20sma'] = pair_df.close.rolling(20).mean()
    pair_df.to_csv(path_or_buf=f'/Users/zacharietournant/Downloads/{pair}_data.csv', sep=',')
    return pair_df

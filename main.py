import pandas as pd
import numpy as np

data = {
    'Date': pd.date_range(start='2023-01-01', end='2023-01-10'),
    'Stock_Price': [100, 105, 98, 110, 112, 95, 105, 115, 120, 125]
}

stock_df = pd.DataFrame(data)

def trading_strategy(dataframe, buy_threshold=5, sell_threshold=-5):
    dataframe['Price_Change'] = dataframe['Stock_Price'].pct_change()*100

    dataframe['Signal'] = np.where(dataframe['Price_Change'] > buy_threshold, 'Buy', np.where(dataframe['Price_Change'] < sell_threshold, 'Sell', 'Hold'))

    return dataframe

trading_result = trading_strategy(stock_df)

print(trading_result)
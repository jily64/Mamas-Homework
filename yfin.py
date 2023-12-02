import yfinance as yf

def download_stock_data(ticker, start_date, end_date, timeframe='1d'):
    try:
        data = yf.download(ticker, start_date, end_date, timeframe)

        #print(data.head())

        return data
    except Exception as e:
        print(e)

def calculate_average_prices(df):
    df['Average_Price'] = df[['Open', 'High', 'Low', 'Close']].mean(axis=1)
    return df

def calculate_price_changes(df, col='Close'):
    df['Price_Change'] = df[col].pct_change() * 100
    return df

def get_high_volume_days(df, threshold=1.5):
    high_volume_days = df[df['Volume'] > df['Volume'].mean() * threshold]
    return high_volume_days

def get_high_price_change_days(df, top_n=5):
    high_price_change_days = df.nlargest(top_n, 'Price_Change')
    return high_price_change_days

def get_low_range_days(df, top_n=5):
    df['Range'] = df['High'] - df['Low']
    low_range_days = df.nsmallest(top_n, 'Range')
    return low_range_days

def find_large_price_gaps(df, threshold=2):
    df['Price_Gap'] = df['Open'] - df['Close'].shift(1)
    large_gaps = df[abs(df['Price_Gap']) > threshold]
    return large_gaps

ticker_symbol = 'AAPl'
start_date = '2022-01-01'
end_date = '2023-01-01'
time_frame = '1d'

stock_data = download_stock_data(ticker_symbol, start_date, end_date, timeframe=time_frame)

#stock_data = calculate_average_prices(stock_data) #Калькулятор каких то авераге цены

#stock_data = calculate_price_changes(stock_data) #Калькулятор изменений в цене

#stock_data = get_high_volume_days(stock_data) #Получить дни высокого обьема

#stock_data = get_high_price_change_days(stock_data) #Получить дни с наибольшим процентным изменением цен

#stock_data = get_low_range_days(stock_data) #Дни с самым низким отношением High к Low

#stock_data = find_large_price_gaps(stock_data) #Выявление дней с самыми большими Гэпами между открытием и закрытием

#ddddw

print(stock_data.head())
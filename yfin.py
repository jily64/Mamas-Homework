import yfinance as yf
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import pandas_ta as ta

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

def average_volume_over_period(df, window=5):
    df['Average_Volume'] = df['Volume'].rolling(window=window).mean()
    return df['Average_Volume']

def analyze_correlations(df):
    # Выбираем только числовые столбцы для анализа корреляций
    numeric_columns = df.select_dtypes(include='number')

    # Вычисляем матрицу корреляций
    correlation_matrix = numeric_columns.corr()

    # Используем Seaborn для визуализации корреляций с использованием тепловой карты
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
    plt.title('Correlation Heatmap')
    plt.show()

def overbought_oversold_levels(df, overbought_threshold=70, oversold_threshold=30, length = 7):
    # Рассчитываем индикатор RSI с использованием pandas_ta
    df.ta.rsi(close='Close', length=length, append=True)
    print(df.columns)

    # Используем столбец RSI для выявления "перекупленных" и "перепроданных" уровней
    overbought_levels = df[df['RSI'+'_'+str(length)] > overbought_threshold]
    oversold_levels = df[df['RSI'+'_'+str(length)] < oversold_threshold]

    # Визуализация результатов
    plt.figure(figsize=(12, 6))
    plt.plot(df['Close'], label='Close Price', color='black')
    plt.scatter(overbought_levels.index, overbought_levels['Close'], marker='o', color='red', label='Перекупленность')
    plt.scatter(oversold_levels.index, oversold_levels['Close'], marker='o', color='blue', label='Перепроданность')
    plt.title('Уровни перекупленности и перпроданности')
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.legend()
    plt.show()

def find_pullback_days(df, window=20):
    df['Rolling_Max'] = df['Close'].rolling(window=window).max()
    df['Rolling_Min'] = df['Close'].rolling(window=window).min()

    pullback_days = df[(df['Close'] > df['Rolling_Max'] - df['Close'].rolling(window=window).std()) &
                       (df['Close'] < df['Rolling_Max'])]

    return pullback_days


def plot_fibonacci_levels(dataframe, high_col='High', low_col='Low', levels=[0, 0.236, 0.382, 0.5, 0.618, 0.786, 1.0]):
    """
    Рисует уровни Фибоначчи на графике цен.

    Параметры:
    - dataframe: pandas.DataFrame
        Датафрейм с ценами, содержащий столбцы 'High' и 'Low'.
    - high_col: str, default='High'
        Название столбца с высокой ценой.
    - low_col: str, default='Low'
        Название столбца с низкой ценой.
    - levels: list of float, default=[0, 0.236, 0.382, 0.5, 0.618, 0.786, 1.0]
        Уровни Фибоначчи для отображения.

    Возвращает:
    - None (рисует график)


    Про enumerate:
    используется функция enumerate для итерации по последовательности levels вместе с их индексами.
    В Python enumerate - это встроенная функция, которая возвращает кортежи, содержащие индекс элемента и сам элемент из переданной последовательности

    enumerate(levels) создает итератор, который возвращает кортежи (index, level) для каждого элемента в списке levels.

    for i, level in enumerate(levels): означает, что в каждой итерации цикла i будет содержать индекс текущего элемента, а level - сам элемент из списка levels.

    plt.axhline(y=fibonacci_values[i], linestyle='--', label=f'{int(level*100)}%', color=f'C{i}') используется для построения горизонтальной линии на графике.
    y=fibonacci_values[i] задает высоту линии, label=f'{int(level*100)}%' устанавливает метку для линии в процентах, и color=f'C{i}' задает цвет линии на основе индекса i.

    Таким образом, enumerate используется здесь для того, чтобы иметь доступ как к самим значениям levels, так и к их индексам внутри цикла
    """
    high_price = dataframe[high_col].max()
    low_price = dataframe[low_col].min()

    fibonacci_values = [(high_price - low_price) * level + low_price for level in levels]

    plt.figure(figsize=(12, 6))
    plt.plot(dataframe['Close'], label='Close Price', linewidth=2)

    for i, level in enumerate(levels):
        plt.axhline(y=fibonacci_values[i], linestyle='--', label=f'{int(level * 100)}%', color=f'C{i}')

    plt.title('Fibonacci Levels')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.show()


ticker_symbol = 'AAPL'
start_date = '2010-01-01'
end_date = '2023-01-01'
time_frame = '1y'

stock_data = download_stock_data(ticker_symbol, start_date, end_date, timeframe=time_frame)

#stock_data = calculate_average_prices(stock_data) #Калькулятор каких то авераге цены

#stock_data = calculate_price_changes(stock_data) #Калькулятор изменений в цене

#stock_data = get_high_volume_days(stock_data) #Получить дни высокого обьема

#stock_data = get_high_price_change_days(stock_data) #Получить дни с наибольшим процентным изменением цен

#stock_data = get_low_range_days(stock_data) #Дни с самым низким отношением High к Low

#stock_data = find_large_price_gaps(stock_data) #Выявление дней с самыми большими Гэпами между открытием и закрытием

#stock_data = find_pullback_days(stock_data)

#averages = average_volume_over_period(stock_data) #Средний обьем торгов

#analyze_correlations(stock_data)

plot_fibonacci_levels(stock_data)
print(stock_data.head())
#print(averages.head())
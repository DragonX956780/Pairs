import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt
import pandas_ta as ta

def create_candlestick_chart(input_file, output_file, stock, backtesting_instance, volume=False, bollinger_bands=False, moving_averages=False, rsi=False):
    data_original = pd.read_csv(input_file, index_col=0, parse_dates=True)
    msft_columns = [col for col in data_original.columns if 'MSFT' in col]
    msft_data = data_original[msft_columns]
    msft_data.columns = [col.replace('MSFT ', '') for col in msft_data.columns]

    data = msft_data.copy()
    data.index.name = 'Date'
    data = data.rename(columns={'Adj Close': 'Close', 'High': 'High', 'Low': 'Low', 'Open': 'Open', 'Volume': 'Volume'})
    data = data[['Open', 'High', 'Low', 'Close', 'Volume']]

    buy_dates = [order['date'] for order in backtesting_instance.orders if order['type'] == 'buy' and order['stock'] == stock]
    sell_dates = [order['date'] for order in backtesting_instance.orders if order['type'] == 'sell' and order['stock'] == stock]

    buy_signals = data.loc[buy_dates]
    sell_signals = data.loc[sell_dates]

    apds = []

    if volume:
        apds.append(mpf.make_addplot(data['Volume'], panel=1, color='g', secondary_y=False))

    if bollinger_bands:
        data['upper_bb'], data['middle_bb'], data['lower_bb'] = ta.bbands(data['Close'])
        apds.append(mpf.make_addplot(data['upper_bb'], color='silver'))
        apds.append(mpf.make_addplot(data['middle_bb'], color='silver'))
        apds.append(mpf.make_addplot(data['lower_bb'], color='silver'))

    if moving_averages:
        data['SMA20'] = ta.sma(data['Close'], length=20)
        data['SMA50'] = ta.sma(data['Close'], length=50)
        apds.append(mpf.make_addplot(data['SMA20'], color='magenta'))
        apds.append(mpf.make_addplot(data['SMA50'], color='orange'))

    if rsi:
        data['RSI'] = backtesting_instance.calculate_rsi(data_original)
        apds.append(mpf.make_addplot(data['RSI'], panel=2, color='b', secondary_y=False))

    fig, axes = mpf.plot(data, type='candle', style='charles', title=f'{stock} Candlestick Chart', ylabel='Price', addplot=apds, returnfig=True, volume=volume)

    for index, row in buy_signals.iterrows():
        axes[0].annotate('BUY', xy=(index, row['Low']), xytext=(index, row['Low'] - 1), arrowprops=dict(facecolor='green', edgecolor='green', shrink=0.05), fontsize=8, color='g')

    for index, row in sell_signals.iterrows():
        axes[0].annotate('SELL', xy=(index, row['High']), xytext=(index, row['High'] + 1), arrowprops=dict(facecolor='red', edgecolor='red', shrink=0.05), fontsize=8, color='r')

    plt.savefig(output_file)
    plt.close()

def create_all_charts(backtesting_instance, volume=False, bollinger_bands=False, moving_averages=False, rsi=False):
    create_candlestick_chart('historical_stock_data.csv', 'static/MSFT_chart.png', 'MSFT', backtesting_instance, volume=volume, bollinger_bands=bollinger_bands, moving_averages=moving_averages, rsi=rsi)


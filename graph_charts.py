import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import mplfinance as mpf
import matplotlib.dates as mdates
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib
matplotlib.use('agg')
import os
from PIL import Image


def plot_data_points():
    # Sample data points
    x = [1, 2, 3, 4, 5]
    y = [2, 4, 6, 8, 10]

    # Create a figure and axis
    fig, ax = plt.subplots()

    # Plot the data points
    ax.scatter(x, y)

    # Set labels for the x and y axes
    ax.set_xlabel('X Axis')
    ax.set_ylabel('Y Axis')

    # Set the title of the plot
    ax.set_title('Sample Data Points')

    # Save the plot as an image
    plt.savefig('static/plot.png', format='png', bbox_inches='tight')

def add_bollinger_bands(data):
    data_with_bb = data.copy()
    data_with_bb['20 Day MA'] = data['Close'].rolling(window=20).mean()
    data_with_bb['Upper Band'] = data_with_bb['20 Day MA'] + 2 * data['Close'].rolling(window=20).std()
    data_with_bb['Lower Band'] = data_with_bb['20 Day MA'] - 2 * data['Close'].rolling(window=20).std()
    bollinger_bands = [mpf.make_addplot(data_with_bb['20 Day MA']), mpf.make_addplot(data_with_bb['Upper Band']), mpf.make_addplot(data_with_bb['Lower Band'])]
    return bollinger_bands, data_with_bb

def add_moving_averages(data):
    data_with_ma = data.copy()
    data_with_ma['50 Day MA'] = data['Close'].rolling(window=50).mean()
    data_with_ma['200 Day MA'] = data['Close'].rolling(window=200).mean()
    moving_averages = [mpf.make_addplot(data_with_ma['50 Day MA'], color='red'), mpf.make_addplot(data_with_ma['200 Day MA'], color='blue')]
    return moving_averages, data_with_ma

def add_rsi(data, period=14):
    delta = data['Close'].diff()
    gains = delta.where(delta > 0, 0)
    losses = -delta.where(delta < 0, 0)

    avg_gain = gains.rolling(window=period).mean()
    avg_loss = losses.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    data_with_rsi = data.copy()
    data_with_rsi['RSI'] = rsi

    rsi_plot = mpf.make_addplot(data_with_rsi['RSI'], panel=1, secondary_y=False, color='g')
    return rsi_plot, data_with_rsi


def add_volume(data, stock, data_original):
    data_with_volume = data.copy()
    data_with_volume['Volume'] = data_original[f'{stock} Volume']
    return data_with_volume

def create_candlestick_chart(csv_file, output_filename, stock, backtesting_instance=None, volume=False, bollinger_bands=False, moving_averages=False, rsi=False, line_graph=False):
    data_original = pd.read_csv(csv_file, index_col=0, parse_dates=True)
    column_prefix = stock
    data = data_original[[f'{column_prefix} Open', f'{column_prefix} High', f'{column_prefix} Low', f'{column_prefix} Close']]
    data.columns = ['Open', 'High', 'Low', 'Close']

    if volume:
        data = add_volume(data, stock, data_original)

    additional_plots = []

    if bollinger_bands:
        bb_plots, data = add_bollinger_bands(data)
        additional_plots.extend(bb_plots)

    if moving_averages:
        ma_plots, data = add_moving_averages(data)
        additional_plots.extend(ma_plots)

    if rsi:
        rsi_plot, data = add_rsi(data)
        additional_plots.append(rsi_plot)

    chart_type = 'line' if line_graph else 'candle'

    if backtesting_instance:
        events = backtesting_instance.get_events(stock=stock)
        buy_events = {pd.to_datetime(event[0]): event[2] for event in events if event[1] == 'buy' and event[0] in data.index}
        sell_events = {pd.to_datetime(event[0]): event[2] for event in events if event[1] == 'sell' and event[0] in data.index}

        buy_df = data[['Close']].copy()
        sell_df = data[['Close']].copy()

        buy_df['Price'] = buy_df.index.map(buy_events).fillna(None)
        sell_df['Price'] = sell_df.index.map(sell_events).fillna(None)

        buy_markers = mpf.make_addplot(buy_df['Price'], scatter=True, markersize=100, marker='^', color='g') if not buy_df['Price'].isnull().all() else None
        sell_markers = mpf.make_addplot(sell_df['Price'], scatter=True, markersize=100, marker='v', color='r') if not sell_df['Price'].isnull().all() else None

        markers = [buy_markers, sell_markers]
        markers = [m for m in markers if m is not None]  # Remove None values from the markers list
        mpf.plot(data, type=chart_type, style='charles', title=f'{stock} Candlestick Chart', ylabel='Price',
                ylabel_lower='Volume', volume=volume, addplot=markers + additional_plots, savefig=output_filename)

    else:
        mpf.plot(data, type=chart_type, style='charles', title=f'{stock} Candlestick Chart', ylabel='Price',
                ylabel_lower='Volume', volume=volume, savefig=output_filename)

def create_combined_chart(first_stock_chart, second_stock_chart, output_filename):
    image1 = Image.open(first_stock_chart)
    image2 = Image.open(second_stock_chart)

    image1 = image1.convert("RGBA")
    image2 = image2.convert("RGBA")

    combined_image = Image.blend(image1, image2, alpha=0.5)
    combined_image.save(output_filename)

def create_all_charts(first_stock, second_stock, backtesting_instance=None, volume=False, bollinger_bands=False, moving_averages=False, rsi=False, line_graph=False):
    create_candlestick_chart('historical_stock_data.csv', 'static/first_stock_chart.png', first_stock, backtesting_instance=backtesting_instance, volume=volume, bollinger_bands=bollinger_bands, moving_averages=moving_averages, rsi=rsi, line_graph=line_graph)
    create_candlestick_chart('historical_stock_data.csv', 'static/second_stock_chart.png', second_stock, backtesting_instance=backtesting_instance, volume=volume, bollinger_bands=bollinger_bands, moving_averages=moving_averages, rsi=rsi, line_graph=line_graph)
    
    create_combined_chart('static/first_stock_chart.png', 'static/second_stock_chart.png', 'static/combined_stock_chart.png')


import pandas as pd
import numpy as np

class Backtesting:
    def __init__(self, csv_file):
        self.data = pd.read_csv(csv_file, index_col=0, parse_dates=True)
        self.events = []

    def buy(self, index, price, stock):
        self.events.append((index, "buy", price, stock))

    def sell(self, index, price, stock):
        self.events.append((index, "sell", price, stock))

    def basic_strategy(self, stock, buy_threshold, sell_threshold):
        data = self.data[[f'{stock} Open', f'{stock} High', f'{stock} Low', f'{stock} Close']]
        data.columns = ['Open', 'High', 'Low', 'Close']

        position = 0
        buy_price = 0
        profit = 0

        for index, row in data.iterrows():
            if row['Close'] < buy_threshold and position == 0:
                position = 1
                buy_price = row['Close']
                self.buy(index, buy_price, stock)
            elif row['Close'] > sell_threshold and position == 1:
                position = 0
                sell_price = row['Close']
                profit += sell_price - buy_price
                self.sell(index, sell_price, stock)

        return profit

    def get_events(self, stock=None):
        if stock is not None:
            return [event for event in self.events if event[3] == stock]
        return self.events


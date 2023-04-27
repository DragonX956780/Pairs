import pandas as pd
import numpy as np

class Backtesting:
    def __init__(self, csv_file):
        self.data = pd.read_csv(csv_file, index_col=0, parse_dates=True)
        self.events = []
        self.total_bought = 0  
        self.total_sold = 0    

    def buy(self, index, price, stock, shares=1):
        self.events.append((index, "buy", price, stock, shares))
        self.total_bought += price * shares

    def sell(self, index, price, stock, shares=1):
        self.events.append((index, "sell", price, stock, shares))
        self.total_sold += price * shares


    def percentage_gain(self):
        if self.total_bought == 0:
            return 0
        return ((self.total_sold - self.total_bought) / self.total_bought) * 100

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

    def pairs_trading_strategy(self, stock1, stock2, entry_threshold, exit_threshold, shares=10):
        data1 = self.data[[f'{stock1} Open', f'{stock1} High', f'{stock1} Low', f'{stock1} Close']]
        data1.columns = ['Open1', 'High1', 'Low1', 'Close1']

        data2 = self.data[[f'{stock2} Open', f'{stock2} High', f'{stock2} Low', f'{stock2} Close']]
        data2.columns = ['Open2', 'High2', 'Low2', 'Close2']

        data = pd.concat([data1, data2], axis=1)
        data['Spread'] = data['Close1'] - data['Close2']
        data['ZScore'] = (data['Spread'] - data['Spread'].rolling(30).mean()) / data['Spread'].rolling(30).std()

        position = 0
        profit = 0
        buy_price1, buy_price2 = 0, 0

        for index, row in data.iterrows():
            if row['ZScore'] < -entry_threshold and position == 0:
                position = 1
                buy_price1 = row['Close1']
                buy_price2 = row['Close2']
                self.buy(index, buy_price1, stock1, shares)
                self.sell(index, buy_price2, stock2, shares)
            elif row['ZScore'] > entry_threshold and position == 0:
                position = -1
                buy_price1 = row['Close1']
                buy_price2 = row['Close2']
                self.sell(index, buy_price1, stock1, shares)
                self.buy(index, buy_price2, stock2, shares)
            elif position == 1 and row['ZScore'] > -exit_threshold:
                position = 0
                sell_price1 = row['Close1']
                sell_price2 = row['Close2']
                profit += (sell_price1 - buy_price1) * shares - (sell_price2 - buy_price2) * shares
                self.sell(index, sell_price1, stock1, shares)
                self.buy(index, sell_price2, stock2, shares)
            elif position == -1 and row['ZScore'] < exit_threshold:
                position = 0
                sell_price1 = row['Close1']
                sell_price2 = row['Close2']
                profit += (buy_price1 - sell_price1) * shares - (buy_price2 - sell_price2) * shares
                self.buy(index, sell_price1, stock1, shares)
                self.sell(index, sell_price2, stock2, shares)

        return profit


    def get_events(self, stock=None):
        if stock is not None:
            return [event for event in self.events if event[3] == stock]
        return self.events


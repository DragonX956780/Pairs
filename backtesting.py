import pandas_ta as ta

class Backtesting:
    def __init__(self, period = 14):
        self.orders = []
        self.period = period
    
    def calculate_rsi(self, stock_data):
        close_column = [col for col in stock_data.columns if 'Close' in col][0]  # Identify the close column
        return ta.rsi(stock_data[close_column], length=self.period)



    def buy(self, stock, price, shares):
        order = {
            'stock': stock,
            'price': price,
            'shares': shares,
            'type': 'buy'
        }
        self.orders.append(order)

    def sell(self, stock, price, shares):
        order = {
            'stock': stock,
            'price': price,
            'shares': shares,
            'type': 'sell'
        }
        self.orders.append(order)
    
    def backtest_basic_strategy(self, historical_data):
        positions = []
        total_profit = 0

        historical_data['RSI'] = self.calculate_rsi(historical_data)

        for index, row in historical_data.iterrows():
            # Buy signal
            if row['RSI'] < 30:
                self.buy('AAPL', row['Close'], 1)
                positions.append({'stock': 'AAPL', 'buy_price': row['Close'], 'buy_date': index})

            # Sell signal
            elif row['RSI'] > 70:
                for position in positions:
                    if position['stock'] == 'AAPL':
                        self.sell('AAPL', row['Close'], 1)
                        profit = row['Close'] - position['buy_price']
                        total_profit += profit
                        positions.remove(position)

            # Close all positions at the end of the month
            if index.month != row.name.month:
                for position in positions:
                    if position['stock'] == 'AAPL':
                        self.sell('AAPL', row['Close'], 1)
                        profit = row['Close'] - position['buy_price']
                        total_profit += profit
                        positions.remove(position)

        return total_profit


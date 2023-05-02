import yfinance as yf
import pandas as pd

def download_sp500_history(start_date, end_date):
    sp500 = yf.Ticker('^GSPC')
    sp500_history = sp500.history(start=start_date, end=end_date)
    return sp500_history

if __name__ == "__main__":
    start_date = '2000-01-01'
    end_date = '2021-09-30'
    sp500_history = download_sp500_history(start_date, end_date)
    sp500_history.to_csv('historical_sp500_data.csv')
    print("S&P 500 historical data saved to 'historical_sp500_data.csv'")

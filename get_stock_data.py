import yfinance as yf
import pandas as pd

def get_historical_data(tickers, start_date, end_date, csv_file):
    data = yf.download(tickers, start=start_date, end=end_date)

    # Update column names
    new_columns = []
    for col in data.columns:
        new_col = col[1] + ' ' + col[0]
        new_columns.append(new_col)
    data.columns = new_columns

    # Save the data to a CSV file
    data.to_csv(csv_file)

if __name__ == "__main__":
    # Example usage
    tickers = "AAPL MSFT"  # You can add more tickers separated by a space
    start_date = "2020-01-01"
    end_date = "2020-12-31"
    csv_file = "historical_stock_data.csv"

    get_historical_data(tickers, start_date, end_date, csv_file)


import pandas as pd

def find_similar_stocks(csv_file):
    data = pd.read_csv(csv_file, index_col=0, parse_dates=True)

    stock_symbols = set([col.split()[0] for col in data.columns if "Close" in col])
    close_prices = []

    for symbol in stock_symbols:
        close_prices.append(data[f"{symbol} Close"].rename(symbol))

    stock_close_prices = pd.concat(close_prices, axis=1)

    corr_matrix = stock_close_prices.corr()

    candidates = []

    for i in range(len(corr_matrix)):
        for j in range(i+1, len(corr_matrix)):
            stock_i = corr_matrix.columns[i]
            stock_j = corr_matrix.columns[j]
            correlation = corr_matrix.at[stock_i, stock_j]

            mean_i = stock_close_prices[stock_i].mean()
            mean_j = stock_close_prices[stock_j].mean()
            mean_diff_ratio = abs(mean_i - mean_j) / max(mean_i, mean_j)

            if correlation > 0.9 and mean_diff_ratio < 0.1:
                candidates.append((stock_i, stock_j, correlation))

    candidates.sort(key=lambda x: x[2], reverse=True)

    return candidates


if __name__ == "__main__":
    candidates = find_similar_stocks('historical_stock_data.csv')

    with open('static/candidates.txt', 'w') as f:
        if candidates:
            f.write("Stock pairs for pairs trading:\n")
            for stock1, stock2, correlation in candidates:  # Updated this line
                f.write(f"{stock1}, {stock2}\n")
        else:
            f.write("No suitable stock pairs found.")


import pandas as pd
from backtesting import Backtesting
import numpy as np
from tqdm import tqdm

def optimize_pairs_trading(backtest, stock1, stock2, entry_threshold_range, exit_threshold_range, benchmark_stock, weights):
    best_entry = 0
    best_exit = 0
    best_score = -np.inf

    for entry_threshold in entry_threshold_range:
        for exit_threshold in exit_threshold_range:
            backtest.events = []
            backtest.total_bought = 0
            backtest.total_sold = 0
            profit = backtest.pairs_trading_strategy(stock1, stock2, entry_threshold, exit_threshold)
            percentage_gain = backtest.percentage_gain()
            alpha = backtest.calculate_alpha(stock1, stock2, benchmark_stock)
            beta = backtest.calculate_beta(stock1, stock2, benchmark_stock)
            sharpe = backtest.sharpe_ratio(stock1, stock2, benchmark_stock)

            score = (weights['profit'] * percentage_gain
                     + weights['alpha'] * alpha
                     - weights['beta'] * abs(beta)
                     + weights['sharpe'] * sharpe)

            if score > best_score:
                best_score = score
                best_entry = entry_threshold
                best_exit = exit_threshold

    if best_score == -np.inf:
        print(f"Possible issue with stock pair: {stock1}, {stock2}")

    return best_entry, best_exit, best_score



def read_stock_pairs(file_path):
    with open(file_path, 'r') as f:
        content = f.readlines()
    
    stock_pairs = []

    for line in content[1:]:
        stock1, stock2 = line.strip().split(', ')
        stock_pairs.append((stock1, stock2))

    return stock_pairs


def write_optimization_results(file_path, results):
    with open(file_path, 'w') as f:
        f.write('Stock1,Stock2,EntryThreshold,ExitThreshold,PercentageGain\n')
        for result in results:
            f.write(','.join(map(str, result)) + '\n')


if __name__ == "__main__":
    backtest = Backtesting('historical_stock_data.csv')
    stock_pairs = read_stock_pairs('static/candidates.txt')

    entry_threshold_range = np.arange(1, 3, 0.1)
    exit_threshold_range = np.arange(0, 1, 0.1)

    optimization_results = []
    benchmark_stock = 'SPY'  # Set the benchmark stock (e.g., SPY for S&P 500)
    weights = {
        'profit': 1,
        'alpha': 1,
        'beta': 1,
        'sharpe': 1
    }

    for stock1, stock2 in tqdm(stock_pairs, desc="Optimizing", ncols=100):
        best_entry, best_exit, best_score = optimize_pairs_trading(backtest, stock1, stock2, entry_threshold_range, exit_threshold_range, benchmark_stock, weights)
        optimization_results.append((stock1, stock2, best_entry, best_exit, best_score))

    write_optimization_results('optimized.csv', optimization_results)


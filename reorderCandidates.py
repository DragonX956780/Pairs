import pandas as pd

def read_optimization_results(file_path):
    optimized_data = pd.read_csv(file_path)
    return optimized_data

def write_sorted_candidates(file_path, sorted_pairs):
    with open(file_path, 'w') as f:
        for pair in sorted_pairs:
            f.write(','.join(pair) + '\n')

if __name__ == "__main__":
    optimized_data = read_optimization_results('optimized.csv')
    sorted_data = optimized_data.sort_values(by='PercentageGain', ascending=False)

    sorted_pairs = [(row['Stock1'], row['Stock2']) for _, row in sorted_data.iterrows()]
    write_sorted_candidates('candidates.txt', sorted_pairs)

from flask import Flask, render_template, request
import graph_charts
from backtesting import Backtesting
from flask import jsonify

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        stock_pair = request.form["stock_pair"].split(",")
        if len(stock_pair) != 2:
            return "Invalid stock pair selected.", 400

        first_stock, second_stock = [stock.strip() for stock in stock_pair]

        volume = request.form.get("volume") == "on"
        bollinger_bands = request.form.get("bollinger_bands") == "on"
        moving_averages = request.form.get("moving_averages") == "on"
        rsi = request.form.get("rsi") == "on"
        line_graph = request.form.get("line_graph") == "on"

        backtesting_instance = Backtesting('historical_stock_data.csv')
        entry_threshold = 1
        exit_threshold = 1

        # Use pairs_trading_strategy instead of basic_strategy
        profit = backtesting_instance.pairs_trading_strategy(first_stock, second_stock, entry_threshold, exit_threshold)

        graph_charts.create_all_charts(
            backtesting_instance=backtesting_instance,
            volume=volume,
            bollinger_bands=bollinger_bands,
            moving_averages=moving_averages,
            rsi=rsi,
            line_graph=line_graph,
            first_stock=first_stock,
            second_stock=second_stock
        )

        # Calculate the new capital value
        initial_capital = 10000
        new_capital = initial_capital + profit

        return jsonify({'new_capital': new_capital})

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)


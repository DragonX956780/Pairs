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
        profit = backtesting_instance.pairs_trading_strategy(first_stock, second_stock)

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

        # Calculate the percentage profit
        percentage_profit = backtesting_instance.percentage_gain()
        benchmark_stock = 'SPY'
        alpha = backtesting_instance.calculate_alpha(first_stock, second_stock, benchmark_stock)
        beta = backtesting_instance.calculate_beta(first_stock, second_stock, benchmark_stock)
        sharpe_ratio = backtesting_instance.sharpe_ratio(first_stock, second_stock, benchmark_stock)

        return jsonify({'new_capital': new_capital, 'percentage_profit': percentage_profit, 'alpha': alpha, 'beta': beta, 'sharpe_ratio': sharpe_ratio})





    return render_template("index.html")

@app.route("/channels", methods=["GET", "POST"])
def channels():
    if request.method == "POST":
        stock = request.form["stock"]
        
        volume = request.form.get("volume") == "on"
        bollinger_bands = request.form.get("bollinger_bands") == "on"
        moving_averages = request.form.get("moving_averages") == "on"
        rsi = request.form.get("rsi") == "on"
        line_graph = request.form.get("line_graph") == "on"

        backtesting_instance = Backtesting('historical_stock_data.csv')

        # Generate chart for the selected stock with the specified features
        graph_charts.create_candlestick_chart(
            csv_file='historical_stock_data.csv',
            output_filename='static/stock_chart.png',
            stock=stock,
            backtesting_instance=backtesting_instance,
            volume=volume,
            bollinger_bands=bollinger_bands,
            moving_averages=moving_averages,
            rsi=rsi,
            line_graph=line_graph,
        )

        return jsonify({'chart_filename':'stock_chart.png'})  # Return an empty JSON object as we're not using the response data

    return render_template("channels.html")


if __name__ == "__main__":
    app.run(debug=True)


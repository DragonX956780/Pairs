from flask import Flask, render_template, request
import graph_charts
from backtesting import Backtesting

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        volume = request.form.get("volume") == "on"
        bollinger_bands = request.form.get("bollinger_bands") == "on"
        moving_averages = request.form.get("moving_averages") == "on"
        rsi = request.form.get("rsi") == "on"

        backtesting_instance = Backtesting('historical_stock_data.csv')
        backtesting_instance.basic_strategy('AAPL', buy_threshold=110, sell_threshold=120)
        backtesting_instance.basic_strategy('MSFT', buy_threshold=160, sell_threshold=180)

        graph_charts.create_all_charts(backtesting_instance=backtesting_instance, volume=volume, bollinger_bands=bollinger_bands, moving_averages=moving_averages, rsi=rsi)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)


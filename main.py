from flask import Flask, render_template, request
import graph_charts

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        volume = request.form.get("volume") == "on"
        bollinger_bands = request.form.get("bollinger_bands") == "on"
        moving_averages = request.form.get("moving_averages") == "on"
        rsi = request.form.get("rsi") == "on"

        graph_charts.create_all_charts(volume=volume, bollinger_bands=bollinger_bands, moving_averages=moving_averages, rsi=rsi)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)


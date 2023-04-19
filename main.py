from flask import Flask, render_template, request
import pandas as pd
from get_stock_data import get_stock_data

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        tickers = request.form.get('tickers')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        stock_data = get_stock_data(tickers, start_date, end_date)

        return render_template('index.html', stock_data=stock_data.to_html())

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)


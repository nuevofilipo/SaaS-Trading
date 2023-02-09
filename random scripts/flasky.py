from flask import Flask, jsonify
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import datetime as dt
from flask import render_template


app = Flask(__name__)


@app.route("/")
def chart():
    return render_template("templates/updater.html")


@app.route("/data")
def data():
    start_date = "2023-01-01"
    end_date1 = dt.datetime.now()
    btc = yf.Ticker("BTC-USD")
    hourly_data = btc.history(interval="1h", start=start_date, end=end_date1)
    df = pd.DataFrame(hourly_data)
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=df.index,
                open=df["Open"],
                high=df["High"],
                low=df["Low"],
                close=df["Close"],
            )
        ]
    )
    fig.update_layout(
        title="Bitcoin Price (USD)", xaxis_title="Date", yaxis_title="Price"
    )
    return jsonify(fig)


if __name__ == "__main__":
    app.run(debug=True)


    

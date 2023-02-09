import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import datetime as dt

start_date = "2023-01-01"
end_date = dt.datetime.now()

# Get the historical data for BTC
btc = yf.Ticker("BTC-USD")

# Get hourly data
hourly_data = btc.history(interval="1h", start=start_date, end=end_date)

# Create a candlestick chart using plotly
fig = go.Figure(
    data=[
        go.Candlestick(
            x=hourly_data.index,
            open=hourly_data["Open"],
            high=hourly_data["High"],
            low=hourly_data["Low"],
            close=hourly_data["Close"],
        )
    ]
)
fig.update_layout(title="Bitcoin Price (USD)", xaxis_title="Date", yaxis_title="Price")
fig.show()

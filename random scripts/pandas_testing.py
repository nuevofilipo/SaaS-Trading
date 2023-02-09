import dash
from dash import dcc
from dash import html
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import datetime as dt
from dash.dependencies import Input, Output
from dash import dcc
import talib as ta

app = dash.Dash()

start_date = "2023-01-20"
end_date = "2023-01-01"
end_date1 = dt.datetime.now()

btc = yf.Ticker("BTC-USD")
hourly_data = btc.history(interval="1h", start=start_date, end=end_date1)

df = pd.DataFrame(hourly_data)
uf = df[["Close"]]

df["MA"] = ta.SMA(df["Close"], timeperiod=7)


# print(uf)


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

moving_average = go.Scatter(x=df.index, y=df["MA"], mode="lines", name="Moving Average")

fig.add_trace(moving_average)

fig.show()

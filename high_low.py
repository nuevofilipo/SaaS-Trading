import plotly.graph_objects as go
import pandas as pd
import datetime as dt
import yfinance as yf

# importing from binance
from binance.spot import Spot as Client

# import talib as ta
import pandas_ta as ta
from scipy.signal import savgol_filter
from scipy.signal import find_peaks

# connecting binance data
# connecting binance data
base_url = "https://api.binance.com"
spot_client = Client(base_url=base_url)

btcusd_historical = spot_client.klines("BTCUSDT", "1w", limit=280)
# print(btcusd_historical)

columns = [
    "Open time",
    "Open",
    "High",
    "Low",
    "Close",
    "Volume",
    "Close time",
    "quote_asset_volume",
    "number_of_trades",
    "taker_buy_base_asset_volume",
    "taker_buy_quote_asset_volume",
    "ignore",
]


df = pd.DataFrame(btcusd_historical, columns=columns)
df["time"] = pd.to_datetime(df["Open time"], unit="ms")
df = df[["time", "Open", "High", "Low", "Close", "Volume"]]
df[["Open", "High", "Low", "Close", "Volume"]] = df[
    ["Open", "High", "Low", "Close", "Volume"]
].astype(float)
print(df)


# date_range = df.loc[df.index[-149] : df.index[-1]]

date_range = df.iloc[-200:]
min_value = round(float(date_range["Close"].min()))
max_value = round(float(date_range["Close"].max()))


print(date_range["Close"])
print(min_value, max_value)
print(date_range["Close"].max())

df.set_index("time", inplace=True)


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
    yaxis=dict(range=[min_value * 0.9, max_value * 1.1]),
    xaxis=dict(
        range=[df.index[-200], df.index[-1]],
    ),
)


fig.show()

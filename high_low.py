import plotly.graph_objects as go
import pandas as pd
import datetime as dt
import yfinance as yf

# import talib as ta
import pandas_ta as ta
from scipy.signal import savgol_filter
from scipy.signal import find_peaks


start_date = "2021-01-01"
end_date = dt.datetime.now()

btc = yf.Ticker("BTC-USD")
data = btc.history(interval="1d", start=start_date, end=end_date)

df = pd.DataFrame(data)
df = df[
    [
        "Open",
        "High",
        "Low",
        "Close",
    ]
]

df["atr"] = ta.atr(df["High"], df["Low"], df["Close"], length=1)
df["atr"] = df.atr.rolling(window=30).mean()

df["close_smooth"] = savgol_filter(df["Close"], 15, 5)
# (49, 2) official from video


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

smoothing = go.Scatter(x=df.index, y=df["close_smooth"], mode="lines", name="Smoothed")
fig.add_trace(smoothing)

atr = df["atr"].iloc[-1]

peaks_idx, _ = find_peaks(df["close_smooth"], distance=15, width=3, prominence=atr)
troughs_idx, _ = find_peaks(-df["close_smooth"], distance=15, width=3, prominence=atr)


peaks = go.Scatter(
    x=df.index[peaks_idx],
    y=df["close_smooth"][peaks_idx],
    mode="markers",
    name="Peaks",
    marker=dict(color="blue", size=12),
)

troughs = go.Scatter(
    x=df.index[troughs_idx],
    y=df["close_smooth"][troughs_idx],
    mode="markers",
    name="Troughs",
    marker=dict(color="yellow", size=12),
)

fig.add_trace(peaks)
fig.add_trace(troughs)


fig.show()

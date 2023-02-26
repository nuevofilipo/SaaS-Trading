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

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# connecting binance data
# connecting binance data


app = dash.Dash()  # creating the dash app


# Getting the Data, and plotting chart-----------------------------------------


def gettingData(coin, candleTimeFrame):
    base_url = "https://api.binance.com"
    spot_client = Client(base_url=base_url)

    limit = 200
    btcusd_historical = spot_client.klines(coin, candleTimeFrame, limit=limit)

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
    df[["Open", "High", "Low", "Close", "Volume"]] = (
        df[["Open", "High", "Low", "Close", "Volume"]].astype(float).astype(int)
    )

    # print(df)

    # date_range = df.loc[df.index[-149] : df.index[-1]]

    date_range = df.iloc[-200:]
    min_value = round(float(date_range["Close"].min()))
    max_value = round(float(date_range["Close"].max()))

    df.set_index("time", inplace=True)
    return df


df = gettingData("BTCUSDT", "1d")

fig = go.Figure(
    data=[
        go.Candlestick(
            x=df.index,
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            increasing_line_color="black",
            decreasing_line_color="red",
            increasing_fillcolor="black",
            decreasing_fillcolor="red",
        )
    ]
)

# ------------------------------------------------------------

options = ["BTCUSDT", "ETHUSDT"]

app.layout = html.Div(
    [
        dcc.Dropdown(
            className="drop-down",
            options=options,
            value="BTCUSDT",
            id="crypto_select",
            clearable=False,
        ),
        # html.H1("Candlestick Chart"),
        dcc.Graph(
            id="candlestick-chart",
            figure=fig,
            style={"height": "100vh", "width": "100vw"},
            config=dict(
                {"scrollZoom": True, "displayModeBar": False},
            ),
        ),
    ]
)


@app.callback(
    Output("candlestick-chart", "figure"),
    Input(component_id="crypto_select", component_property="value"),
)
def update_chart(value):
    df = gettingData(value, "1d")

    fig = go.Figure(
        data=[
            go.Candlestick(
                x=df.index,
                open=df["Open"],
                high=df["High"],
                low=df["Low"],
                close=df["Close"],
                increasing_line_color="green",
                decreasing_line_color="red",
                increasing_fillcolor="green",
                decreasing_fillcolor="red",
            )
        ]
    )

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)

import dash
from dash import dcc
from dash import html
import plotly.graph_objects as go
import plotly.express as px
import plotly
import pandas as pd
import datetime as dt
from dash.dependencies import Input, Output
from dash import dcc
import talib as ta

from scipy.signal import savgol_filter
from scipy.signal import find_peaks
import pandas_ta as tan

# importing from binance
from binance.spot import Spot as Client


app = dash.Dash()  # creating the dash app


def gettingData(coin, candleTimeFrame):
    limit = 365
    base_url = "https://api.binance.com"
    spot_client = Client(base_url=base_url)

    btcusd_historical = spot_client.klines(coin, candleTimeFrame, limit=limit)
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
    df[["Open", "High", "Low", "Close", "Volume"]] = (
        df[["Open", "High", "Low", "Close", "Volume"]].astype(float).astype(int)
    )
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
            increasing_line_color="#56b36a",
            decreasing_line_color="red",
            increasing_fillcolor="#56b36a",
            decreasing_fillcolor="red",
        )
    ]
)
# ctrl f2 for renaming all variables at once
options = ["BTCUSDT", "ETHUSDT"]

app.layout = html.Div(
    [
        html.Button("Toggle Dark Mode", className="toggle-button", id="dark-mode-btn"),
        html.Button("daily/weekly", className="toggle-button", id="daily-weekly-btn"),
        dcc.Dropdown(
            className="drop-down",
            options=options,
            value="BTCUSDT",
            id="crypto_select",
            clearable=False,
        ),
        dcc.Graph(
            id="candlestick-chart",
            figure=fig,
            style={"height": "100vh", "width": "100vw"},
            config=dict(
                {"scrollZoom": True, "displayModeBar": False},
            ),
        ),
        dcc.Interval(
            id="interval-component", interval=10000, n_intervals=0  # in milliseconds
        ),
    ]
)


@app.callback(
    Output("candlestick-chart", "figure"),
    [Input("interval-component", "n_intervals")],
    Input(component_id="crypto_select", component_property="value"),
    [dash.dependencies.Input("dark-mode-btn", "n_clicks")],
    [dash.dependencies.Input("daily-weekly-btn", "n_clicks")],
)
def update_chart(n, n_clicks_1, n_clicks_2, value):
    if n_clicks_2 is not None and n_clicks_2 % 2 == 1:
        df = gettingData(value, "1d")
        df["MA"] = ta.SMA(df["Close"], timeperiod=63)
        df["EMA"] = ta.EMA(df["Close"], timeperiod=84)
    else:
        df = gettingData(value, "1w")
        df["MA"] = ta.SMA(df["Close"], timeperiod=9)
        df["EMA"] = ta.EMA(df["Close"], timeperiod=12)

    df["atr"] = tan.atr(df["High"], df["Low"], df["Close"], length=1)
    df["atr"] = df.atr.rolling(window=30).mean()
    df["close_smooth"] = savgol_filter(df["Close"], 15, 5)

    fig = go.Figure(
        data=[
            go.Candlestick(
                x=df.index,
                open=df["Open"],
                high=df["High"],
                low=df["Low"],
                close=df["Close"],
                name="Bitcoin Price (USD)",
                increasing_line_color="#56b36a",
                decreasing_line_color="red",
                increasing_fillcolor="#56b36a",
                decreasing_fillcolor="red",
            )
        ],
    )

    smoothing = go.Scatter(
        x=df.index, y=df["close_smooth"], mode="lines", name="Smoothed"
    )
    # fig.add_trace(smoothing)

    atr = df["atr"].iloc[-1]

    peaks_idx, _ = find_peaks(df["close_smooth"], distance=15, width=3, prominence=atr)
    troughs_idx, _ = find_peaks(
        -df["close_smooth"], distance=15, width=3, prominence=atr
    )

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

    moving_average = go.Scatter(
        x=df.index,
        y=df["MA"] * 1.62,
        mode="lines",
        name="Moving Average",
        line=dict(color="#2780d9", width=1),
    )

    moving_average2 = go.Scatter(
        x=df.index,
        y=df["MA"] * 0.62,
        mode="lines",
        name="Moving Average",
        line=dict(color="#2780d9", width=1),
    )

    ema1 = go.Scatter(
        x=df.index,
        y=df["EMA"] * 1.21,
        mode="lines",
        name="EMA",
        line=dict(color="#ffb22e", width=1),
    )

    ema2 = go.Scatter(
        x=df.index,
        y=df["EMA"] * 0.79,
        mode="lines",
        name="EMA",
        line=dict(color="#ffb22e", width=1),
    )

    fig.add_trace(moving_average)
    fig.add_trace(moving_average2)

    fig.add_trace(ema1)
    fig.add_trace(ema2)

    date_range = df.loc[df.index[-200] : df.index[-1]]
    max_value = round(float(date_range["High"].max()))
    min_value = round(float(date_range["Low"].min()))

    fig.update_layout(
        title="Bitcoin Price (USD)",
        title_font=dict(family="Century Gothic", size=18, color="#ffffff"),
        font=dict(family="Century Gothic", size=15, color="#ffffff"),
        # height=900,
        # width=1800,
        # plot_bgcolor="#000000",
        paper_bgcolor="#000000",
        font_color="#FFFFFF",
        spikedistance=1000,
        hovermode="x",
        dragmode="pan",
        autosize=True,
        showlegend=False,
        # scrollzoom=True,
        # responsive=True,
        xaxis=dict(
            tickfont=dict(size=14, color="#bdbdbd"),
            linecolor="#bdbdbd",
            showspikes=True,
            spikedash="dot",
            spikethickness=2,
            spikecolor="#999999",
            spikemode="across",
            showgrid=False,
            # fixedrange=True,
            rangeslider=dict(visible=False),
            # type="log",
            zeroline=False,
        ),
        yaxis=dict(
            tickfont=dict(size=14, color="#bdbdbd"),
            linecolor="#bdbdbd",
            showgrid=False,
            fixedrange=False,
            range=[min_value * 0.9, max_value * 1.1],
            # type="log",
            zeroline=False,
        ),
        margin=dict(l=100, r=100, t=100, b=100),
    )

    if n_clicks_2 is not None and n_clicks_2 % 2 == 1:
        fig.update_layout(
            xaxis=dict(
                range=[df.index[-200], df.index[-1]],
            )
        )
    else:
        fig.update_layout(
            xaxis=dict(
                range=[df.index[-200], df.index[-1]],
            ),
        )

    if n_clicks_1 is not None and n_clicks_1 % 2 == 1:
        fig.update_layout(
            plot_bgcolor="#000000",
            paper_bgcolor="#000000",
            title_font_color="#FFFFFF",
        )
    else:
        fig.update_layout(
            plot_bgcolor="#ffffff",
            paper_bgcolor="#ffffff",
            title_font_color="#000000",
        )

    fig["layout"]["uirevision"] = "something"
    return fig


if __name__ == "__main__":
    app.run_server(
        debug=False
    )  # if you want to activate debug mode, set it to True, this also adds the blue button

# If the browser always loads the same chart, you have to clear the cache of your browser.

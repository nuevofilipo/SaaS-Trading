import dash
from dash import dcc
from dash import html
import yfinance as yf
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


app = dash.Dash()

start_date = "2017-01-01"
end_date = "2023-01-01"
end_date1 = dt.datetime.now()

btc = yf.Ticker("BTC-USD")
hourly_data = btc.history(interval="1wk", start=start_date, end=end_date1)

df = pd.DataFrame(hourly_data)
# uf = df[["Close"]]

df["MA"] = ta.SMA(df["Close"], timeperiod=9)


# print(uf)


fig = go.Figure(
    data=[
        go.Candlestick(
            x=hourly_data.index,
            open=hourly_data["Open"],
            high=hourly_data["High"],
            low=hourly_data["Low"],
            close=hourly_data["Close"],
            increasing_line_color="#ffffff",
            decreasing_line_color="#ffffff",
        )
    ]
)

fig.update_layout(
    plot_bgcolor="#000000",
)

moving_average = go.Scatter(x=df.index, y=df["MA"], mode="lines", name="Moving Average")


fig.add_trace(moving_average)

app.layout = html.Div(
    [
        html.Button("Toggle Dark Mode", className="toggle-button", id="dark-mode-btn"),
        dcc.Graph(
            id="candlestick-chart",
            figure=fig,
            style={"height": "100vh", "width": "100vw"},
            config=dict({"scrollZoom": True}),
        ),
        dcc.Interval(
            id="interval-component", interval=10000, n_intervals=0  # in milliseconds
        ),
    ]
)


@app.callback(
    Output("candlestick-chart", "figure"),
    [Input("interval-component", "n_intervals")],
    [dash.dependencies.Input("dark-mode-btn", "n_clicks")],
)
def update_chart(n, n_clicks):
    end_date1 = dt.datetime.now()
    hourly_data = btc.history(interval="1wk", start=start_date, end=end_date1)
    df = pd.DataFrame(hourly_data)
    df["MA"] = ta.SMA(df["Close"], timeperiod=9)
    df["EMA"] = ta.EMA(df["Close"], timeperiod=12)

    df["atr"] = tan.atr(df["High"], df["Low"], df["Close"], length=1)
    df["atr"] = df.atr.rolling(window=30).mean()
    df["close_smooth"] = savgol_filter(df["Close"], 49, 5)

    fig = go.Figure(
        data=[
            go.Candlestick(
                x=hourly_data.index,
                open=hourly_data["Open"],
                high=hourly_data["High"],
                low=hourly_data["Low"],
                close=hourly_data["Close"],
                name="Bitcoin Price (USD)",
                increasing_line_color="#03fc94",
                decreasing_line_color="#fc032d",
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
            range=[df.index[-120], df.index[-1]],
            # fixedrange=True,
            rangeslider=dict(visible=False),
            # type="log",
        ),
        yaxis=dict(
            tickfont=dict(size=14, color="#bdbdbd"),
            linecolor="#bdbdbd",
            showgrid=False,
            fixedrange=False,
            type="log",
        ),
        margin=dict(l=100, r=100, t=100, b=100),
    )

    if n_clicks is not None and n_clicks % 2 == 1:
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
            yaxis=dict(
                # type="linear",
            ),
        )

    fig["layout"]["uirevision"] = "something"
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)

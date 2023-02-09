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

app = dash.Dash()

start_date = "2023-01-28"
end_date = "2023-01-01"
end_date1 = dt.datetime.now()

btc = yf.Ticker("BTC-USD")
hourly_data = btc.history(interval="1h", start=start_date, end=end_date1)

df = pd.DataFrame(hourly_data)
# uf = df[["Close"]]

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

app.layout = html.Div(
    [
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
    Output("candlestick-chart", "figure"), [Input("interval-component", "n_intervals")]
)
def update_chart(n):
    end_date1 = dt.datetime.now()
    hourly_data = btc.history(interval="1h", start=start_date, end=end_date1)
    df = pd.DataFrame(hourly_data)
    df["MA"] = ta.SMA(df["Close"], timeperiod=7)

    fig = go.Figure(
        data=[
            go.Candlestick(
                x=hourly_data.index,
                open=hourly_data["Open"],
                high=hourly_data["High"],
                low=hourly_data["Low"],
                close=hourly_data["Close"],
                name="Bitcoin Price (USD)",
            )
        ],
    )

    moving_average = go.Scatter(
        x=df.index,
        y=df["MA"],
        mode="lines",
        name="Moving Average",
        line=dict(color="#BCCCDC"),
    )

    fig.add_trace(moving_average)

    fig.update_layout(
        title="Bitcoin Price (USD)",
        title_font=dict(family="Century Gothic", size=18, color="#ffffff"),
        font=dict(family="Century Gothic", size=15, color="#ffffff"),
        # height=900,
        # width=1800,
        plot_bgcolor="#000000",
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
            range=[df.index[-200], df.index[-1]],
            # fixedrange=True,
            rangeslider=dict(visible=False),
        ),
        yaxis=dict(
            tickfont=dict(size=14, color="#bdbdbd"),
            linecolor="#bdbdbd",
            showgrid=False,
            fixedrange=False,
        ),
        margin=dict(l=100, r=100, t=100, b=100),
    )

    fig["layout"]["uirevision"] = "something"
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)

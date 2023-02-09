import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import datetime as dt


start_date = "2023-01-01"
end_date = "2023-01-01"
end_date1 = dt.datetime.now()

# Get the historical data for BTC
btc = yf.Ticker("BTC-USD")
data = btc.history(start=start_date, end=end_date1)

hourly_data = btc.history(interval="1h", start=start_date, end=end_date1)

df = pd.DataFrame(data)
# print(df)

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
fig.update_layout(
    title="Bitcoin Price (USD)",
    xaxis_title="Date",
    yaxis_title="Price",
    plot_bgcolor="#FFF",
    xaxis=dict(title="time", linecolor="#BCCCDC", showgrid=False),
)
fig.show()

# Convert the chart to a JSON object
# chart_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

# with open("chart.json", "w") as f:
#     json.dump(chart_json, f)

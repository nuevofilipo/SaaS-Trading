import plotly.graph_objects as go
import pandas_datareader as pdr
import datetime as dt

CRYPTO_NAME = "BTC-USD"


def get_data():
    ed = dt.datetime.now()
    sd = ed - dt.timedelta(days=365)
    start_date = [sd.year, sd.month, sd.day]

    end_date = [ed.year, ed.month, ed.day]

    data = pdr.get_data_yahoo(CRYPTO_NAME, start_date, end_date)
    return data


def main():
    crypto_data = get_data()

    graph = go.Figure(
        data=[
            go.Candlestick(
                x=crypto_data.index,
                open=pdr.to_numeric(crypto_data["Open"]),
                close=pdr.to_numeric(crypto_data["Close"]),
                high=pdr.to_numeric(crypto_data["High"]),
                low=pdr.to_numeric(crypto_data["Low"]),
            )
        ]
    )
    print(crypto_data)


if __name__ == "__main__":
    main()

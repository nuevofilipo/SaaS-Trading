import dash
from dash import html
import datetime as dt
from dash.dependencies import Input, Output
from dash import dcc

app = dash.Dash()

app.layout = html.Div(
    children=[
        html.H1(
            id="time-display",
            children=f'The current time is: {dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
        )
    ]
)


@app.callback(
    Output("time-display", "children"), [Input("interval-component", "n_intervals")]
)
def update_time(n):
    return f'The current time is: {dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'


app.layout = html.Div(
    children=[
        html.H1(
            id="time-display",
            children=f'The current time is: {dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
        ),
        dcc.Interval(
            id="interval-component", interval=1000, n_intervals=0  # in milliseconds
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)

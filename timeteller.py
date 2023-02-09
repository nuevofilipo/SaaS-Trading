import dash
from dash import html
import datetime as dt

app = dash.Dash()

app.layout = html.Div(
    children=[
        html.H1(
            children=f'The current time is: {dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
        )
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)

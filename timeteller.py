import dash
from dash import html
import datetime as dt
from dash import dcc

app = dash.Dash()

app.layout = html.Div(
    [
        html.Div("Example Div", style={"color": "blue", "fontSize": 14}),
        html.P("Example P", className="my-class", id="my-p-element"),
        html.Button(
            "Example Button",
            id="my-button",
            className="my-button",
        ),
    ],
)

if __name__ == "__main__":
    app.run_server(debug=True)

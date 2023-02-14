import dash
from dash import dcc
from dash import html
import plotly.graph_objs as go
import plotly.io as pio

app = dash.Dash(__name__)

# Create the figure with a light mode template
fig = go.Figure(
    data=go.Scatter(x=[1, 2, 3], y=[4, 5, 6]), layout=go.Layout(template="plotly_white")
)

app.layout = html.Div(
    [
        dcc.Graph(id="graph", figure=fig),
        html.Button("Toggle Dark Mode", id="dark-mode-btn"),
    ]
)


@app.callback(
    dash.dependencies.Output("graph", "figure"),
    [dash.dependencies.Input("dark-mode-btn", "n_clicks")],
    [dash.dependencies.State("graph", "figure")],
)
def toggle_dark_mode(n_clicks, fig):
    if n_clicks is not None and n_clicks % 2 == 1:
        # Update the template to a dark mode template
        fig = go.Figure(
            data=go.Scatter(x=[1, 2, 3], y=[4, 5, 6]),
            layout=go.Layout(template="plotly_white"),
        )
        fig.update_layout(template="plotly_dark")
    else:
        # Use the light mode template
        fig = go.Figure(
            data=go.Scatter(x=[1, 2, 3], y=[4, 5, 6]),
            layout=go.Layout(template="plotly_white"),
        )
        fig.update_layout(template="plotly_white")

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)

import plotly.graph_objs as go

# Sample data
x = [1, 2, 3, 4, 5]
y = [10, 100, 1000, 10000, 100000]

# Create a scatter plot
fig = go.Figure(data=go.Scatter(x=x, y=y))

# Add a button to change the colorway
fig.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            direction="left",
            buttons=list(
                [
                    dict(
                        args=["plot_bgcolor", "#4287f5"],
                        label="dark",
                        method="relayout",
                    ),
                    dict(
                        args=["plot_bgcolor", "#ffffff"],
                        label="light",
                        method="relayout",
                    ),
                ]
            ),
        ),
    ]
)

# Show the chart
fig.show()

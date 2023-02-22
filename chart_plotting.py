import plotly.graph_objs as go

# Create a scatter plot
fig = go.Figure(go.Scatter(x=[1, 2, 3], y=[4, 5, 6]))

# Change the color of the x axis line to red
fig.update_xaxes(line_color="red")

# Change the color of the y axis line to blue
fig.update_yaxes(line_color="blue")

# Show the plot
fig.show()

import dash
import plotly.graph_objects as go
from dash import dcc
from dash import html

import pandas as pd
from binance.spot import Spot as Client

app = dash.Dash()

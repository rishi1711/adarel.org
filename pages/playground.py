from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd

browse_file_component = html.Div([
    dcc.Upload(
        id="upload-data",
        children = html.Div([
            html.Strong("Step1: "), "Update files by either ", html.U("drag and drop "), "or ", 
            html.A("click here!", style={'fontWeight': 'bolder', 'textDecoration': 'underline'})]
        ),
        accept=".csv, .xlsx"
    )

])

page = html.Div([
    html.H2("Welcom to user playground!", style={"fontWeight": "bolder"}),
    html.Div("This is where you can use your own dataset to test our data."),
    browse_file_component,

])
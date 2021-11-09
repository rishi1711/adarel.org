from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
#pd.options.plotting.backend = "plotly"
from numpy import genfromtxt
import plotly.graph_objects as go
import os
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def test():
    df = px.data.gapminder().query("country=='Canada'")
    fig = px.line(df, x="year", y="lifeExp", title='Life expectancy in Canada')
    return fig


home_page = html.Div([
    dbc.Container(
    [
        ### Archive: these are from the old results
        # dbc.Row([
        #     dcc.Link('Go to Data 1', href='/data1'),
        # ]),
        # dbc.Row([
        #     dcc.Link('Go to Data 2', href='/data2'),
        # ]),
        # dbc.Row([
        #     dcc.Link('Go to Data 3', href='/data3'),
        # ]),
        # dbc.Row([
        #     dcc.Link('Go to Data 4', href='/data4'),
        # ]),

        dbc.Row([
            dcc.Link('Go to Data set 1', href='/2021data_1'),
        ]),
        dbc.Row([
            dcc.Link('Go to Data set 2', href='/2021data_2'),
        ]),
        dbc.Row([
            dcc.Link('Go to Data set 3', href='/2021data_3'),
        ]),
        dbc.Row([
            dcc.Link('Go to Data set SEC', href='/2021data_sec'),
        ]),
        dbc.Row([
            dcc.Link('Adarel on Live Data', href='/live'),
        ])
    ]),
])
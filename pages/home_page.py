import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
#pd.options.plotting.backend = "plotly"
from numpy import genfromtxt

import os
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def test():
    df = px.data.gapminder().query("country=='Canada'")
    fig = px.line(df, x="year", y="lifeExp", title='Life expectancy in Canada')
    return fig

def data1():
    lol = pd.read_csv("raw_data/ds1_truth.csv") 
   # my_data = genfromtxt('../raw_data/ds1_truth.csv', delimiter=',')
    print(lol)
    fig = lol.plot()

    return fig

home_page = html.Div([
    dbc.Container(
    [
        dbc.Row([
            dcc.Link('Go to Data 1', href='/data1'),
        ]),
        dbc.Row([
            dcc.Link('Go to Data 2', href='/data2'),
        ]),
        dbc.Row([
            dcc.Link('Go to Data 3', href='/data3'),
        ])
    ]),
    dbc.Container(
    [
        dbc.Row([
            html.Div([
                dcc.Graph(figure=data1())
            ])

        ])
    ])
])
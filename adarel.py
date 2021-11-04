# -*- coding: utf-8 -*-
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

from navbar import navbar


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = html.Div(children=[
    navbar,
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web applicatffion framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])
server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)

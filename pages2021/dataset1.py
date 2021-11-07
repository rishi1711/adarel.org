from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd

# from pages2021.datapaths import DATA, SHEET_NUM
import pages2021.figgenerator as fgen



dataset_1_page = html.Div([
    dbc.Row([
        dbc.Col(
            html.H3('Emprical Study 1'),
            width = 4,
        ),
        dbc.Col( 
            html.A("Download this data set", href="/static/2021_DataSet1.xlsx"),
            width = 4,
        ),
    ], justify='between',
    ),

    dbc.Row([
        dbc.Col([ 
            html.Div([
                dcc.Graph(figure= fgen.get_fig('DataSet1'))
            ])
        ])
    ])
])
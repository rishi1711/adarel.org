import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import plotly.graph_objects as go
import pandas as pd

live_page = html.Div([
    dbc.Row([
        dbc.Col(
            html.H3("Live data from on of our servers."),
            width=5,
        )
    ],
    justify="between",),

    

    dbc.Row([
        dbc.Col([
        html.Div([
            html.P(";p;")
            ])
        ])
    ])
])

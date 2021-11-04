from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd

def data():
    lol = pd.read_csv("raw_data/ds3.csv") 
    fig = go.Figure()
    plots=['truth_values','lstm','gaussian','adarel','sarima','svr','rf']
    for plot in plots:
        fig.add_trace(go.Scatter(x=[*range(1, len(lol[plot].to_numpy()))],
                    y=lol[plot].to_numpy(),
                    mode='lines',
                    name=plot))
    return fig

data3 = html.Div([
    dbc.Row([
        dbc.Col(
            html.H3("Empirical Study 3 Plots"),
            width=4,
        ),
        dbc.Col(
            html.A("Raw_Data Download", href="/static/ds3.csv"),
            width=4,
        )
    ],
    justify="between",),

    dbc.Row([
        dbc.Col([
        html.Div([
            dcc.Graph(figure=data())
            ])
        ])
    ])
])
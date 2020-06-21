import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import plotly.graph_objects as go
import pandas as pd
import tool.fetchData as fetchData
from statsmodels.tsa.api import ExponentialSmoothing, SimpleExpSmoothing, Holt
import matplotlib.pyplot as plt
import numpy as np
from dateutil.parser import parse

def gen_plot_forecast():
    es_conn = fetchData.elasticSearch(url="https://kibanaadmin:kibana@kf6-stage.ikit.org/es/_search")
    df = es_conn.get_nginx_reliability(interval='1h')
    df = df.sort_values('buckets', ascending=True)
    data_in_window = df.tail(1000)
    rel_data = data_in_window["reliability"].to_numpy()
    last_bucket = parse(data_in_window["buckets"].iloc[-1])
    if np.isnan(np.sum(rel_data)):
        print("NaN in data")
        exit(1)
    simple_exp_model = SimpleExpSmoothing(rel_data).fit(smoothing_level=.5)
    predicted_data = np.average(simple_exp_model.forecast(5))
    fitted_values = simple_exp_model.fittedvalues
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=range(1, len(rel_data)),
                    y=rel_data,
                    mode='lines',
                    name="Data in window"))
    fig.add_trace(go.Scatter(x=range(1, len(fitted_values)),
                    y=fitted_values,
                    mode='lines',
                    name="Previous Predictions"))
    return fig, predicted_data, last_bucket


fig, predicted_data, last_bucket = gen_plot_forecast()

live_page = html.Div([
    dbc.Row([
        dbc.Col(
            html.H3("Live data from one of our servers."),
            width=5,
        ),
        dbc.Col(html.Div([
            html.P("Next Prediction: " + str(round(predicted_data, 3))),
            html.P("Latest data on : "+last_bucket.strftime("%a %b %d %H:%M:%S %Y %Z"))
        ]),
            width=4,
        )
    ],
    justify="between",),

    dbc.Row([
        dbc.Col([
        html.Div([
            dcc.Graph(figure=fig)
            ])
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.Div([
                dcc.Input(
            id="es_url",
            type="text",
            placeholder="https://<userName>:<password>@<url>/es/_search",
        )
            ])
        ])
    ])
])

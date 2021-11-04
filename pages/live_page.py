from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

import plotly.graph_objects as go
import pandas as pd
import tool.fetchData as fetchData
from statsmodels.tsa.api import ExponentialSmoothing, SimpleExpSmoothing, Holt
import matplotlib.pyplot as plt
import numpy as np
from dateutil.parser import parse
import sys
sys.path.append("..")
from dash.dependencies import Input, Output
from app import app
from app import cache
import datetime

@cache.memoize(timeout=240)
def gen_plot_forecast():
    es_conn = fetchData.elasticSearch(url="https://kibanaadmin:kibana@kf6-stage.ikit.org/es/_search")
    df = es_conn.get_nginx_reliability(interval='1h')
    df = df.sort_values('buckets', ascending=True)
    data_in_window = df.tail(1000)
    rel_data = data_in_window["reliability"].to_numpy()
    date_data = data_in_window["buckets"].to_numpy()
    last_bucket = parse(data_in_window["buckets"].iloc[-1])
    if np.isnan(np.sum(rel_data)):
        print("NaN in data")
        exit(1)
    simple_exp_model = SimpleExpSmoothing(rel_data).fit(smoothing_level=.5)
    predicted_data = np.average(simple_exp_model.forecast(5))
    fitted_values = simple_exp_model.fittedvalues
    for idx, val in enumerate(fitted_values):
        if val < 0.5:
            fitted_values[idx] = 0.5
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=date_data,
                    y=rel_data,
                    mode='lines',
                    name="Observed Reliability"))
    fig.add_trace(go.Scatter(x=date_data,
                    y=fitted_values,
                    mode='lines',
                    name="Predicted Reliability"))
    print (datetime.datetime.now())
    sys.stdout.flush()
    tm = datetime.datetime.now()
    return fig, predicted_data, last_bucket, tm


#fig, predicted_data, last_bucket,tm = gen_plot_forecast()

live_page = html.Div([
    dcc.Interval(
            id='interval-component',
            interval=120*1000, # in milliseconds
            n_intervals=0
        ),
    dbc.Row([
        dbc.Col(
            html.H3("Live data from one of our servers."),
            width=5,
        ),
        dbc.Col(html.Div(id="next-prediction-div"),
            width=4,
        )
    ],
    justify="between",),

    dbc.Row([
        dbc.Col([
        html.Div(id="graph-div")
        ])
    ]),
    dbc.Row([
        dbc.Col([
        html.Div([
            html.H4("Custom ES Cluster Details"),
            html.P("The tool can connect to external ES cluster to fetch data.")
            ])
        ])
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                [
                    dbc.Label("Enter your ElasticSearch Cluster URL"),
                    dbc.Input(id="es_url",type="text",
                    placeholder="https://<userName>:<password>@<url>/es/_search",
                    )    
                ],
                [
                    dbc.Label("Enter your agent.hostname"),
                    dbc.Input(id="agent_hostname",type="text",
                    placeholder="agent-Hostname",
                    ),
                    dbc.FormText("Agent Hostname used as a filter to differenciate multiple agents sending logs to same ES Cluster")
                ],
                dbc.Button("Fetch Data", color="primary", id="refresh_data")
                ]), width=5)
    ]),
    dbc.Row([
        dbc.Col([
            html.Div([html.Div(id="out-all-types")])
        ])
    ])
])

@app.callback(
    Output("out-all-types", "children"),
    [Input("es_url", "value")]
)
def cb_render(vals):
    return vals

@app.callback(Output('graph-div', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_metrics_graph(n):
    fig, predicted_data, last_bucket,tm = gen_plot_forecast()
    return [
        dcc.Graph(figure=fig)
    ]


@app.callback(Output('next-prediction-div', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_metrics_prediction_div(n):
    fig, predicted_data, last_bucket,tm = gen_plot_forecast()
    return [
            html.P("Next Prediction: " + str(round(predicted_data, 3))),
            html.P("Latest data on : " + last_bucket.strftime("%a %b %d %H:%M:%S %Y %Z")),
            html.P("Updated on: " + tm.strftime("%a %b %d %H:%M:%S %Y %Z"))
        ]
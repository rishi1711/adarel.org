from dash import dcc
from dash import html, ctx
import dash
import dash_bootstrap_components as dbc
import plotly.express as px
import os


__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def test():
    df = px.data.gapminder().query("country=='Canada'")
    fig = px.line(df, x="year", y="lifeExp", title='Life expectancy in Canada')
    return fig


main_page = html.Div([dcc.Location(id = 'url_home', refresh=True),
    html.Div([
        html.H1("AdaRel"),
        html.P("a tool for reliability prediction")
        ], id="index-title"),
    dbc.Row([
        dbc.Col([
            html.H4("Welcome to AdaRel!"),
            html.Div("AdaRel is an online customisable reliability forecasting tool which accounts for dynamically changing bebaviour of modern web applications. It integrates with log aggrigator pipelines to continuously fetch data and predict near sighted reliability which serves as triggers for auto recovering systems. The tool has been validated on four emperical studies and this tool lets practioners and researchers visually experience the tool."),
            html.Div("AdaRel can connect to existing data sources or consume raw log files as input via file upload. Practisioners can select built-in strategies to predict reliablity. Researchers can further create bespoke strategies to extend and further tune predictions. We then visualize the results at the end. In practise this pipeline is extended in scaling workloads to serve as triggers to perform preventative actions avoiding low reliability.")
        ],class_name="main_page-card1",),

        dbc.Col([
            html.H5("See How It Works!"),
            dbc.Col([
                html.Div("See our Demo Prediction on Dataset:"),
                html.Div(""),
                html.Div("2021 Dataset1"),
                html.Div("2021 Dataset2"),
                html.Div("2021 Dataset3"),
                html.Div("2021 DatasetSEC"),
            ]),
            dbc.Col([
                html.Div(dcc.Link('Sign Up', href='/signup')),
                html.Div("for an account and test the prediction model on your dataset"),
            ])
        ], class_name="main_page-card2")
])
])
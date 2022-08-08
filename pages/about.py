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

#----------------------------------------------Front end of the About page-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
about = html.Div([dcc.Location(id = 'url_about', refresh=True),
        dbc.Col([
            html.H4("About"),
            html.Div("AdaRel is an online customisable reliability forecasting tool which accounts for dynamically changing bebaviour of modern web applications. It integrates with log aggrigator pipelines to continuously fetch data and predict near sighted reliability which serves as triggers for auto recovering systems. The tool has been validated on four emperical studies and this tool lets practioners and researchers visually experience the tool."),
            html.Div("AdaRel can connect to existing data sources or consume raw log files as input via file upload. Practisioners can select built-in strategies to predict reliablity. Researchers can further create bespoke strategies to extend and further tune predictions. We then visualize the results at the end. In practise this pipeline is extended in scaling workloads to serve as triggers to perform preventative actions avoiding low reliability.")
        ],class_name="about-card",),
])
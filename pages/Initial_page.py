from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import plotly.express as px
import os



__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def test():
    df = px.data.gapminder().query("country=='Canada'")
    fig = px.line(df, x="year", y="lifeExp", title='Life expectancy in Canada')
    return fig


first_page = html.Div([dcc.Location(id = 'url_new', refresh=True),
    dbc.Row([
        dbc.Col([
            html.H4("Try our Demo Data!"),
            html.Div("If you want to know how our tool work try working with our demo data!", className = "description"),
            html.Div([
                # dcc.Link(html.Button("Jump to Demo!"), href="/home_page", refresh=True),
                dbc.Button("Jump to Demo!", color="info", href="/home_page")
            ],style={"display": "flex", "flexFlow": "row-reverse nowrap"})
        ], width=4, class_name="notice-card")
    ]),

    dbc.Row([
        dbc.Col([
            html.H4("Have your own Data?"),
            html.Div("Do you have your own data that you want to try out? Then you come to the right place!", className = "description"),
            html.Div([
                dbc.Button("Sign Up Now!", color="info", href="/signup", )
            ],style={"display": "flex", "flexFlow": "row-reverse nowrap"})
        ], width=4, class_name="notice-card")
    ])
],)


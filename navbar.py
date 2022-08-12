import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from flask_login import current_user
from dash import html, ctx
from dash import dcc
from app import app
import dash

navbar = html.Div([dbc.NavbarSimple(
            id = 'nav_bar',
            children=[
                dbc.NavItem(dbc.NavLink("Home", href = "/", style={'color':'black'})),
                dbc.NavItem(dbc.NavLink("About", href = "/about", style={'color':'black'})),
                dbc.NavItem(dbc.NavLink("Demo", href = "/home_page", style={'color':'black'})),
                dbc.NavItem(dbc.NavLink(id = 'login', children = "Log In", href="/login", style={'color':'black'})),
                dbc.NavItem(dbc.NavLink(id = 'signup', children = "Sign Up", href="/signup" , style={'color':'black'})),
            ],
            brand="AdaRel",
            brand_href="/",
            color="light",
            class_name='navbar-custom'
    ),
    html.Div(id = 'temp')
])


@app.callback(
    Output('login', 'children'),
    Output('login', 'href'),
    Output('signup', 'children'),
    Output('signup', 'href'),
    Input('temp', 'children'),
)

def fill_navbar(data):
    if current_user.is_authenticated:
        return "My Workspace", '/first_page', "Log Out", '/logout'
    else:
        return "Log In", '/login', "Sign Up", '/signup'

import dash_bootstrap_components as dbc
from flask_login import current_user
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href = "/", style={'color':'black'})),
        dbc.NavItem(dbc.NavLink("About", href = "/about", style={'color':'black'})),
        dbc.NavItem(dbc.NavLink("Demo", href = "/home_page", style={'color':'black'})),
        dbc.NavItem(dbc.NavLink("Sign In", href="/login", style={'color':'black'})),
        dbc.NavItem(dbc.NavLink("Sign Up", href="/signup" , style={'color':'black'})),

    ],
    brand="AdaRel",
    brand_href="/",
    color="light",
    class_name='navbar-custom'
)

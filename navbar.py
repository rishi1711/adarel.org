import dash_bootstrap_components as dbc
from flask_login import current_user
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href = "/")),
        dbc.NavItem(dbc.NavLink("About", href = "/about")),
        dbc.NavItem(dbc.NavLink("Demo", href = "/home_page")),
        dbc.NavItem(dbc.NavLink("Sign In", href="/login")),
        dbc.NavItem(dbc.NavLink("Sign Up", href="/signup")),

    ],
    brand="AdaRel",
    brand_href="/",
    color="secondary",
    dark=True
)

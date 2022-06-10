import dash_bootstrap_components as dbc

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Sign In", href="/login")),
        dbc.NavItem(dbc.NavLink("Sign Up", href="/signup")),

    ],
    brand="AdaRel",
    brand_href="/",
    color="secondary",
    dark=True,
)
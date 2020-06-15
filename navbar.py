import dash_bootstrap_components as dbc

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Data 1", href="/data1")),
        dbc.NavItem(dbc.NavLink("Data 2", href="/data2")),
        dbc.NavItem(dbc.NavLink("Data 3", href="/data3")),  
    ],
    brand="AdaRel",
    brand_href="#",
    color="secondary",
    dark=True,
)
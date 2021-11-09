import dash_bootstrap_components as dbc

navbar = dbc.NavbarSimple(
    children=[
        # Archive: before 2021
        # dbc.NavItem(dbc.NavLink("Data 1", href="/data1")),
        # dbc.NavItem(dbc.NavLink("Data 2", href="/data2")),
        # dbc.NavItem(dbc.NavLink("Data 3", href="/data3")),
        # dbc.NavItem(dbc.NavLink("Data 4", href="/data4")),
        # dbc.NavItem(dbc.NavLink("Live Data", href="/live")),  
        dbc.NavItem(dbc.NavLink("Data 1", href="/2021data_1")),
        dbc.NavItem(dbc.NavLink("Data 2", href="/2021data_2")),
        dbc.NavItem(dbc.NavLink("Data 3", href="/2021data_3")),
        dbc.NavItem(dbc.NavLink("Data SEC", href="/2021data_sec")),
        dbc.NavItem(dbc.NavLink("Live Data", href="/live")),  
    ],
    brand="AdaRel",
    brand_href="/",
    color="secondary",
    dark=True,
)
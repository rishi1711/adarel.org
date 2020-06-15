import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


data3 = html.Div([
    dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(html.Div("One   d3  mns")),
                dbc.Col(html.Div("One of three columns")),
                dbc.Col(html.Div("One of three columns")),
            ],
            align="start",
        ),
    ]),
    dcc.Link('Go to Data 1', href='/data1')
])
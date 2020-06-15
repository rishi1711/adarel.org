import dash_core_components as dcc

import dash_html_components as html
from dash.dependencies import Input, Output
from navbar import navbar
from app import app
from pages.home_page import home_page
from pages.data1 import data1
from pages.data2 import data2
from pages.data3 import data3
import callbacks

app.layout = html.Div(children=[
    navbar,
    html.H1(children='Hello Dash'),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def router(pathname):
    if pathname == '/':
        return home_page
    elif pathname == '/data1':
        return data1
    elif pathname == '/data2':
        return data2
    elif pathname == '/data3':
        return data3
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)
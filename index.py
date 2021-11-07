from dash import dcc
from waitress import serve
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from navbar import navbar
from app import app
from pages.home_page import home_page
from pages.data1 import data1
from pages.data2 import data2
from pages.data3 import data3
from pages.data4 import data4
from pages.live_page import live_page

from pages2021.dataset1 import dataset_1_page

import callbacks
import serve_static
import os
app.title="AdaRel"
def serve_layout():

    return html.Div(children=[
    navbar,
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("AdaRel tool for reliability prediction"),width={"size": 8, "offset": 3},)
        ]),
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content')
    ]),
    
    ])
app.layout = serve_layout
# making it an instance of function makes it update every load
# https://dash.plotly.com/live-updates
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
    elif pathname == '/data4':
        return data4
    elif pathname == '/live':
        return live_page
    elif pathname == '/2021data1':
        return dataset_1_page
    else:
        return '404'
if __name__ == '__main__':
    DEBUG = (os.getenv('DASH_DEBUG_MODE', 'False') == 'True')
    if DEBUG:
        app.run_server(debug=True, host='0.0.0.0') # Development 
    else:# prod
        serve(app.server, host="0.0.0.0", port="8050") 
        # remember to clear the cache-direcotry on startup in prod
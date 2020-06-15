import dash_core_components as dcc
from waitress import serve
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from navbar import navbar
from app import app
from pages.home_page import home_page
from pages.data1 import data1
from pages.data2 import data2
from pages.data3 import data3
import callbacks
import serve_static

app.layout = html.Div(children=[
    navbar,
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("AdaRel tool for reliability prediction"),width={"size": 8, "offset": 3},)
        ]),
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content')
    ]),
    
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
    serve(app.server, host="0.0.0.0", port="8080") # prod
    #app.run_server(debug=True) # Development 
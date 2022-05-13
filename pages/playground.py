from app import app
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd

import base64
import io
import os

browse_file_component = html.Div([
    dcc.Upload(
        id="upload-data",
        children = html.Div([
            html.Strong("Step1: "), "Update files by either ", html.U("drag and drop "), "or ", 
            html.A("click here!", style={'fontWeight': 'bolder', 'textDecoration': 'underline'}),
            html.Div(id="uploaded-file")
        ]),
        accept=".csv, .xlsx"
    )

])

page = html.Div([
    html.H2("Welcom to user playground!", style={"fontWeight": "bolder"}),
    html.Div("This is where you can use your own dataset to test our data."),
    browse_file_component,
])

@app.callback(
    Output("uploaded-file", "children"),
    Input("upload-data", "contents"),
    State('upload-data', "filename"),
    prevent_initial_call=True
)
def read_spreadsheet(content: str, file_name: str) -> pd.DataFrame:
    # modified from https://stackoverflow.com/questions/62097062/uploading-a-csv-to-plotly-dash-and-rendering-a-bar-plot-based-on-a-pandas-datafr
    _, ext = os.path.splitext(file_name)
    content_info, content_encoded = content.split(",")
    content_decoded = base64.b64decode(content_encoded)
    print(content_decoded)

    try:
        if ext == ".csv":
            df = pd.read_csv(io.StringIO(content_decoded.decode('utf-8')))
        elif ext == ".xlsx":
            df = pd.read_excel(io.BytesIO(content_decoded))
        else:
            pass
    except Exception as e:
        print(e)
        
    return file_name
from app import app
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd

import base64
import io
import os

AVAILABLE_MODELS = {
    "SVR": "SVR",
    "Random Forest": "Random Forest"
}

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

parameter_component = html.Div([
    html.Div([
        html.Strong("Step 2: "), "Select a model for analysis"
    ]),
    dcc.Dropdown(
        id="model-select", 
        options=[{"label": k, 'value': v} for k, v in AVAILABLE_MODELS.items()], 
        placeholder="select a model"),
])

page = html.Div([
    html.H2("Welcom to user playground!", style={"fontWeight": "bolder"}),
    html.Div("This is where you can use your own dataset to test our data."),
    browse_file_component,
    html.Div(id='params-comp-holder')
])

@app.callback(
    Output("uploaded-file", "children"),
    Output("params-comp-holder","children"),
    Input('upload-data', "filename"),
    prevent_initial_call=True
)
def read_spreadsheet(file_name: str) -> str:
    # modified from https://stackoverflow.com/questions/62097062/uploading-a-csv-to-plotly-dash-and-rendering-a-bar-plot-based-on-a-pandas-datafr       
    return file_name, parameter_component

def read_encoded_spreadsheet(raw_content: str, ext: str) -> pd.DataFrame:
    content_info, encoded_content = raw_content.split(",")
    decoded_content = base64.b64decode(encoded_content)
    assert ext in ['.csv', '.xlsx']

    if ext == ".csv":
        df = pd.read_csv(io.StringIO(decoded_content.decode('utf-8')))
    else:
        df = pd.read_excel(io.BytesIO(decoded_content))
    
    return df    
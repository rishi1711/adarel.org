from dash import dcc, dash_table
from dash import html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import os
import base64
from urllib.parse import quote as urlquote
from app import app
import getpass
from database.models import Uploaded_files_tbl
from database.models import Uploadedfiles
from database.models import engine
from flask_login import current_user
from flask import g
import sqlite3
import io
import json
import dash


logged_in_user = html.Div([
    dbc.Row([
        html.H1("Want to Upload your Custom Data Set!"),
        dcc.Upload(
            id="upload-data",
            children=html.Div(
                ["Drag and drop or click to select a file to upload."]
            ),
            style={
                "width": "100%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px",
            },
            #multiple=True,
        ),
        html.Ul(id="file-list"),
    ],),

    dbc.Row([
        #---------------------------------------First Dropdown(DataSet Selection)---------------------------------------#
        html.H4("Lets Get Started!"),
        dbc.Col([
            html.Div([
                dcc.Dropdown(
                    id = "Custom Data Selection",
                    options=[],
                    placeholder = "Select DataSet",
                    value = 'None'
                )
            ])
        ]),
        #---------------------------------------------------------------------------------------------------------------#
        
        dbc.Col([
            html.Div([
                    html.Button('Create Strategy', id = 'custom submit_id', n_clicks=0)
            ])
        ]),

    ],class_name="notice-card"),
    ])


@app.callback(
    Output(component_id='Custom Data Selection', component_property='options'),
    [Input('upload-data', 'children')]
)
def get_custom_datasets(filename):
    conn = sqlite3.connect("./database/data.sqlite")
    g.user = current_user.get_id()
    id = g.user
    datasets = pd.read_sql("""select file_id, filename from files where user_id = '{}'""".format(id), conn)
    datasets = datasets.values.tolist()
    datasets = [{'label' : i[1], 'value' : i[0]} for i in datasets]
    return datasets


@app.callback(
    Output("file-list", "children"),
    [Input('upload-data', 'filename'),
    Input('upload-data', 'contents')],
    prevent_initial_call=True
)
def update_output(filename,content):
    path = "/Users/patil24/adarel.org/data2021/"+filename

    content_type, content_string = content.split(',')
    decoded = base64.b64decode(content_string)
    if 'txt' in filename:
        data = content.encode("utf8").split(b";base64,")[1]
        with open(path, "wb") as fp:
            fp.write(base64.decodebytes(data))
    elif 'csv' in filename:
        # Assume that the user uploaded a CSV file
        df = pd.read_csv(
            io.StringIO(decoded.decode('utf-8')))
        df.to_csv (path, index = False, header=True)
    elif 'xls' in filename:
        # Assume that the user uploaded an excel file
        df = pd.read_excel(io.BytesIO(decoded))


    
    file_name=os.path.splitext(filename)[0]
    if file_name is not None and current_user.get_id() is not None and path is not None:
        ins = Uploaded_files_tbl.insert().values(user_id = current_user.get_id(), filepath = path, filename = file_name)
        conn = engine.connect()
        conn.execute(ins)
        conn.close()
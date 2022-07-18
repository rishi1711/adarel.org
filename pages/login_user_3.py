from dash import dcc, dash_table
from dash import html, ctx
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import os
import base64
from urllib.parse import quote as urlquote
from app import app
from database.models import Uploaded_files_tbl
from database.models import Uploadedfiles
from database.models import engine
from flask_login import current_user
from flask import g
import sqlite3
import io
import json
import dash
import numpy as np
from PredictionModels.SelectionModels import predictOnSelectedModel

login_user_3 = html.Div([dcc.Location(id = 'url_path_3', refresh=True),
    dbc.Row([
        html.H1("Upload Custom Data!"),
        dcc.Upload(
            id = "upload-custom-data",
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
        html.Ul(id="file-list1"),
    ],),

    dbc.Row([
        #---------------------------------------First Dropdown(DataSet Selection)---------------------------------------#
        html.H4(" Predict the Dataset"),
        dbc.Col([
            html.Div([
                dcc.Dropdown(
                    id = "Custom Data Selection",
                    options=[],
                    placeholder = "Select DataSet"
                )
            ])
        ]),
        #---------------------------------------------------------------------------------------------------------------#


        #---------------------------------------Second Dropdown(Strategy Selection)---------------------------------------#
        dbc.Col([
            html.Div([
                dcc.Dropdown(
                    id ="Custom Strategy Selection",
                    options=[],
                    placeholder = "Select Strategy",
                )
            ])
        ]),
        #----------------------------------------------------------------------------------------------------------------#

        dbc.Col([
            html.Div([
                    html.Button('Predict', id = 'custom submit_id', n_clicks=0),
            ])
        ]),
    ],class_name="notice-card"),
    ])




#---------------------------------Function to fetch the uploaded dataset and strategy from database-----------------------#
@app.callback(
    Output(component_id='Custom Data Selection', component_property='options'),
    Output(component_id='Custom Strategy Selection', component_property='options'),
    [Input('upload-custom-data', 'children')]
)
def get_custom_datasets(filename):
    conn = sqlite3.connect("./database/data.sqlite")
    g.user = current_user.get_id()
    id = g.user

    datasets = pd.read_sql("""select file_id, filename from files where user_id = '{}' and filetype = '{}'""".format(id, "Custom"), conn)
    datasets = datasets.values.tolist()
    datasets = [{'label' : i[1], 'value' : i[0]} for i in datasets]

    get_strategy = pd.read_sql("""select strategy_id, strategy_name from strategy where user_id = '{}'""".format(id), conn)
    get_strategy = get_strategy.values.tolist()
    get_strategy = [{'label' : i[1], 'value' : i[0]} for i in get_strategy]
    return datasets, get_strategy
#---------------------------------------------------------------------------------------------------------------------------#


@app.callback(
    Output('customdataset', 'data'),
    [Input('Custom Data Selection','value')],
    prevent_initial_callback = True
)
def store_custom_dataset(value):
    return value


@app.callback(
    Output('customstrategy', 'data'),
    [Input('Custom Strategy Selection','value')],
    prevent_initial_callback = True
)
def store_custom_strategy(value):
    return value

#--------------------------------------store the uploaded dataset path in the database and file in data2021 folder-----------------------------------------#
@app.callback(
    Output("file-list1", "children"),
    [Input('upload-custom-data', 'filename'),
    Input('upload-custom-data', 'contents')],
    prevent_initial_call=True
)
def update_custom_output(filename, content):
    path = os.getcwd()+"/data2021/"+filename

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
        ins = Uploaded_files_tbl.insert().values(user_id = current_user.get_id(), filepath = path, filetype = "Custom" ,filename = file_name)
        conn = engine.connect()
        conn.execute(ins)
        conn.close()
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------#

@app.callback(
    Output(component_id='url_path_3', component_property='pathname'),
    [Input('custom submit_id', 'n_clicks')],
    [State('customdataset', 'data'), 
    State('customstrategy', 'data'),
    State('trainingdataset', 'data')],
    prevent_initial_callback = True
)
def custom_redirection(n_clicks1, dataset, strategy, trainingdata):
    id = ctx.triggered_id
    if id == "custom submit_id":
        if current_user.is_authenticated:
            call_predictions(dataset, strategy)
            return '/2021data'
        else:
            pass
    else:
        pass


def call_predictions(dataset, strategy):
    conn = sqlite3.connect("./database/data.sqlite")
    df_dataset = pd.read_sql("""select filepath from files where file_id = '{}'""".format(dataset), conn)
    df_strategy = pd.read_sql("""select strategy_name, strategy_data from strategy where strategy_id = '{}'""".format(strategy), conn)
    datasetPath = df_dataset["filepath"].loc[0]
    strategyName = df_strategy["strategy_name"].loc[0]
    strategyData = df_strategy["strategy_data"].loc[0]
    json_val = json.loads(strategyData)
    predictOnSelectedModel(datasetPath, strategyName, json_val)
    

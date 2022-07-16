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
from statsmodels.tsa.holtwinters import SimpleExpSmoothing
import numpy as np
from PredictionModels.SelectionModels import predictOnSelectedModel

login_user_1 = html.Div([dcc.Location(id = 'url_path_1', refresh=True),
    dbc.Row([
        html.H1("Upload Training Data!"),
        dcc.Upload(
            # id="upload-data",
            id = "upload-training-data",
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
        html.H4("Train-Dataset"),
        dbc.Col([
            html.Div([
                dcc.Dropdown(
                    id = "Training Data Selection",
                    options=[],
                    placeholder = "Select Training DataSet"
                )
            ])
        ]),
        #---------------------------------------------------------------------------------------------------------------#


        #---------------------------------------Second Dropdown(Strategy Selection)---------------------------------------#
        dbc.Col([
            html.Div([
                dcc.Dropdown( 
                    id ="Training Strategy Selection",
                    options=[],
                    placeholder = "Select Strategy",
                )
            ])
        ]),
        #----------------------------------------------------------------------------------------------------------------#

        dbc.Col([
            html.Div([
                    html.Button('Train Data', id = 'training submit_id', n_clicks=0),
            ])
        ]),
    ],class_name="notice-card"),

    dbc.Row([

        dbc.Col([
            html.H4("Create your own strategy?"),
            html.Div([
                dbc.Button("Create Strategy!", color="info", id='create_strategy')
            ],style={"display": "flex", "flexFlow": "row-reverse nowrap"})
            
        ], width=5, class_name="notice-card")

    ], style={"padding" : "20px", "column-gap" : "30px"})
    ])




#---------------------------------Function to fetch the uploaded dataset and strategy from database-----------------------#
@app.callback(
    Output(component_id='Training Data Selection', component_property='options'),
    Output(component_id='Training Strategy Selection', component_property='options'),
    [Input('upload-training-data', 'children')]
)
def get_training_datasets(filename):
    conn = sqlite3.connect("./database/data.sqlite")
    g.user = current_user.get_id()
    id = g.user

    # datasets = pd.read_sql("""select file_id, filename from files where user_id and filetype= '{}'""".format(id, "Training"), conn)
    datasets = pd.read_sql("""select file_id, filename from files where user_id = '{}' and filetype = '{}'""".format(id, "Training"), conn)
    datasets = datasets.values.tolist()
    datasets = [{'label' : i[1], 'value' : i[0]} for i in datasets]

    get_strategy = pd.read_sql("""select strategy_id, strategy_name from strategy where user_id = '{}'""".format(id), conn)
    get_strategy = get_strategy.values.tolist()
    get_strategy = [{'label' : i[1], 'value' : i[0]} for i in get_strategy]
    return datasets, get_strategy
#---------------------------------------------------------------------------------------------------------------------------#


# @app.callback(
#     Output('trainingdataset', 'data'),
#     [Input('Training Data Selection','value')],
#     prevent_initial_callback = True
# )
# def store_training_dataset(value):
#     return value


# @app.callback(
#     Output('trainingstrategy', 'data'),
#     [Input('Training Strategy Selection','value')],
#     prevent_initial_callback = True
# )
# def store_training_strategy(value):
#     return value

#--------------------------------------store the uploaded dataset path in the database and file in data2021 folder-----------------------------------------#
@app.callback(
    Output("file-list", "children"),
    [Input('upload-training-data', 'filename'),
    Input('upload-training-data', 'contents')],
    prevent_initial_call=True
)
def update_training_output(filename,content):
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
        ins = Uploaded_files_tbl.insert().values(user_id = current_user.get_id(), filepath = path, filetype = "Training", filename = file_name)
        conn = engine.connect()
        conn.execute(ins)
        conn.close()
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------#

@app.callback(
    Output(component_id='url_path_1', component_property='pathname'),
    [Input('create_strategy', 'n_clicks'),
    Input('training submit_id', 'n_clicks')],
    [State('Training Data Selection', 'value'), 
    State('Training Strategy Selection', 'value')],
    prevent_initial_callback = True
)
def training_redirection(n_clicks1, n_clicks2, dataset, strategy):
    id = ctx.triggered_id
    if id == "create_strategy":
        if current_user.is_authenticated:
            return '/strategy'
        else:
            pass
    elif id == "training submit_id":
        if current_user.is_authenticated:
            call_predictions(dataset, strategy)
            return '/login_user_2'
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
    

from tkinter import HIDDEN
from dash.exceptions import PreventUpdate
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

from sqlalchemy import true
from app import app
from database.models import Uploaded_files_tbl
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
import plotly.express as px

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
        html.Ul(id="file-list_t"),
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
                    html.Div(id="loading_t", className="loader", hidden='HIDDEN'),
                    html.Div([
                        html.Div(id = "p1"),
                        html.Div(id = "p2"),
                    ]),
            ])
        ]),
    ],class_name="notice-card"),

    dbc.Row([html.Div(id = "barGraph")]),

    dbc.Row([

        dbc.Col([
            html.H4("Create your own strategy?"),
            html.Div([
                dbc.Button("Create Strategy!", color="info", id='create_strategy')
            ],style={"display": "flex", "flexFlow": "row-reverse nowrap"})
            
        ], width=5, class_name="notice-card")

    ], style={"padding" : "20px", "column-gap" : "30px"}),

    dbc.Row([
        html.H1("Upload Test Data!"),
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
        html.Ul(id="file-list_c"),
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

        dbc.Col([
            html.Div([
                    html.Button('Predict', id = 'custom submit_id', n_clicks=0),
                    html.Div(id="loading_c", className="loader", hidden='HIDDEN')
            ])
        ]),
    ],class_name="notice-card"),
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

#--------------------------------------store the uploaded dataset path in the database and file in data2021 folder-----------------------------------------#
@app.callback(
    Output("file-list_t", "children"),
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



#---------------------------------Function to fetch the uploaded dataset and strategy from database-----------------------#
@app.callback(
    Output(component_id='Custom Data Selection', component_property='options'),
    [Input('upload-custom-data', 'children')]
)
def get_custom_datasets(filename):
    conn = sqlite3.connect("./database/data.sqlite")
    g.user = current_user.get_id()
    id = g.user

    datasets = pd.read_sql("""select file_id, filename from files where user_id = '{}' and filetype = '{}'""".format(id, "Custom"), conn)
    datasets = datasets.values.tolist()
    datasets = [{'label' : i[1], 'value' : i[0]} for i in datasets]
    return datasets
#---------------------------------------------------------------------------------------------------------------------------#


#--------------------------------------store the uploaded dataset path in the database and file in data2021 folder-----------------------------------------#
@app.callback(
    Output("file-list_c", "children"),
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

# @app.callback(
#     Output('loading_t', 'hidden'),
#     Input('training submit_id', 'n_clicks'),
#     Input('p1', 'hidden'),
#     prevent_initial_callback = True
# )
# def showLoader1(nclicks, value):
#     id = ctx.triggered_id
#     if id=='training submit_id':
#         if current_user.is_authenticated:
#             if nclicks == 0:
#                 return True
#             else:
#                 return False 
#         else:
#             pass
#     elif id=='p1':
#         if current_user.is_authenticated:
#             if value == False:
#                 return True
#             else:
#                 return False
#         else:
#             pass
#     else:
#         pass


@app.callback(
    Output('loading_c', 'hidden'),
    Input('custom submit_id', 'n_clicks'),
    prevent_initial_callback = True
)
def showLoader2(nclicks):
    if nclicks==0:
        return True
    else:
        return False 

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------#
@app.callback(
    Output('url_path_1', 'pathname'),
    Input('create_strategy', 'n_clicks'),
    Input('training submit_id', 'n_clicks'),
    Input('custom submit_id', 'n_clicks'),
    State('trainingdata', 'data'),
    State('sstrategy', 'data'),
    State('testingdata', 'data'),
    prevent_initial_callback = True
)
def training_redirection(n_clicks1, n_clicks2, n_clicks3, t_dataset, strategy, c_dataset):
    id = ctx.triggered_id
    if id == "create_strategy":
        if current_user.is_authenticated:
            return '/strategy', None, None
        else:
            pass
    elif id == "custom submit_id":
        if current_user.is_authenticated:
            call_predictions(t_dataset, c_dataset, strategy, "testing")
            return '/2021data'
        else:
            pass
    raise PreventUpdate


def call_predictions(train_dataset_id, test_dataset_id, strategy_id, type):
    conn = sqlite3.connect("./database/data.sqlite")
    df_dataset = pd.read_sql("""select filepath from files where file_id = '{}'""".format(train_dataset_id), conn)
    df_strategy = pd.read_sql("""select strategy_name, strategy_data from strategy where strategy_id = '{}'""".format(strategy_id), conn)
    datasetPath_train = df_dataset["filepath"].loc[0]
    if type == "testing":
        df_dataset_test = pd.read_sql("""select filepath from files where file_id = '{}'""".format(test_dataset_id), conn)
        datasetPath_test = df_dataset_test["filepath"].loc[0]
    else:
        datasetPath_test = None
    strategyName = df_strategy["strategy_name"].loc[0]
    strategyData = df_strategy["strategy_data"].loc[0]
    json_val = json.loads(strategyData)
    errors = predictOnSelectedModel(datasetPath_train, datasetPath_test, strategyName, json_val, type)
    return errors


@app.callback(
    Output('trainingdata', 'data'),
    Input('Training Data Selection', 'value'),
    prevent_initial_callback = True
)
def store_trainingdata(value):
    return value

@app.callback(
    Output('testingdata', 'data'),
    Input('Custom Data Selection', 'value'),
    prevent_initial_callback = True
)
def store_testingdata(value):
    return value

@app.callback(
    Output('sstrategy', 'data'),
    Input('Training Strategy Selection', 'value'),
    prevent_initial_callback = True
)
def store_strategy(value):
    return value

@app.callback(
    Output('bar_graph_values', 'data'),Output('mae_measure', 'data'), Output('rmse_measure', 'data'), 
    Input('training submit_id', 'n_clicks'),
    [State('trainingdata', 'data'),
    State('sstrategy', 'data'),
    State('testingdata', 'data')],
    prevent_initial_callback = True
)
def get_error_values(nclicks, t_dataset, strategy, c_dataset):
    if nclicks>0:
        if current_user.is_authenticated:
            errors = call_predictions(t_dataset, c_dataset, strategy, "training")
            return errors[2], errors[0], errors[1]
        else:
            pass
    else:
        pass
    return dash.no_update

@app.callback(
    [Output('p1','hidden'),Output('p2','hidden'),Output('barGraph','hidden'),Output('p1', 'children'), Output('p2', 'children'), Output('barGraph','children')],
    [Input('mae_measure', 'data'), Input('rmse_measure', 'data'),Input('bar_graph_values', 'data')],
    prevent_initial_callback = True
)
def show_error(data1,data2,data3):
    e1 = "Mean Average Error:   " + str('{0:.6g}'.format(data1))
    e2 = "Root Mean Squared Error:   " + str('{0:.6g}'.format(data2))
    x = ['0-0.0005', '0.0005-0.001', '0.001-0.005', '0.005-0.01', '0.01-0.05', '0.05-0.1', '0.1-0.5', '0.5-1','>=1']      
    df = px.data.tips()
    fig = px.bar(x=x, y=data3, labels={'x':'intervals', 'y' : 'count'}, title="Summary")
    fig.update_xaxes(type='category')
    
    final = dcc.Graph(figure = fig)
    if data1 is None:
        return 'HIDDEN','HIDDEN', 'HIDDEN' ,e1,e2,final
    else:
        return False,False,False,e1,e2,final

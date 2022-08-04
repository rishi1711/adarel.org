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
from app import app
from database.models import Uploaded_files_tbl
from database.models import engine
from flask_login import current_user
from flask import g
import sqlite3
import io
import json
import dash
import tool.figgenerator as fgen
from statsmodels.tsa.holtwinters import SimpleExpSmoothing
import numpy as np
from PredictionModels.SelectionModels import predictOnSelectedModel

login_user_1 = html.Div([dcc.Location(id = 'url_path_1', refresh=True),
    dbc.Row([
            html.H1("My Workspace > Make New Predictions", style={'text-align' : 'left', 'color' : '#686868', 'font-size' : '3rem', 'padding-bottom' : '', 'padding-top' : '20px'}),
            html.Div("In your workspace, you are able to experiment diffrent prediction strategies." ,style={'text-align' : 'left', 'color' : '#686868', 'font-size' : ''}),
            html.Div("To begin, try the combinations of data and strategies using a small subset of dataset. Later in step 3, the same strategy can be applied to entire dataset.", style={'text-align' : 'left', 'color' : '#686868', 'font-size' : '', 'padding-bottom' : '1rem'}),
           ]),
dbc.Row([
    dbc.Row([
        html.H4("Step 1: Select Training Data"),
        html.Div("You can either select the data from your uploaded data pool, or upload a new one here.",style={'text-align' : 'left', 'color' : '#686868', 'padding-bottom':'10px'}),
        dbc.Col([
            html.Div([
                dcc.Dropdown(
                    id = "Training Data Selection",
                    options=[],
                    placeholder = "Select Training DataSet"
                )
            ])
        ]),
        dbc.Col([
            html.Div([
                html.Button('Upload Data', id = 'upload_dataset', n_clicks=0, style= {'background-color' : '#6E6E6E', 'color' : 'white', 'border' : 'none', 'border-radius' : '5px', 'display' : 'inline-block', 'height' : '30px', 'width' : '200px', 'margin-left' : '200px'}),
            ]),
        ],class_name = 'button__style__uploaddata'),
        dbc.Col([
            html.Div([
                html.Button('Connect to ElasticSearch', id = 'ElasticSearchbutton', n_clicks=0, style= {'background-color' : '#6E6E6E', 'color' : 'white', 'border' : 'none', 'border-radius' : '5px', 'display' : 'inline-block', 'height' : '30px', 'width' : '200px', 'margin-left' : '200px'}),
            ]),
        ],class_name = 'button__style__searchbutton'),
    ],style = {'padding-bottom':'3rem', 'padding-top':'1rem'}),

    dbc.Row([
        html.H4("Step 2: Select a Prediction Strategy"),
        html.Div("A Strategy is the collection of prediction models and its parameters.",style={'text-align' : 'left', 'color' : '#686868', 'font-size' : ''}),
        html.Div("Either select an existing strategy or create a new one.",style={'text-align' : 'left', 'color' : '#686868', 'font-size' : '','padding-bottom':'10px'}),
        dbc.Col([
            html.Div([
                dcc.Dropdown( 
                    id ="Training Strategy Selection",
                    options=[],
                    placeholder = "Select Strategy",
                )
            ])
        ]),

        dbc.Col([
            html.Div(id='temporary_div'),
        ]),

        dbc.Col([
            html.Div([
                html.Button('Create a New Strategy', id = 'create_strategy', n_clicks=0, style= {'background-color' : '#6E6E6E', 'color' : 'white', 'border' : 'none', 'border-radius' : '5px', 'display' : 'inline-block', 'height' : '30px', 'width' : '200px', 'margin-left' : '200px'}),
            ]),
        ]),
    ],style = {'padding-bottom':'3rem'}),

    dbc.Row([
        dbc.Row([
            html.H3(id = 'strategy-title'),
        ], style= {'padding-bottom':'0.1rem', 'padding-top':'1rem'}),
        dbc.Row([
            dbc.Col([
                html.Div(id = 'base-model', style={'text-align' : 'left', 'color' : '#686868'}),
                html.Div(id = 'param', style={'text-align' : 'left', 'color' : '#686868'}),
            ]),
            dbc.Col([
                html.Div("Based on the selected base model, the strategy should account for high seasonal variations. Refer below for more information.",style={'text-align' : 'left', 'color' : '#686868'} ),
            ]),
        ], style= {'padding-bottom':'2rem', 'padding-top':'1rem'}),
        dbc.Row([
            html.Button('Get a Quick Summary of Training Data', id = 'training submit_id', n_clicks=0, style= {'background-color' : '#714FFF', 'color' : 'white', 'border' : 'none', 'border-radius' : '5px', 'display' : 'inline-block', 'height' : '35px', 'width' : '400px',  'margin-left' : '880px'}),
        ]),
    ], class_name='first_row'),

    dbc.Row([
        html.Div(id ='training_summary'),
    ]),

    # dbc.Row([
    #     html.Div("", style={ 'background-color' : '#F8F8F8'}),
    # ]),

    # dbc.Row([
    #     dbc.Row([
    #         html.H3("Training Result Summary"),
    #     ], style= {'padding-bottom':'0.1rem', 'padding-top':'1rem'}),
    #     dbc.Row([
    #         dbc.Col([
    #             html.Div(id = 'p1', style={'text-align' : 'left', 'color' : '#686868'}),
    #             html.Div(id = 'p2', style={'text-align' : 'left', 'color' : '#686868'}),
    #         ]),
    #         dbc.Col([
    #             html.Div(id = 'get_graph'),
    #         ]),
    #     ], style= {'padding-bottom':'2rem', 'padding-top':'1rem'}),
    # ], class_name='second_row'),

    dbc.Row([
        html.Div(id ='file-list'),
    ]),
    dbc.Row([
        html.H4("Step 3: Proceed to Predict!"),
        html.Div("Strategy Selected in Step-1 is used here for prediction.",style={'text-align' : 'left', 'color' : '#686868', 'font-size' : '','padding-bottom':'10px'}),
        dbc.Col([
            html.Div([
                dcc.Dropdown(
                    id = "Custom Data Selection",
                    options=[],
                    placeholder = "Select DataSet"
                ),
            ]),
        ]),
        dbc.Col([
            html.Div([
                    html.Button('Predict Entire Dataset', id = 'custom submit_id', n_clicks=0, style= {'background-color' : '#714FFF', 'color' : 'white', 'border' : 'none', 'border-radius' : '5px', 'display' : 'inline-block', 'height' : '35px', 'width' : '250px',  'margin-left' : '440px' }),
                    html.Div(id="loading_c", className="loader", hidden='HIDDEN')
            ]),
        ]),
    ],style = {'padding-top':'1rem', 'padding-bottom':'2rem'}),
], class_name = 'page-view'),
],style = {'padding-bottom':'2rem'})




#---------------------------------Function to fetch the uploaded dataset and strategy from database-----------------------#
@app.callback(
    Output(component_id='Training Data Selection', component_property='options'),
    Output(component_id='Training Strategy Selection', component_property='options'),
    Output(component_id='Custom Data Selection', component_property='options'),
    [Input('file-list', 'children')],
    prevent_initial_callback = True
)
def get_training_datasets(filename):
    conn = sqlite3.connect("./database/data.sqlite")
    g.user = current_user.get_id()
    id = g.user

    training_datasets = pd.read_sql("""select file_id, filename from files where user_id = '{}' and filetype = '{}'""".format(id, "Training"), conn)
    training_datasets = training_datasets.values.tolist()
    training_datasets = [{'label' : i[1], 'value' : i[0]} for i in training_datasets]

    get_strategy = pd.read_sql("""select strategy_id, strategy_name from strategy where user_id = '{}'""".format(id), conn)
    get_strategy = get_strategy.values.tolist()
    get_strategy = [{'label' : i[1], 'value' : i[0]} for i in get_strategy]

    testing_datasets = pd.read_sql("""select file_id, filename from files where user_id = '{}' and filetype = '{}'""".format(id, "Testing"), conn)
    testing_datasets = testing_datasets.values.tolist()
    testing_datasets = [{'label' : i[1], 'value' : i[0]} for i in testing_datasets] 

    return training_datasets, get_strategy, testing_datasets
#---------------------------------------------------------------------------------------------------------------------------#

# @app.callback(
#     Output('loading_c', 'hidden'),
#     Input('custom submit_id', 'n_clicks'),
#     prevent_initial_callback = True
# )
# def showLoader2(nclicks):
#     if nclicks==0:
#         return True
#     else:
#         return False 

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------#
@app.callback(
    Output('url_path_1', 'pathname'),
    Input('create_strategy', 'n_clicks'),
    Input('custom submit_id', 'n_clicks'),
    Input('upload_dataset', 'n_clicks'),
    State('trainingdata', 'data'),
    State('sstrategy', 'data'),
    State('testingdata', 'data'),
    prevent_initial_callback = True
)
def training_redirection(n_clicks1, n_clicks2, n_clicks3, t_dataset, strategy, c_dataset):
    id = ctx.triggered_id
    if id == "upload_dataset":
        if current_user.is_authenticated:
            return '/create_data'
        else:
            pass
    elif id == "create_strategy":
        if current_user.is_authenticated:
            return '/strategy'
        else:
            pass
    elif id == "custom submit_id":
        if current_user.is_authenticated:
            call_predictions(t_dataset, c_dataset, strategy, "testing")
            return '/2021data'
        else:
            pass
    else:
        pass
    return dash.no_update


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

#-------------------------------------------------------dcc.store elements update------------------------------------------#
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
    Output('strategy-title', 'children'),
    Output('base-model', 'children'),
    Output('param', 'children'),
    Input('Training Strategy Selection', 'value'),
    prevent_initial_callback = True
)
def store_strategy(value):
    if value is not None:
        conn = sqlite3.connect("./database/data.sqlite")
        strategy = pd.read_sql("""select strategy_name, strategy_data from strategy where strategy_id = '{}'""".format(value), conn)
        strategy_title = strategy["strategy_name"].loc[0]
        strategy_info = strategy["strategy_data"].loc[0]
        info_dict = json.loads(strategy_info)
        base_model = "Base Model: " + str(info_dict.get('name'))
        del info_dict['name']
        param = "Parameter: " + str(info_dict)
        return value, strategy_title, base_model, param
    return dash.no_update
#----------------------------------------------------------------------------------------------------------------------------#


#-------------------------------------------------------rmse and mae value update--------------------------------------------#
@app.callback(
    Output('training_summary', 'children'),
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
            mae = "Mean Average Error:   " + str('{0:.6g}'.format(errors[0]))
            rmse = "Root Mean Squared Error:   " + str('{0:.6g}'.format(errors[1]))
            return get_training_summary(mae, rmse)
        else:
            pass
    else:
        pass
    return dash.no_update

def get_training_summary(mae=None, rmse=None) -> html.Div :
    itermediate = [
        dbc.Row([
            html.H3("Training Result Summary"),
        ], style= {'padding-bottom':'0.1rem', 'padding-top':'1rem'}),

        dbc.Row([
            dbc.Col([
                html.Div(mae),
                html.Div(rmse),
            ]),

            dbc.Col([
                html.Div([
                    dcc.Graph(figure= fgen.get_bar_graph()),
                ])
            ]),
        ]),
    ]

    html_div = html.Div(itermediate)
        
    return html_div
#----------------------------------------------------------------------------------------------------------------------------#

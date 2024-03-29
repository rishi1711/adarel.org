from cProfile import label
from optparse import Values
from re import I
from tkinter import HIDDEN
from turtle import width
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
from database.models import PreviousPredictions, Uploaded_files_tbl, previousPredictions_tbl
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
import plotly.express as px

#-------------------------------------Front end of the Make New Prediction Page---------------------------------------------------------------------------------------------------------------------------------------------------------------
login_user_1 = html.Div([dcc.Location(id = 'url_path_1', refresh=True),
                dbc.Row([
                    html.H1("My Workspace > Make New Predictions", 
                    style={'text-align' : 'left', 'color' : '#686868', 'font-size' : '3rem', 'padding-bottom' : '', 'padding-top' : '20px'}),
                    html.Div("In your workspace, you are able to experiment diffrent prediction strategies.",
                    style={'text-align' : 'left', 'color' : '#686868', 'font-size' : ''}),
                    html.Div("To begin, try the combinations of data and strategies using a small subset of dataset. Later in step 3, the same strategy can be applied to entire dataset.",
                    style={'text-align' : 'left', 'color' : '#686868', 'font-size' : '', 'padding-bottom' : '1rem'}),
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
                                # html.Button('Upload Data', id = 'upload_dataset', n_clicks=0, 
                                # style= {'background-color' : '#6E6E6E', 'color' : 'white', 'border' : 'none', 'border-radius' : '5px', 'display' : 'inline-block', 'height' : '30px', 'width' : '200px', 'margin-left' : '200px'}),
                            ]),
                        ],class_name = 'button__style__uploaddata'),
                        dbc.Col([
                            html.Div([
                                html.Button('Connect to ElasticSearch', id = 'ElasticSearchbutton', n_clicks=0, 
                                style= {'background-color' : '#6E6E6E', 'color' : 'white', 'border' : 'none', 'border-radius' : '5px', 'display' : 'inline-block', 'height' : '30px', 'width' : '200px', 'margin-left' : '200px'}),
                            ]),
                        ],class_name = 'button__style__searchbutton'),
                    ],style = {'padding-bottom':'3rem', 'padding-top':'1rem'}),

                    dbc.Row([
                        html.H4("Optional: Use Anomaly Detection?"),
                        html.Div("Anomaly Detection allows you to eliminate outliers and improve the performance of the prediction",style={'text-align' : 'left', 'color' : '#686868', 'font-size' : ''}),
                        dbc.Col([
                            dbc.Switch(
                                id = "switch",
                                label = "Anomaly Detection off",
                                value=False
                            ),
                        ]),
                    ]),
                    
                    dbc.Collapse(
                        dbc.Card(
                            dbc.CardBody([
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Row([
                                            dbc.Col([
                                                html.H6(["Observation Window"]),
                                            ]),
                                            dbc.Col([
                                                html.Abbr("?",title = "The observation window determines the length of cycle, and the window size where the number of samples will be performed anomaly detection on."),
                                            ]),    
                                        ]),
                                        dbc.Row([
                                            dbc.Col([
                                                dbc.Input(
                                                    id = "observation_window",
                                                    value = 24,
                                                ),
                                            ]),
                                            dbc.Col([
                                                dcc.Dropdown(id = "o_dropdown",
                                                options=['Minutes', 'Hours', 'Days', 'Weeks'],
                                                value = 'Hours'
                                                )                          
                                             ])    
                                        ]),
                                    ]),
                                    dbc.Col([
                                        dbc.Row([
                                        dbc.Col([
                                            html.H6(["Anomaly Window"]),
                                        ]),
                                        dbc.Col([
                                            html.Abbr("?",title = "The number of consecutive anamoly points to trigger trend change."),
                                        ]),
                                        ]),
                                        dbc.Row([
                                            dbc.Col([
                                                dbc.Input(
                                                    id = "anomly_window",
                                                    value = 3,
                                                ),
                                            ]),
                                            dbc.Col([
                                                dcc.Dropdown(id = "a_dropdown",
                                                options=['Minutes', 'Hours', 'Days', 'Weeks'],
                                                value = 'Hours'
                                                )
                                            ])                           
                                        ])
                                    ]),
        
                                    dbc.Col([
                                        dbc.Row([
                                        dbc.Col([
                                            html.H6(["Threshold"]),
                                        ]),
                                        dbc.Col([
                                            html.Abbr("?",title = "The coefficient. If the error of the current prediction is larger than this number times the average error, thecurrent point will be marked as anomaly as well."),
                                        ]),
                                        ]),
                                            dcc.Input(
                                                id = "thresold",
                                                value = 2,
                                        ),                     
                                    ])
                                ], style = {'padding-bottom':'1rem'}),
                                dbc.Row([
                                    html.H3("Anomaly Detection Method:")
                                ]),
                                dbc.Row([
                                    dbc.Col([
                                        dcc.Dropdown(
                                            id= "detection_method",
                                            placeholder="Select Detection method",
                                            options=["CIAnomaly"],
                                            value = "CIAnomaly"
                                        )
                                    ]),
                                    dbc.Col([
                                        html.Label("Z-value : "),
                                        dcc.Input(
                                            id="z-value",
                                            value=1.96,
                                            style={'border-color' : '#D3D3D3', 'border-width' : '0.025px', 'border-radius' : '5px', 'height' : '34px', 'width' : '11.5rem'}
                                        )
                                    ], style = {'padding-left':'20rem'}),                           
                                ]),
                                dbc.Row([
                                    dbc.Col([

                                    ]),

                                    dbc.Col([
                                        html.Div([
                                            html.Button('Confirm',id = "anomaly_confirm",
                                                style= {'background-color' : '#0000ff', 'color' : 'white', 'border' : 'none', 'border-radius' : '5px', 'display' : 'inline-block', 'height' : '30px', 'width' : '100px', 'margin-left' : '250px'}),
                                        ]),
                                    ], style = {'padding-top':'1rem'}),

                                ]),
                                
                            ])
                        ),
                        id="collapse",
                        is_open=False,
                        style = {'padding-bottom':'1rem'}),
                    html.Div(id="output", children=[]),

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
                                    multi=True,
                                )
                            ])
                        ]),

                        dbc.Col([
                            html.Div([
                            #     html.Button('Train Data', id = 'training submit_id', n_clicks=0, 
                            #     style= {'background-color' : '#6E6E6E', 'color' : 'white', 'border' : 'none', 'border-radius' : '5px', 'display' : 'inline-block', 'height' : '30px', 'width' : '200px', 'margin-left' : '200px'}),
                            ]),
                        ]),

                        dbc.Col([
                            html.Div([
                                html.Button('Train Data', id = 'training submit_id', n_clicks=0, 
                                style= {'background-color' : '#6E6E6E', 'color' : 'white', 'border' : 'none', 'border-radius' : '5px', 'display' : 'inline-block', 'height' : '30px', 'width' : '200px', 'margin-left' : '200px'}),
                                # html.Button('Create a New Strategy', id = 'create_strategy', n_clicks=0, style= {'background-color' : '#6E6E6E', 'color' : 'white', 'border' : 'none', 'border-radius' : '5px', 'display' : 'inline-block', 'height' : '30px', 'width' : '200px', 'margin-left' : '200px'}),
                            ]),
                        ]),
                    ],style = {'padding-bottom':'3rem'}),
                    dbc.Row([
                        html.H3("Training Result Summary"),
                    ], style= {'padding-bottom':'0.1rem', 'padding-top':'1rem'}),
                    #The training summary and the details of the model selected are dynamically filled over here.  
                    html.Div(id ='training_details', children=[]),

                    dbc.Row([
                        html.Div(id ='file-list'),
                    ]),

                    dbc.Row([
                        html.H4("Step 3: Proceed to Predict!"),
                        html.Div("Select the dataset and strategy to be used for prediction.",style={'text-align' : 'left', 'color' : '#686868', 'font-size' : '','padding-bottom':'10px'}),
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
                                dcc.Dropdown( 
                                    id ="Final Strategy Selection",
                                    options=[],
                                    placeholder = "Select Strategy"
                                )
                            ]),
                        ]),
                        dbc.Col([
                            html.Div([
                                    html.Button('Predict Entire Dataset', id = 'custom submit_id', n_clicks=0, style= {'background-color' : '#714FFF', 'color' : 'white', 'border' : 'none', 'border-radius' : '5px', 'display' : 'inline-block', 'height' : '35px', 'width' : '250px',  'margin-left' : '440px' }),
                                    html.Div(id="loading_c", className="loader", hidden='HIDDEN')
                            ]),
                        ]),
                    ],style = {'padding-top':'1rem', 'padding-bottom':'2rem'}),
                    dbc.Row([
                             html.Button('Back to Home', id = 'home', n_clicks=0, style= {'background-color' : '#2C2B2B', 'color' : 'white', 'border' : 'none', 'border-radius' : '5px', 'display' : 'inline-block', 'height' : '35px', 'width' : '150px',  'margin-left' : '440px'}),
                    ], style={'padding-left':'160px', 'padding-bottom': '1.5rem'}),
                ], class_name= "page-view")
            ])
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


#---------------------------------Function to fetch the uploaded dataset and strategy from database---------------------------------------------------------------------#
@app.callback(
    Output(component_id='Training Data Selection', component_property='options'),
    Output(component_id='Training Strategy Selection', component_property='options'),
    Output(component_id='Custom Data Selection', component_property='options'),
    [Input('file-list', 'children')],

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
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------#



#---------Function to redirect to different pages based the input provided--------------------------------------------------------------------------------------------------------------------------------------------------------#
@app.callback(
    Output('url_path_1', 'pathname'),
    Input('custom submit_id', 'n_clicks'),
    Input('home', 'n_clicks'),
    [State('trainingdata', 'data'), State('sstrategy', 'data'), State('testingdata', 'data'), State('mae_rmse', 'data'),
    State('strategies', 'data'), State('bar_graph_values', 'data'), State('anomaly_values', 'data')],
    prevent_initial_callback = True
)
def training_redirection(n_clicks1, n_clicks2, t_dataset, strategy, c_dataset, mae_rmse, strategies, graph_values, anomaly_values):
    if not c_dataset == None and not strategy == None and not mae_rmse == None and not strategies == None and not graph_values == None and not current_user.get_id() == None:
        print(strategies)
        p_data = PreviousPredictions.query.filter_by(file_id = c_dataset, strategy_id=strategy).first()
        for i in mae_rmse:
            if i[0] == strategy:
                mae = i[1]
                rmse = i[2]
            else:
                pass
        if p_data == None:
                #insert into database
            ins = previousPredictions_tbl.insert().values(user_id=current_user.get_id(), strategy_id = strategy, file_id = c_dataset, mae = mae, rmse = rmse, graph_values=str(graph_values))
        elif str(p_data.user_id) == current_user.get_id() and p_data.strategy_id == strategy and p_data.file_id == c_dataset:
                #update the database
            ins = previousPredictions_tbl.update().where(previousPredictions_tbl.c.user_id == current_user.get_id(), previousPredictions_tbl.c.strategy_id == strategy).values(user_id=current_user.get_id(), strategy_id = strategy, file_id = c_dataset, mae = mae, rmse = rmse, graph_values=str(graph_values))
        conn = engine.connect()
        conn.execute(ins)
        conn.close()
    else:
        pass
    id = ctx.triggered_id
    if id == "custom submit_id":
        if current_user.is_authenticated:
            call_predictions(t_dataset, c_dataset, strategy, "testing", anomaly_values)
            return '/2021data'
        else:
            pass
    elif id == "home":
        if current_user.is_authenticated:
            return '/first_page'
        else:
            pass
    else:
        pass
    return dash.no_update
#------------------------------------------------------------------------------------------------------------------------------------------------------------


#-------Driver to call the method for training and testing the data-----------------------------------------------------------------------------------------
def call_predictions(train_dataset_id, test_dataset_id, strategy_id, type, anomaly_values):
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
    errors = predictOnSelectedModel(datasetPath_train, datasetPath_test, strategyName, json_val, type, anomaly_values)
    return errors
#--------------------------------------------------------------------------------------------------------------------------------------------------


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
    Input('Final Strategy Selection', 'value'),
    prevent_initial_callback = True
)
def store_testingdata(value):
    return value
#----------------------------------------------------------------------------------------------------------------------------#


#--------Driver method to get mae, rmse and summary bar graph---------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
@app.callback(
    [Output('training_details', 'children'), Output('strategies', 'data'), Output('mae_rmse', 'data'), Output('bar_graph_values', 'data'), Output('Final Strategy Selection', 'options')],
    [Input('training submit_id', 'n_clicks'),Input('Training Strategy Selection', 'value')],
    [State('trainingdata', 'data'),State('testingdata', 'data')],
    prevent_initial_callback = True
)
def get_error_values(nclicks, value, t_dataset, c_dataset):
    if nclicks>0:
        if current_user.is_authenticated:
            if value is not None:
                conn = sqlite3.connect("./database/data.sqlite")
                children = [html.Div([dbc.Row([
                                dbc.Col([
                                    html.Div()
                                ]),
                                # dbc.Col([
                                #     html.Div("Based on the selected base model, the strategy should account for high seasonal variations. Refer below for more information.",
                                #     style={'text-align' : 'left', 'color' : '#686868'} ),
                                # ]),
                            ]),])]
                #based on multiple strategies selected, display appropriate details
                s = []
                for i in value:
                    strategy = pd.read_sql("""select strategy_id, strategy_name from strategy where strategy_id = '{}'""".format(i), conn)
                    strategy = strategy.values.tolist()
                    if not strategy == []:
                        s.append({'label' : strategy[0][1], 'value' : strategy[0][0]})
                err = []
                strat = []
                e = []
                for i in value:
                    strategy = pd.read_sql("""select strategy_name, strategy_data from strategy where strategy_id = '{}'""".format(i), conn)
                    strategy_title = strategy["strategy_name"].loc[0]
                    strategy_info = strategy["strategy_data"].loc[0]
                    info_dict = json.loads(strategy_info)
                    base_model = "Base Model: " + str(info_dict.get('name'))
                    del info_dict['name']
                    param = "Parameter: " + str(info_dict)
                    #display information of strategy
                    intermediate = html.Div([                                
                                dbc.Row([
                                    dbc.Row([
                                        html.H3(strategy_title),
                                    ]),
                                    dbc.Row([
                                        dbc.Col([
                                            html.Div(base_model, style={'text-align' : 'left', 'color' : '#686868'}),
                                            html.Div(param, style={'text-align' : 'left', 'color' : '#686868'}),
                                        ]),

                                    ]),
                                ], class_name='first_row'),])
                    children.append(intermediate)
                    data = {}
                    #call method for training the model on training data
                    errors, dataframe = call_predictions(t_dataset, c_dataset, i, "training", data)
                    err.append(errors[2])
                    children.append(get_error_plot(errors[0], errors[1]))
                    strat.append(strategy_title)
                    e.append([i, errors[0], errors[1]])
                    #the method to display the summary graph
                intermediate =  html.Div([
                    dcc.Graph(figure= get_bar_graph(err, strat)),
                ])
                children.append(intermediate)
                print("get_error", value)
                return children, value, e, err, s
            else:
                pass
        else:
            pass
    else:
        pass
    return dash.no_update
#------------------------------------------------------------------------------------------------------------------------------------------#

#----------Display mae and rmse errors-----------------------------------------------------------------------------------------------------#
def get_error_plot(mae, rmse) -> html.Div :
    itermediate = html.Div([dbc.Row([
        dbc.Row([
            dbc.Col([
                html.Div("Mean Absolute Error:   " + str('{0:.6g}'.format(mae))),
                html.Div("Root Mean Squared Error:   " + str('{0:.6g}'.format(rmse))),
            ], width=3,class_name='first_row' ),
        ]),]),
        
        ])
    return itermediate
#----------------------------------------------------------------------------------------------------------------------------#

#-------Display summary bar graph----------------------------------------------------------------------------------------------#
def get_bar_graph(err, strategy):
    x = ['0-0.0005', '0.0005-0.001', '0.001-0.005', '0.005-0.01', '0.01-0.05', '0.05-0.1', '0.1-0.5', '0.5-1','>=1']  
    df1 = pd.DataFrame (x, columns = ['x'])
    df2 = pd.DataFrame(err)
    df2 = df2.transpose()
    i=0
    for col in df2.columns[:]:
        df2 = df2.rename(columns={col:strategy[i]})
        i = i+1
    df = pd.concat([df1, df2], axis=1)
    fig = px.bar(df,x=x, y=strategy, labels={'x':'intervals', 'y' : 'frequency'}, barmode='group')
    fig.update_xaxes(type='category')
    return fig
#------------------------------------------------------------------------------------------------------------------------------

#------Anomaly Detection Card------------------------------------------------------------------------------------------------------------
@app.callback(
    Output("collapse", "is_open"), Output("switch", "label"),
    Input("switch", "value"),
    State("collapse", "is_open")
)
def fill_card(value, is_open):
    if value == True:
        return True, "Anomaly Detection On"
    else:
        return False, "Anomaly Detection Off" 
#-----------------------------------------------------------------------------------------------------------------------------------

#---Store Anomaly Detection Data---------------------------------------------------------------------------------------------------------------------------

@app.callback(
    Output('anomaly_values', 'data'), 
    [Input('anomaly_confirm', 'n_clicks'), Input("observation_window", "value"), Input("anomly_window", "value"), 
    Input("thresold", "value"), Input("detection_method", "value"), Input("z-value", "value"), Input("switch", "value")],
    prevent_initial_call=True
)
def get_data(n_clicks, ob_window, a_window, thresold, detection, zvalue, switch):
    data = {}
    if switch == True:
        if not n_clicks == None and n_clicks>0:
            data = {'switch' : switch, 'ob_window' : ob_window, 'a_window' : a_window, 'thresold' : thresold, 'detection_method' : detection, 'zvalue' : zvalue}
            return data
        else:
            pass
    else:
        return {}
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


        

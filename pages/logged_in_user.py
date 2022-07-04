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
from statsmodels.tsa.holtwinters import SimpleExpSmoothing
import numpy as np

logged_in_user = html.Div([dcc.Location(id = 'url_path', refresh=True),
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
                    placeholder = "Select Custom DataSet",
                    # value = 'None'
                )
            ])
        ]),
        #---------------------------------------------------------------------------------------------------------------#


        #---------------------------------------Second Dropdown(Strategy Selection)---------------------------------------#
        dbc.Col([
            html.Div([
                dcc.Dropdown(
                    id ="Strategy Selection", 
                    options=[],
                    placeholder = "Select Strategy",
                )
            ])
        ]),
        #----------------------------------------------------------------------------------------------------------------#


        dbc.Col([
            html.Div([
                html.I("Input the threshold of the training data:"),
                dcc.Input(id="traindata", type='number', placeholder="Enter Number"),
                ])
        ]),


        dbc.Col([
            html.Div([
                    html.Button('Predict', id = 'custom submit_id', n_clicks=0),
                    # dbc.Spinner(children=[dcc.Location(id="loading_output")], size="lg", color="primary", type="border", fullscreen=True,),
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





@app.callback(
    Output(component_id='Custom Data Selection', component_property='options'),
    Output(component_id='Strategy Selection', component_property='options'),
    [Input('upload-data', 'children')]
)
def get_custom_datasets(filename):
    conn = sqlite3.connect("./database/data.sqlite")
    g.user = current_user.get_id()
    id = g.user

    datasets = pd.read_sql("""select file_id, filename from files where user_id = '{}'""".format(id), conn)
    datasets = datasets.values.tolist()
    datasets = [{'label' : i[1], 'value' : i[0]} for i in datasets]

    get_strategy = pd.read_sql("""select strategy_id, strategy_name from strategy where user_id = '{}'""".format(id), conn)
    get_strategy = get_strategy.values.tolist()
    get_strategy = [{'label' : i[1], 'value' : i[0]} for i in get_strategy]
    return datasets, get_strategy

@app.callback(
    Output('customdataset', 'data'),
    [Input('Custom Data Selection','value')],
    prevent_initial_callback = True
)
def store_custom_dataset(value):
    return value


@app.callback(
    Output('customstrategy', 'data'),
    [Input('Strategy Selection','value')],
    prevent_initial_callback = True
)
def store_custom_strategy(value):
    return value


@app.callback(
    Output("file-list", "children"),
    [Input('upload-data', 'filename'),
    Input('upload-data', 'contents')],
    prevent_initial_call=True
)
def update_output(filename,content):
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
        ins = Uploaded_files_tbl.insert().values(user_id = current_user.get_id(), filepath = path, filename = file_name)
        conn = engine.connect()
        conn.execute(ins)
        conn.close()

@app.callback(
    Output(component_id='url_path', component_property='pathname'),
    # Output('loading_output', 'pathname'),
    [Input('create_strategy', 'n_clicks'),
    Input('custom submit_id', 'n_clicks')],
    [State('customdataset', 'data'), 
    State('customstrategy', 'data'),
    State('trainingthreshold', 'data')],
    prevent_initial_callback = True
)
def create_the_new_strategy(n_clicks1, n_clicks2, dataset, strategy, training_data_index):
    id = ctx.triggered_id
    if id == "create_strategy":
        if current_user.is_authenticated:
            return '/strategy'
        else:
            pass
    elif id == "custom submit_id":
        if current_user.is_authenticated:
            #add gif until the data is being processed.
            call_predictions(dataset, strategy,training_data_index)
            return '/2021data'
        else:
            pass
    else:
        pass


def call_predictions(dataset, strategy, training_data_index):
    conn = sqlite3.connect("./database/data.sqlite")
    df_dataset = pd.read_sql("""select filepath from files where file_id = '{}'""".format(dataset), conn)
    df_strategy = pd.read_sql("""select strategy_name from strategy where strategy_id = '{}'""".format(strategy), conn) 
    datasetPath = df_dataset["filepath"].loc[0]
    strategyName = df_strategy["strategy_name"].loc[0]
    df = pd.read_csv(datasetPath, encoding='utf-8')
    columnName = strategyName
    # j=0
    for i in range(training_data_index,len(df)):
        # train = df.iloc[j:i]
        train = df.iloc[0:i]
        model = SimpleExpSmoothing(train['true value']).fit()
        data = np.array(model.forecast())
        df.loc[df.index[i], columnName] = data[0]
        # j = j + 1
    df_col = list(df.columns)
    if "Unnamed" not in df_col[0]:
        df.to_csv(datasetPath, index=True)
    else:
        df.to_csv(datasetPath, index=False)


#---------------------------------------Number of Dataset used for training data--------------------------------------------#
@app.callback(
    Output(component_id='trainingthreshold', component_property='data'),
    [Input('traindata', 'value')],
    prevent_initial_callback = True
)
def get_threshold(value):
    return value
#-----------------------------------------------------------------------------------------------------------------#
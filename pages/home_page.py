#from asyncio.windows_events import NULL
from cProfile import label
from dash import dcc
from dash import html, ctx
import dash
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from flask_login import login_required
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from numpy import equal, genfromtxt
import plotly.graph_objects as go
from pages import pages2021 as p21
from app import app

from operator import itemgetter
import os
import json
from flask_login import current_user

from tool.datapathscsv import META_DATA_CSV

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def test():
    df = px.data.gapminder().query("country=='Canada'")
    fig = px.line(df, x="year", y="lifeExp", title='Life expectancy in Canada')
    return fig

#----------------------------------------------------------Demo Page----------------------------------------------------#

home_page = html.Div([dcc.Location(id = 'url_new', refresh=True),
    dbc.Row([
        #---------------------------------------First Dropdown(DataSet Selection)---------------------------------------#
        html.H4("Try our Reliability Predition tool on our Demo Data!"),
        dbc.Col([
            html.Div([
                dcc.Dropdown(
                    id = "Data Selection",
                    options=[{'label': 'Select DataSet', 'value' :'None'},
                    {'label':'Dataset1', 'value' : '1'},
                    {'label':'Dataset2', 'value' : '2'}, 
                    {'label':'Dataset3', 'value' : '3'}, 
                    {'label':'DataSetSEC', 'value' : '4'},
                    #{'label':'LiveData', 'value' : '5'}
                    ], 
                    placeholder = "Select Dataset",
                    value = 'None'
                )
            ])
        ]),
        #--------------------------------------------------------------------------------------------------------------#
        
        #---------------------------------------Second Dropdown(Model Selection)---------------------------------------#
        dbc.Col([
            html.Div([
                    dcc.Dropdown(
                    id ="Model Selection", 
                    options=['SES','SVR'],
                    placeholder = "Select Models",
                    multi=True,
                    disabled=True
                )
                ])
        ]),
        #--------------------------------------------------------------------------------------------------------------#
        dbc.Col([
            html.Div([
                    html.Button('Predict', id = 'submit_id', n_clicks=0)
            ])
        ])
    ],class_name="notice-card", style={"column-gap" : "40px"}),


#------------------------------------------------------Sign Up Redirection-----------------------------------------------#
    dbc.Row([
        dbc.Col([
            html.H4("Have your own Data?"),
            html.Div("Do you have your own data that you want to try out? Then you come to the right place!", className = "description"),
            html.Div([
                dbc.Button("Click here!", color="info", id='userplayground')
            ],style={"display": "flex", "flexFlow": "row-reverse nowrap"})
            
        ], width=6, class_name="notice-card"),

        dbc.Col([
            html.H4("Do you want to create your own strategy?"),
            html.Div([
                dbc.Button("Click here!", color="info", id='strategy')
            ],style={"display": "flex", "flexFlow": "row-reverse nowrap"})
            
        ], width=5, class_name="notice-card")

    ], style={"padding" : "20px", "column-gap" : "30px"})
],)
#------------------------------------------------------------------------------------------------------------------------#



#------------------------Enable the second dropdown after first dropdown value is selected------------------- -----------#
@app.callback(
    Output(component_id='Model Selection', component_property='disabled'), Input('Data Selection', 'value')
)
def show_next_dropdown(value):
    if value == 'None':
        return True
    else:
        return False
#-------------------------------------------------------------------------------------------------------------------------#




#------------------------------------Selection of Models on basis of DataSet selected-------------------------------------#
@app.callback(
    Output(component_id='Model Selection', component_property='options'), [Input(component_id= 'Data Selection', component_property='value')]
)
def show_next_dropdown(value):
    if value == '1':
        models = itemgetter('available_models')(META_DATA_CSV["DataSet1"])
        return [{'label' : i, 'value' : i} for i in models]
    elif value == '2':
        models = itemgetter('available_models')(META_DATA_CSV["DataSet2"])
        return [{'label' : i, 'value' : i} for i in models]
    elif value == '3':
        models = itemgetter('available_models')(META_DATA_CSV["DataSet3"])
        return [{'label' : i, 'value' : i} for i in models]
    elif value == '4':
        models = itemgetter('available_models')(META_DATA_CSV["DataSetSEC"])
        return [{'label' : i, 'value' : i} for i in models]
    # elif value =='5':
    #     dcc.Link(id='live data', href='/live')
    #     return None
    else:
        return []
#-------------------------------------------------------------------------------------------------------------------------#

@app.callback(
    Output('datasetName', 'data'),
    Input('Data Selection', 'value')
)
def set_dataset(value):
    return value


#--------------------------------------------Redirect to Demo Dataset Page------------------------------------------------#
@app.callback(
   [Output('url_new', 'pathname'), Output('modelsList', 'data')],
    [Input('submit_id', 'n_clicks'), Input('userplayground', 'n_clicks'), Input('strategy', 'n_clicks')],
    [State('Data Selection', 'value'), State('Model Selection', 'value')]
)
def submit_dataset(n_clicks1, n_clicks2, n_clicks3, value1, value2):
    id = ctx.triggered_id
    if id == "strategy":
        if current_user.is_authenticated:
            return '/strategy', None
        else:
            return '/signup', None
    elif id == "submit_id":
        if value1 == '1':
            return "/2021data_1", value2
        elif value1 == '2':
            return "/2021data_2", value2
        elif value1 == '3':
            return "/2021data_3", value2  
        elif value1 == '4':
            return "/2021data_sec", value2     
        else:
            return "/", None
    elif id == "userplayground":
        if current_user.is_authenticated:
            return '/userplayground', None
        else:
            return '/signup', None
    else:
        pass


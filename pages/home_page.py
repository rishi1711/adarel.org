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

#----------------------------------------------Front end of the Demo page------------------------------------------------------------------------------------------------------------------------------------------#
home_page = html.Div([dcc.Location(id = 'url_new', refresh=True),
    dbc.Row([
        #---------------------------------------First Dropdown(DataSet Selection)---------------------------------------#
        html.H4("DEMO DATA"),
        html.Div("You will be able to see how AdaRel performs on our collected dataset."),
        dbc.Col([
            html.Div([
                dcc.Dropdown(
                    id = "Data Selection",
                    options=[{'label': 'Select Demo Data', 'value' :'None'},
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
                    html.Button('Predict',
                        id = 'submit_id', 
                        n_clicks=0,
                        style= {'background-color' : '#5D5C78', 'color' : 'white', 'border' : 'none', 'border-radius' : '5px', 'display' : 'inline-block', 'height' : '30px'})
            ])
        ])
    ],class_name="demo-card", style={"column-gap" : "10px"}),
])
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#


#------------------------Enable the second dropdown after first dropdown value is selected-------------------------------#
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


#--------------------------------------------Redirect to a different page--------------------------------------------------#
@app.callback(
   [Output('url_new', 'pathname'), Output('modelsList', 'data')],
    [Input('submit_id', 'n_clicks')],
    [State('Data Selection', 'value'), State('Model Selection', 'value')]
)

def submit_dataset(n_clicks1, value1, value2):
    id = ctx.triggered_id
    if id == "submit_id":
        if value1 == '1':
            return "/2021data_1", value2
        elif value1 == '2':
            return "/2021data_2", value2
        elif value1 == '3':
            return "/2021data_3", value2  
        elif value1 == '4':
            return "/2021data_sec", value2     
        else:
            return "/home_page", None
    else:
        pass


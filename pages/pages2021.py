from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from app import app
from database.models import Uploaded_files_tbl
from database.models import Uploadedfiles
from database.models import engine
from flask_login import current_user
from flask import g
import sqlite3
import pandas as pd
import tool.figgenerator as fgen


def get_pages_obj(title: str, file_url: str, dataset_name: str) -> html.Div :
    html_div = html.Div([
        dbc.Row([
            dbc.Col(
                html.H3(title),
                width = 4,
            ),
            dbc.Col( 
                html.A(f"Download this data set ({dataset_name})", href=file_url),
                width = 4,
            ),
        ], justify='between',
        ),
        dbc.Row([
            dbc.Col([ 
                html.Div([
                    dcc.Graph(figure= fgen.get_fig(dataset_name))
                ])
            ])
        ])
    ])
    return html_div


def get_pages_obj_csv(title: str, dataset_name: str, additional_WebDom: html.Div= None, data=None) -> html.Div :
    itermediate = [
        dbc.Row([
            html.H1("My Workspace > Prediction Result", style={'text-align' : 'left', 'color' : '#686868', 'font-size' : '3rem', 'padding-bottom' : '', 'padding-top' : '20px'}),
            html.Div("The prediction result on the selected dataset is shown in graph below." ,style={'text-align' : 'left', 'color' : '#686868', 'font-size' : '', 'padding-bottom' : '20px'}),
        ]),
        dbc.Row([
            # dbc.Col(
            #     html.H3(title),
            #     width = 4,
            # ),
            dbc.Col( 
                html.A(f"Download this data set ({dataset_name})", href=f"/2021data/{dataset_name}"),
                width = 4,
            ),
        ], justify='between',
        ),
        dbc.Row([
            dbc.Col([ 
                html.Div([
                    dcc.Graph(figure= fgen.get_fig_from_csv(dataset_name, data)),
                ])
            ])
        ])
    ]

    if additional_WebDom:
        itermediate.append(dbc.Row([dbc.Col([additional_WebDom])]))

    html_div = html.Div(itermediate)        
    return html_div

def get_MAE_dist_fig(dataset_name: str) -> html.Div:
    result = html.Div([
        html.Img(src=f'/2021data/mae_dist_fig/{dataset_name}', width='800px')
    ])
    return result


def get_graph_from_custom_dataset(title: str, additional_WebDom: html.Div= None, dataset_path=None, strategy_name=None) -> html.Div :
    itermediate = [
        dbc.Row([
            html.H1("My Workspace > Prediction Result", style={'text-align' : 'left', 'color' : '#686868', 'font-size' : '3rem', 'padding-bottom' : '', 'padding-top' : '20px'}),
            html.Div("The prediction result on the selected dataset is shown in graph below." ,style={'text-align' : 'left', 'color' : '#686868', 'font-size' : ''}),
        ]),
        # dbc.Row([
        #     dbc.Col(
        #         html.H3(title),
        #         width = 4,
        #     ),
        # ],
        # ),

        dbc.Row([
            dbc.Col([ 
                html.Div([
                    dcc.Graph(figure= fgen.get_fig_from_custom_csv(dataset_path, strategy_name)),
                ])
            ])
        ])
    ]

    if additional_WebDom:
        itermediate.append(dbc.Row([dbc.Col([additional_WebDom])]))

    html_div = html.Div(itermediate)       
    return html_div

def dataset_1(data):
    return get_pages_obj_csv("Empirical Study 1", "DataSet1", get_MAE_dist_fig("DataSet1"), data)
def dataset_2(data):
    return get_pages_obj_csv("Empirical Study 2", "DataSet2", get_MAE_dist_fig("DataSet2"), data)
def dataset_3(data):
    return get_pages_obj_csv("Empirical Study 3", "DataSet3", None, data)
def dataset_sec(data):
    return get_pages_obj_csv("Empirical Study SEC", "DataSetSEC", get_MAE_dist_fig("DataSetSEC"), data)

def custom_dataset(training, strategy, testing):
    conn = sqlite3.connect("./database/data.sqlite")
    df_dataset = pd.read_sql("""select filepath from files where file_id = '{}'""".format(testing), conn)
    df_strategy = pd.read_sql("""select strategy_name from strategy where strategy_id = '{}'""".format(strategy), conn)
    path = df_dataset["filepath"].loc[0]
    strat_name = df_strategy["strategy_name"].loc[0]
    return get_graph_from_custom_dataset("Empirical Study", None, path, strat_name) 

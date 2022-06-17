from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from app import app


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
            dbc.Col(
                html.H3(title),
                width = 4,
            ),
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

def dataset_1(data):
    return get_pages_obj_csv("Empirical Study 1", "DataSet1", get_MAE_dist_fig("DataSet1"), data)
def dataset_2(data):
    return get_pages_obj_csv("Empirical Study 2", "DataSet2", get_MAE_dist_fig("DataSet2"), data)
def dataset_3(data):
    return get_pages_obj_csv("Empirical Study 3", "DataSet3", None, data)
def dataset_sec(data):
    return get_pages_obj_csv("Empirical Study SEC", "DataSetSEC", get_MAE_dist_fig("DataSetSEC"), data)

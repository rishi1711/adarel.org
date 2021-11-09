from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

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

def get_pages_obj_csv(title: str, file_url: str, dataset_name: str) -> html.Div :
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
                    dcc.Graph(figure= fgen.get_fig_from_csv(dataset_name))
                ])
            ])
        ])
    ])
    return html_div

dataset_1 = get_pages_obj_csv("Empirical Study 1", "/static/2021_DataSet1.csv", "DataSet1")
dataset_2 = get_pages_obj_csv("Empirical Study 2", "/static/2021_DataSet2.csv", "DataSet2")
dataset_3 = get_pages_obj_csv("Empirical Study 3", "/static/2021_DataSet3.csv", "DataSet3")
dataset_sec = get_pages_obj_csv("Empirical Study SEC", "/static/2021_DataSetSEC.csv", "DataSetSEC")
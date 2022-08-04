from dash import dcc, dash_table
from dash import html, ctx
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
from urllib.parse import quote as urlquote
from app import app
from flask_login import current_user
from database.models import Uploaded_files_tbl
from flask import g
from database.models import engine
import sqlite3
import dash
import base64
import os
import io
import json

create_data = html.Div([dcc.Location(id = 'url_redirect', refresh=True),
    dbc.Row([
            html.H1("My Workspace > Create Data", style={'text-align' : 'left', 'color' : '#686868', 'font-size' : '3rem', 'padding-bottom' : '1rem', 'padding-top' : '40px'}),
            html.Div("You will be able to upload new data here." ,style={'text-align' : 'left', 'color' : '#686868', 'font-size' : '', 'padding-bottom' : ''}),
            html.Div("The current supported data format are csv, xls files with specific headers or raw Nginx/Apache error files.", style={'text-align' : 'left', 'color' : '#686868', 'font-size' : '', 'padding-bottom' : '2rem'}),
    ]),
    dbc.Row([
        dcc.Upload(
            id = "upload__data",
            children=html.Div("Drag and Drop or Click here to select a file to upload.", style={'text-align' : 'center', 'padding-top' : '2rem'}
            ),
            style={
                "width": "100%",
                "height": "120px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px",
            },
            #multiple=True,
        ),
    ]),

    dbc.Row([
        html.Div("Note: It is mandatory to specify the type of the dataset you are uploading.(i.e: Training or Testing)", style={'text-align' : 'left', 'color' : '#9E0404', 'font-size' : '1rem', 'padding-bottom' : '1rem', 'padding-top' : '1rem'}),
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Input(id="file-type", type="text", placeholder="Type of Data Upload", style = {'border-radius' : '5px', 'height' : '30px', 'width' : '300px', 'padding-left' : '50px'}),
        ]),
        dbc.Col([
            html.Button("Confirm and Upload", 
                        id = 'confirm_upload', 
                        n_clicks=0,
                        style= {'background-color' : '#714FFF', 'color' : 'white', 'border' : 'none', 'border-radius' : '5px', 'display' : 'inline-block', 'height' : '30px', 'width' : '300px'}),
            ],class_name='button_style_data_upload'),
    ]),
    dbc.Row([
            dash_table.DataTable(id = 'preview_data'),
    ]),
    ]),

@app.callback(
    Output('preview_data', 'data'),
    Output('dataframe', 'data'),
    Output('path', 'data'),
    Output('filename', 'data'),
    [Input('upload__data', 'filename'),
    Input('upload__data', 'contents')],
    prevent_initial_callback=True
)
def data_upload(filename, content):
    if filename is not None and content is not None:
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
            # df.to_csv (path, index = False, header=True)
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        file_name=os.path.splitext(filename)[0]
        return df.to_dict('records'), df.to_json(), path, file_name
    else:
        return dash.no_update

@app.callback(
    Output('url_redirect', 'pathname'),
    Input('confirm_upload', 'n_clicks'),
    State('type','data'),
    State('dataframe', 'data'),
    State('path', 'data'),
    State('filename', 'data'),
    prevent_initial_callback = True
)
def upload_confirmation(nclicks, type, df, path, filename):
    if nclicks>0:
        df = pd.read_json(df)
        df.to_csv (path, index = False, header=True)
        if filename is not None and current_user.get_id() is not None and path is not None:
            ins = Uploaded_files_tbl.insert().values(user_id = current_user.get_id(), filepath = path, filetype = type, filename = filename)
            conn = engine.connect()
            conn.execute(ins)
            conn.close()
            return '/first_page'
        else:
            pass
    else:
        return dash.no_update

@app.callback(
    Output('type', 'data'),
    Input('file-type', 'value')
)
def gettype(filetype):
    return filetype
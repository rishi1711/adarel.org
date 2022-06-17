from fileinput import filename
from dash import dcc
from dash import html
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
from database.models import engine
import flask_login

from flask import Flask, send_from_directory
import dash
from dash.dependencies import Input, Output

UPLOAD_DIRECTORY = "/Users/patil24/adarel.org/user_data/"

logged_in_user = html.Div([
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
        html.H5("File List"),
        html.Ul(id="file-list"),
    ],),

    dbc.Row([
        #---------------------------------------First Dropdown(DataSet Selection)---------------------------------------#
        html.H4("Lets Get Started!"),
        dbc.Col([
            html.Div([
                dcc.Dropdown(
                    id = "Custom Data Selection",
                    options=[{'label': 'Select DataSet', 'value' :'None'},
                        {'label': 'Custom Dataset', 'value':'1'}
                    ], 
                    placeholder = "Select DataSet",
                    value = 'None'
                )
            ])
        ]),
        #--------------------------------------------------------------------------------------------------------------#
        
        #---------------------------------------Second Dropdown(Model Selection)---------------------------------------#
        dbc.Col([
            html.Div([
                    dcc.Dropdown(
                    id ="Custom Model Selection", 
                    options=['arima'],
                    placeholder = "Select Models",
                    multi=True,
                    disabled=True
                )
                ])
        ]),
        #--------------------------------------------------------------------------------------------------------------#
        dbc.Col([
            html.Div([
                    html.Button('Predict', id = 'custom submit_id', n_clicks=0)
            ])
        ])
    ],class_name="notice-card"),
    ])

#----------------------------------------------------Disable Property Unable-------------------------------------------#
@app.callback(
    Output(component_id='Custom Model Selection', component_property='disabled'), Input('Custom Data Selection', 'value')
)
def show_next_dropdown(value):
    if value == 'None':
        return True
    else:
        return False
#-----------------------------------------------------------------------------------------------------------------------#

def download(path):
    """Serve a file from the upload directory."""
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)

def save_file(name, content):
    """Decode and store a file uploaded with Plotly Dash."""
    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join(UPLOAD_DIRECTORY, name), "wb") as fp:
        fp.write(base64.decodebytes(data))

def uploaded_files():
    """List the files in the upload directory."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return files

def file_download_link(filename):
    """Create a Plotly Dash 'A' element that downloads a file from the app."""
    location = "/download/{}".format(urlquote(filename))
    return html.A(filename, href=location)

# @app.callback(
#     Output("file-list", "children"),
#     [Input("upload-data", "filename")]
# )
# def update_output(namefile):
#     """Save uploaded files and regenerate the file list."""

#     if namefile is not None:
#         location = UPLOAD_DIRECTORY+namefile
#         # for name, data in zip(uploaded_filenames, uploaded_file_contents):
#         #     save_file(name, data)


#     if namefile is not None:
#         name = os.path.splitext(namefile)[0]
#     else:
#         name = None
#     # name_of_user = getpass.getuser()
#     name_of_user = flask_login.current_user
#     print(name_of_user)
#     if name is not None and location is not None and name_of_user is not None:
#         ins = Uploaded_files_tbl.insert().values(user_id = name_of_user, filepath = location, filename = name)
#         conn = engine.connect()
#         conn.execute(ins)
#         conn.close()

#flask_login.current_user

    # if len(files) == 0:
    #     return [html.Li("No files yet!")]
    # else:
    #     return [html.Li(file_download_link(filename)) for filename in files]
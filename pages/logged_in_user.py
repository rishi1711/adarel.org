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

from flask import Flask, send_from_directory
import dash
from dash.dependencies import Input, Output

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def test():
    df = px.data.gapminder().query("country=='Canada'")
    fig = px.line(df, x="year", y="lifeExp", title='Life expectancy in Canada')
    return fig


UPLOAD_DIRECTORY = "/Users/patil24/adarel.org/user_data/"

logged_in_user = html.Div([
    dbc.Row([
        html.H1("Want to upload your Custom Data Set!"),
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
            multiple=True,
        ),
        html.H5("File List"),
        html.Ul(id="file-list"),
    ],
    style={"max-width": "500px"},),

    dbc.Row([
        #---------------------------------------First Dropdown(DataSet Selection)---------------------------------------#
        html.H4("Lets Get Started!"),
        dbc.Col([
            html.Div([
                dcc.Dropdown(
                    id = "Data Selection",
                    options=[{'label': 'Select DataSet', 'value' :'None'},
                    {'label':'DataSet1', 'value' : '1'},
                    {'label':'DataSet2', 'value' : '2'}, 
                    {'label':'DataSet3', 'value' : '3'}, 
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
    ],class_name="notice-card"),
    ])



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
    # return html.A(filename, href=location)
    return filename

@app.callback(
    Output("file-list", "children"),
    [Input("upload-data", "filename"), Input("upload-data", "contents")],
)
def update_output(uploaded_filenames, uploaded_file_contents):
    """Save uploaded files and regenerate the file list."""

    if uploaded_filenames is not None and uploaded_file_contents is not None:
        for name, data in zip(uploaded_filenames, uploaded_file_contents):
            save_file(name, data)

    files = uploaded_files()
    if len(files) == 0:
        return [html.Li("No files yet!")]
    else:
        return [html.Li(file_download_link(filename)) for filename in files]

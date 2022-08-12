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

#----------------------------------------------Front end of the Upload Data Page-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
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
            # dcc.Input(id="file-type", type="text", placeholder="Type of Data Upload", style = {'border-radius' : '5px', 'height' : '30px', 'width' : '300px', 'padding-left' : '50px'}),

            #For the selection of the type of data being uploaded.
            dcc.RadioItems(
                id = "dataset_type",
                options = [{'label': 'Training', 'value': 'Training'},
                {'label': 'Testing', 'value': 'Testing'}],
                value = 'Training'
            )
        ]),

        dbc.Col([
            #To input the name of the file.
            # dcc.Input(id="dataset_name", type="text", placeholder="Enter the Dataset Name"),
            html.Div(id = "choice"),
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
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#


#-------------------------To temporary store and display the name, path and content of the file being uploaded by user----------------------------------------------#
@app.callback(
    Output('preview_data', 'data'),
    Output('dataframe', 'data'),
    Output('path', 'data'),
    Output('oldfilename', 'data'),
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
        oldfilename=os.path.splitext(filename)[0]
        return df.to_dict('records'), df.to_json(), path, oldfilename
    else:
        return dash.no_update
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------#


#-----------------------------------------To store the file being uploaded by the user in the database-------------------------------------------------------------------------------# 
@app.callback(
    Output('url_redirect', 'pathname'),
    Input('confirm_upload', 'n_clicks'),
    State('oldfilename', 'data'),
    State('inputvalue', 'data'),
    State('dropdownvalue','data'),
    State('dataset_type','value'),
    State('dataframe', 'data'),
    State('path', 'data'),
    prevent_initial_callback = True
)

def upload_confirmation(nclicks, oldfilename, inputvalue, dropdownvalue, file_type, df, path):
    if nclicks>0:
        df = pd.read_json(df)
        if inputvalue is not None:
            dataset_name = inputvalue
        else:
            dataset_name = dropdownvalue
        newfilename = dataset_name
        newfilename = newfilename + '_' + file_type
        path = path.replace(oldfilename, newfilename)
        df.to_csv (path, index = False, header=True)
        if newfilename is not None and current_user.get_id() is not None and path is not None:
            ins = Uploaded_files_tbl.insert().values(user_id = current_user.get_id(), filepath = path, filetype = file_type, datasetname = dataset_name, filename = newfilename)
            conn = engine.connect()
            conn.execute(ins)
            conn.close()
            return '/first_page'
        else:
            pass
    else:
        return dash.no_update
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#


#----------------Select/Input dataset name on the basis of radiobutton----------------------------------------------------------------------------------------------------------------#
@app.callback(
    Output('choice', 'children'),
    Input('dataset_type', 'value'),
    prevent_initial_callback = True
)

def give_user_choice(value):
    if value == 'Training':
        return dcc.Input(id="dataset_nameInput", type="text", placeholder="Enter the Dataset Name")
    elif value == 'Testing':
        return dcc.Dropdown(id = "dataset_nameDropdown", options=[], placeholder = "Select Dataset Name", style = {'width': '12rem'})
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#


#----------------Fill the dropdown options--------------------------------------------------------------------------------------------------------------------------------------------#
@app.callback(
    Output('dataset_nameDropdown', 'options'),
    Input('choice', 'children'),
    prevent_initial_callback = True
)

def get_options_for_dropdown(data):
    conn = sqlite3.connect("./database/data.sqlite")
    g.user = current_user.get_id()
    id = g.user

    name = pd.read_sql("""select datasetname from files where user_id = '{}'""".format(id), conn)
    count = name['datasetname'].value_counts()
    l = []
    for item in count.iteritems():
        if item[1]==1:
            l.append(item[0])
    dropdownlist = [{'label' : i, 'value' : i} for i in l]
    return dropdownlist
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#


#----------------Store value selected in dropdown-------------------------------------------------------------------------------------------------------------------------------------#
@app.callback(
    Output('dropdownvalue', 'data'),
    Input('dataset_nameDropdown', 'value')
)

def getdatanamefromdropdown(value):
    return value
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#


#----------------Store value inputted in textbox--------------------------------------------------------------------------------------------------------------------------------------#
@app.callback(
    Output('inputvalue', 'data'),
    Input('dataset_nameInput', 'value'),
)

def getdatanamefrominput(value):
    return value
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

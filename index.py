from dash import dcc
from waitress import serve
from dash import html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from app import app

from pages import first_page
from pages.home_page import home_page
from pages.data1 import data1
from pages.data2 import data2
from pages.data3 import data3 
from pages.data4 import data4
from pages import playground
from pages import pages2021 as p21
from pages.live_page import live_page
from pages.login import login
from pages.Register import create
from pages import strategies
from pages.login_user_1 import login_user_1
from pages.first_page import first_page
from pages.main_page import main_page
from pages.about import about
from pages.create_data import create_data
from pages.logout import logout
from navbar import navbar
import sqlite3
import pandas as pd


import callbacks
import serve_static
import os
from typing import List

#--------------------------------login/ signup/ database connection----------------------------------
# for login signup
import database.models
from database.models import db
from database.models import Users
import warnings
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, LoginManager, UserMixin
import configparser
from sqlalchemy_utils import database_exists, create_database

config = configparser.ConfigParser()
server = app.server

#config the server to interact with the database
#Secret Key is used for user sessions
server.config.update(
    SECRET_KEY=os.urandom(12),
    SQLALCHEMY_DATABASE_URI='sqlite:///database/data.sqlite',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)
db.init_app(server)

# Setup the LoginManager for the server
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = '/login'
#User as base
# Create User class with UserMixin
# class Users(UserMixin, Users):
#     pass
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@login_manager.unauthorized_handler     
def unauthorized_callback():            
       return '/login'

#-------------------------------------------------------------------------------------------------------------------



app.title="AdaRel"

app.layout = html.Div([
        navbar,
        dcc.Store(id="datasetName", storage_type="session"),
        dcc.Store(id="modelsList", storage_type="session"),  
        dcc.Store(id="strategyData", storage_type="session"),
        dcc.Store(id="strategies", storage_type="session"),

        # make prediction page
        dcc.Store(id="trainingdata", storage_type="session"),
        dcc.Store(id="testingdata", storage_type="session"),
        dcc.Store(id="sstrategy", storage_type="session"),
        dcc.Store(id="strategy_id", storage_type="session"),
        dcc.Store(id="testing_id", storage_type="session"),
        dcc.Store(id="mae_rmse", storage_type="session"),
        dcc.Store(id = "bar_graph_values", storage_type="session"),
        dcc.Store(id="dataframe_prediction", storage_type="session"),

        # create data page
        dcc.Store(id="dataframe", storage_type="session"),
        dcc.Store(id="path", storage_type="session"),
        dcc.Store(id="oldfilename", storage_type="session"),
        dcc.Store(id="inputvalue", storage_type="session"),
        dcc.Store(id="dropdownvalue", storage_type="session"),
        
        #anomalyDetection
        dcc.Store(id="anomaly_values", storage_type="session"),

        dbc.Container([                
            # html.Div([
            #     html.H1("AdaRel"),
            #     html.P("a tool for reliability prediction")
            #     ], id="index-title"),
            dcc.Location(id='url', refresh=False),
            html.Div(id='page-content')
        ]),
        
    ])


# making it an instance of function makes it update every load
# https://dash.plotly.com/live-updates
@app.callback(Output('page-content', 'children'), 
[Input('url', 'pathname')], 
[State('modelsList', 'data'),
State('trainingdata', 'data'),
State('sstrategy', 'data'),
State('testingdata', 'data'),State('testing_id', 'data'), State('strategy_id', 'data')
],
prevent_initial_call=True )

def router(pathname, data, training, strategy, testing, testing_id, strategy_id):
    if pathname == '/':
        return main_page
    elif pathname == '/first_page':
        return first_page 
    elif pathname == '/home_page':
        return home_page
    elif pathname == '/about':
        return about
    elif pathname == '/data1':
        return data1
    elif pathname == '/data2':
        return data2
    elif pathname == '/data3':
        return data3
    elif pathname == '/data4':
        return data4
    # elif pathname == '/live':
    #     return live_page
    elif pathname == '/2021data_1':
        return p21.dataset_1(data)
    elif pathname == '/2021data_2':
        return p21.dataset_2(data)
    elif pathname == '/2021data_3':
        return p21.dataset_3(data)
    elif pathname == '/2021data_sec':
        return p21.dataset_sec(data)
    elif pathname == '/2021data':
        return p21.custom_dataset(training, strategy, testing)
    elif pathname == '/previous_prediction':
        return p21.previous_prediction_dataset(strategy_id, testing_id)
    elif pathname == '/userplayground':
        return playground.page
    elif pathname == '/signup':
        return create
    elif pathname == '/login':
        return login
    elif pathname == '/strategy':
        return strategies.strategy
    elif pathname == '/login_user_1':
        return login_user_1
    elif pathname == '/create_data':
        return create_data
    elif pathname == '/logout':
        return logout
    else:
        return 'Error 404'


# if __name__ == '__main__':
#     DEBUG = (os.getenv('DASH_DEBUG_MODE', 'False') == 'True')
#     # DEBUG = True
#     if DEBUG:
#         app.run_server(debug=True, host='0.0.0.0') # Development 
#     else:# prod
#         serve(app.server, host="0.0.0.0", port="8050") 


if __name__ == '__main__':
    # DEBUG = (os.getenv('DASH_DEBUG_MODE', 'False') == 'True')
   DEBUG = True
   if DEBUG:
        app.run_server(debug=True, host='0.0.0.0') # Development 
   else:# prod
        serve(app.server, host="0.0.0.0", port="8050") 
        # remember to clear the cache-directory on startup in prod 

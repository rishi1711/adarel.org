from dash import dcc
from waitress import serve
from dash import html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from navbar import navbar

from app import app
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
from pages.logged_in_user import logged_in_user

from pages.Initial_page import first_page


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

#-------------------------------------------------------------------------------------------------------------------

app.title="AdaRel"

app.layout = html.Div([
        navbar,
        dcc.Store(id="datasetName", storage_type="session"),
        dcc.Store(id="modelsList", storage_type="session"),  
        dbc.Container([                
            html.Div([
                html.H1("AdaRel"),
                html.P("a tool for reliability prediction")
                ], id="index-title"),
            dcc.Location(id='url', refresh=False),
            html.Div(id='page-content')
        ]),
        
    ])


# making it an instance of function makes it update every load
# https://dash.plotly.com/live-updates
@app.callback(Output('page-content', 'children'), 
[Input('url', 'pathname'), State('modelsList', 'data')], prevent_initial_call=True )
def router(pathname, data):
    if pathname == '/':
         return home_page
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
    elif pathname == '/2021data_2':
        return p21.dataset_2(data)
    elif pathname == '/2021data_3':
        return p21.dataset_3(data)
    elif pathname == '/2021data_sec':
        return p21.dataset_sec(data)
    elif pathname == '/userplayground':
        return playground.page
    elif pathname == '/2021data_1':
        return p21.dataset_1(data)
    elif pathname == '/signup':
        return create
    elif pathname == '/login':
        return login
    elif pathname == '/logged_in_user':
        return logged_in_user
    else:
        return 'Error 404'


if __name__ == '__main__':
    DEBUG = (os.getenv('DASH_DEBUG_MODE', 'False') == 'True')
    #DEBUG = True
    if DEBUG:
        app.run_server(debug=True, host='0.0.0.0') # Development 
    else:# prod
        serve(app.server, host="0.0.0.0", port="8050") 


# if __name__ == '__main__':
#     # DEBUG = (os.getenv('DASH_DEBUG_MODE', 'False') == 'True')
#    DEBUG = True
#    if DEBUG:
#         app.run_server(debug=True, host='0.0.0.0', port = "8051") # Development 
#    else:# prod
#         serve(app.server, host="0.0.0.0", port="8050") 
#         # remember to clear the cache-directory on startup in prod 


# if __name__ == '__main__':
#     # DEBUG = (os.getenv('DASH_DEBUG_MODE', 'False') == 'True')
#    DEBUG = True
#    if DEBUG:
#         app.run_server(debug=True, host='0.0.0.0') # Development 
#    else:# prod
#         serve(app.server, host="0.0.0.0", port="8051") 
#         # remember to clear the cache-directory on startup in prod  
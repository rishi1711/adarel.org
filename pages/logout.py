from ctypes import alignment
from turtle import color, width
from  dash import html
from  dash import dcc
import dash_bootstrap_components as dbc
from sqlalchemy import between
from app import app
from dash import html, ctx
from dash.dependencies import Input, Output, State
from database.models import Users_tbl
from database.models import engine
from database.models import Users
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, logout_user

#------------Main layout-----------------------------------------------------------------------------------------------------------------------------------------------
logout = dbc.Card([
            dbc.CardBody([dcc.Location(id='url_logout', refresh=True),
                html.Div("Do you really want to logout from your account?", 
                    style={'padding-bottom' : '2rem', 'font-weight' : 'normal', 'text-align' : 'left', 'width': '18rem'}),
                dbc.Row([
                    dbc.Col([
                        html.Button(id = 'yes', children = 'Yes', n_clicks=0, style= {'background-color' : '#009933', 'color' : 'white', 'border-radius' : '5px', 'border': 'none', 'width': '70px' }),
                    ]),
                    dbc.Col([
                        html.Button(id = 'no', children = 'No', n_clicks=0, style = {'background-color' : '#009933', 'color' : 'white', 'border-radius' : '5px', 'border': 'none','width': '70px'}),
                    ]),
                ], style={'padding-bottom' : '0.25rem' , 'padding-left' : '2.5rem'}),
            ])
], className='login-card')

@app.callback(
    Output('url_logout', 'pathname'),
    Input('yes', 'n_clicks'),
    Input('no', 'n_clicks'),
)
def logout_redirection(n1,n2):
    id = ctx.triggered_id
    if id == 'yes':
        logout_user()
        return '/'
    elif id == 'no':
        return 'first_page'
from ctypes import alignment
from turtle import color, width
from  dash import html
from  dash import dcc
import dash_bootstrap_components as dbc
from sqlalchemy import between
from app import app
from dash.dependencies import Input, Output, State
from database.models import Users_tbl
from database.models import engine
from database.models import Users
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user

login = dbc.Card([
            dbc.CardBody([dcc.Location(id='url_login', refresh=True),
                html.H2(''' Sign In ''', id='h1', style={'text-align' : 'center', 'color' : '#686868', 'font-size' : '3rem', 'padding-bottom' : '1rem'}),
                html.Div("Login to access previously created datasets and strategies", style={'padding-bottom' : '2rem', 'font-weight' : 'normal', 'color' : '#808080', 'text-align' : 'left', 'width': '18rem'}),
                dbc.Row([
                        dcc.Input(placeholder='Email Address here',
                        type='email',
                        id='uname-box',
                        style={'border-color' : '#D3D3D3', 'border-width' : '0.025px', 'border-radius' : '5px', 'height' : '30px'})
                ], style={'padding-bottom' : '0.25rem' }),
                dbc.Row([
                        dcc.Input(placeholder='Password',
                        type='password',
                        id='pwd-box',
                        style={'border-color' : '#D3D3D3', 'border-width' : '0.025px', 'border-radius' : '5px', 'height' : '30px'})
                ], style={'padding-bottom' : '0.75rem' }),
                dbc.Row([
                        html.Button(children='Login',
                        n_clicks=0,
                        type='submit',
                        id='login-button',
                        style= {'background-color' : '#009933', 'color' : 'white', 'border' : 'none', 'border-radius' : '5px', 'display' : 'inline-block', 'height' : '30px'})
                ]),
                html.Div(children='', id='output-state')
            ])
], className='login-card')

   
@app.callback(
    Output('url_login', 'pathname')
    , [Input('login-button', 'n_clicks')]
    , [State('uname-box', 'value'), State('pwd-box', 'value')])
def successful(n_clicks, input1, input2):
    user = Users.query.filter_by(username=input1).first()
    if user:
        # if user.password == input2:
        if check_password_hash(user.password, input2):
            login_user(user)
            return '/login_user_1'
        else:
            pass
    else:
        pass
@app.callback(
    Output('output-state', 'children')
    , [Input('login-button', 'n_clicks')]
    , [State('uname-box', 'value'), State('pwd-box', 'value')])
def update_output(n_clicks, input1, input2):
    if n_clicks > 0:
        user = Users.query.filter_by(username=input1).first()
        if user:
            #if user.password == input2:
            if check_password_hash(user.password, input2):
                return ''
            else:
                return 'Incorrect username or password'
        else:
            return 'Incorrect username or password'
    else:
        return ''
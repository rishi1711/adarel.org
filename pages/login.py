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

login =  html.Div([dcc.Location(id='url_login', refresh=True)
            , html.H2(''' Log In ''', id='h1'),
            dbc.Row([
                dbc.Col([
                    dcc.Input(placeholder='Enter your Email',
                    type='email',
                    id='uname-box')
                ], width=2, ),
                dbc.Col([
                    dcc.Input(placeholder='Enter your password',
                    type='password',
                    id='pwd-box')
                ], width=2),
                dbc.Col([
                    html.Button(children='Login',
                    n_clicks=0,
                    type='submit',
                    id='login-button')
                ], width=2),
            ]),
            html.Div(children='', id='output-state')
        ], className="notice-card") #end div
   
@app.callback(
    Output('url_login', 'pathname')
    , [Input('login-button', 'n_clicks')]
    , [State('uname-box', 'value'), State('pwd-box', 'value')])
def successful(n_clicks, input1, input2):
    user = Users.query.filter_by(username=input1).first()
    if user:
        # if user.password == input2:
        if check_password_hash(user.password, input2):
            #login_user(user)
            return '/logged_in_user'
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
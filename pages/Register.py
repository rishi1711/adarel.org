from distutils.log import error
from  dash import html
from  dash import dcc
import dash_bootstrap_components as dbc
from app import app
from dash.dependencies import Input, Output, State
from werkzeug.security import generate_password_hash, check_password_hash
from database.models import Users_tbl
from database.models import engine
from pages.login import login

create = html.Div([ dcc.Location(id='url_register', refresh=True),
        html.H1('Sign Up'),
       # , dcc.Location(id='create_user', refresh=True)
       dbc.Row([
            dbc.Col([
                dcc.Input(id="username"
                    , type="email"
                    , placeholder="Email")
            ], width=2),
            dbc.Col([
                dcc.Input(id="password"
                    , type="password"
                    , placeholder="password")
            ], width=2),
            dbc.Col([
                dcc.Input(id="companyName"
                    , type="text"
                    , placeholder="Company Name")
            ], width=2),
            dbc.Col([
                html.Button('Register', id='submit-val', n_clicks=0)
            ])
       ], style={"column-gap" : "40px"}),
        html.Div([html.H2('Already have a user account?', style={"font-size": '20px', "padding" : "4px"}), dcc.Link('Click here to Log In', href='/login')])
    ],className='notice-card')#end div


@app.callback(
    Output('url_register', "pathname")
    , [Input('submit-val', 'n_clicks')]
    , [State('username', 'value'), State('password', 'value'), State('companyName', 'value')])
def insert_users(n_clicks, un, pw, cn):
    if pw is not None:
        hashed_password = generate_password_hash(pw, method='pbkdf2:sha256', salt_length=16)
    if un is not None and pw is not None and cn is not None:
        ins = Users_tbl.insert().values(username=un,  password=hashed_password, companyName= cn)
        conn = engine.connect()
        conn.execute(ins)
        conn.close()
        return '/login'
    else:
        pass




   



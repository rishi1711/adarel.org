#For user to register

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
from database.models import Users

#--------------------Main Layout-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
create = dbc.Card([
            dbc.CardBody([dcc.Location(id='url_register', refresh=True),
                html.H1('Sign Up', style={'text-align' : 'center', 'color' : '#686868', 'font-size' : '3rem', 'padding-bottom' : '1rem'}),
                html.Div("Create an account so you can use our prediction modelson your own dataset and compare the results", 
                    style={'padding-bottom' : '2rem', 'font-weight' : 'normal', 'color' : '#808080', 'text-align' : 'left', 'width': '18rem'}),
                dbc.Row([
                    dcc.Input(id="firstname",
                        type="text",
                        placeholder="First Name",
                        style={'border-color' : '#D3D3D3', 'border-width' : '0.025px', 'border-radius' : '5px', 'height' : '30px'})
                ], style={'padding-bottom' : '0.25rem' }),
                dbc.Row([
                    dcc.Input(id="lastname",
                        type="text",
                        placeholder="Last Name",
                        style={'border-color' : '#D3D3D3', 'border-width' : '0.025px', 'border-radius' : '5px', 'height' : '30px'})
                ], style={'padding-bottom' : '0.25rem' }),

                dbc.Row([
                    dcc.Input(id="username",
                        type="email",
                        placeholder="Email Address",
                        style={'border-color' : '#D3D3D3', 'border-width' : '0.025px', 'border-radius' : '5px', 'height' : '30px'})
                ], style={'padding-bottom' : '0.25rem' }),
                dbc.Row([
                    dcc.Input(id="password",
                        type="password",
                        placeholder="Password",
                        style={'border-color' : '#D3D3D3', 'border-width' : '0.025px', 'border-radius' : '5px', 'height' : '30px'})
                ], style={'padding-bottom' : '0.25rem' }),
                dbc.Row([
                    dcc.Input(id="companyName",
                        type="text",
                        placeholder="Organization Name",
                        style={'border-color' : '#D3D3D3', 'border-width' : '0.025px', 'border-radius' : '5px', 'height' : '30px'})
                ], style={'padding-bottom' : '0.75rem' }),
                dbc.Row([
                    html.Div(id="value", style={'color' : '#ff0000'})
                ]),
                dbc.Row([
                     html.Button('Register', 
                        id='submit-val', 
                        n_clicks=0,
                        style= {'background-color' : '#009933', 'color' : 'white', 'border' : 'none', 'border-radius' : '5px', 'display' : 'inline-block', 'height' : '30px'})
                ])
            ])

], className='register-card')
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#--------Store the details in the database--------------------------------------------------------------------------------------
@app.callback(
    Output('url_register', "pathname"), Output('value', 'children')
    , [Input('submit-val', 'n_clicks')]
    , [State('firstname', 'value'), State('lastname', 'value'), State('username', 'value'), 
        State('password', 'value'), State('companyName', 'value')])
def insert_users(n_clicks, fn, ln, un, pw, cn):
    if pw is not None:
        hashed_password = generate_password_hash(pw, method='pbkdf2:sha256', salt_length=16)
        user = Users.query.filter_by(username=un).first()
    if fn is not None and ln is not None and un is not None and pw is not None and cn is not None:
        if user is None:
            ins = Users_tbl.insert().values(firstname=fn, lastname=ln, username=un,  password=hashed_password, companyName=cn)
            conn = engine.connect()
            conn.execute(ins)
            conn.close()
            return '/login', ""
        else:
            return '/signup', 'Email already exists'
    else:
         return '/signup', ""
#---------------------------------------------------------------------------------------------------------------------------------------


   



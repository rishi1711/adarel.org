
from operator import itemgetter
from turtle import width
from dash import dcc
from dash import html, ctx
import dash_bootstrap_components as dbc
from requests import session
from app import app
from dash.dependencies import Input, Output, State, ALL, MATCH
from tool.strategy_list import META_DATA_Val
import json
from database.models import Strategy
from database.models import strategy_tbl
from flask_login import current_user
from database.models import engine

strategy = html.Div([dcc.Location(id = 'new_path', refresh=True),
                html.H4("Try to create your own strategy"),
                dbc.Row([
                    dbc.Col([
                        html.Div([
                                dcc.Input(
                                    id='strategy_name',
                                    placeholder="Enter the Strategy name",
                                    type='text',
                                    required=True
                                )
                        ])
                    ], width=4),

                    dbc.Col([
                        html.Div([
                            dcc.Dropdown(
                                id ="ModelSelection", 
                                options=['SES','SVR', 'Holtwinter', 'Arima', 'Sarimax', 'GPR', 'NN', 'RF'],
                                placeholder = "Select Models"
                            )
                        ])
                    ], width=3), 

                    dbc.Col([
                        html.Div(
                            id= 'parameters',
                            children=[]
                        )
                    ])
                ], style={'column-gap' : '20px'}),
                html.Div(id = "list"),
                dbc.Row([
                        dbc.Col([
                                html.Button('Back to Home', id = 'go_login_home', n_clicks=0)
                            ])
                        ])
                ])

@app.callback(
    Output('new_path', 'pathname'),
    [Input('go_login_home', 'n_clicks')]
)
def go_to_login_home(nclicks):
    id = ctx.triggered_id
    if id == "go_login_home":
        if current_user.is_authenticated:
            return '/logged_in_user'
        else:
            pass
    else:
        pass


@app.callback(
    Output('parameters', 'children'),
    Input('ModelSelection', 'value'),
    State('parameters', 'children')
)
def set_parameters(value,children):
    if not value == None:      
        label, parameters, default, dropdown, required = itemgetter('label', 'parameters', 'default', 'dropdown', 'required')(META_DATA_Val[value])
        if parameters == None:
            children =  [html.Div("No extra parameters")]
            new_button = html.Div([
                            dbc.Col([
                                html.Button(children='Create',
                                    n_clicks=0,
                                    type='submit',
                                    id='strategy-button'
                                )
                            ])
                        ])
            children.append(new_button)
            return children
        else:
            i=0
            children = [html.Div("Enter the following parameters:")]
            for key in parameters:
                if parameters[key] == 'dropdown':
                    dropdown_values = dropdown[i]
                    v = default[i]
                    l = label[i]
                    i = i+1
                    new_dropdown =  html.Div([dbc.Row([
                                                dbc.Col([
                                                    html.Label(l)
                                                ]),
                                                dbc.Col([
                                                    dcc.Dropdown(
                                                        id= {
                                                            'type':'dropdown',
                                                            'index': key
                                                        },
                                                        options= dropdown_values,
                                                        value = v
                                                    )
                                                ])
                                            ])
                                    ])
                    children.append(new_dropdown)
                elif parameters[key] == 'input':
                    l = label[i]
                    v = default[i]
                    i = i+1
                    new_input =  html.Div([dbc.Row([
                                                dbc.Col([
                                                    html.Label(l)
                                                ]),
                                                dbc.Col([
                                                    dcc.Input(
                                                        id = {
                                                            'type':'input',
                                                            'index' : key
                                                        },
                                                        value = v
                                                    )
                                                ])
                                            ])
                                    ])
                    children.append(new_input)
                else:
                    l = label[i]
                    v = default[i]
                    i = i+1
                    new_tupple = html.Div([dbc.Row([
                                                
                                            html.Label(l)
                                                
                                        ], justify='between')
                                ])
                    children.append(new_tupple)
            new_button = html.Div([
                            dbc.Col([
                                html.Button(children='Create',
                                    n_clicks=0,
                                    type='submit',
                                    id='strategy-button'
                                )
                            ])
                        ])
            children.append(new_button)
            return children
    else:
        pass
        

@app.callback(
    Output('list', 'children'),
    [Input('strategy-button', 'n_clicks')],
    [State({'type' : 'dropdown', 'index':ALL}, 'value'),State({'type' : 'input', 'index':ALL}, 'value'), State('strategy_name', 'value'), State('ModelSelection', 'value'),],prevent_initial_call=True
)
def store_database(n_clicks, dropdown, input, strategy_name,value):
    if n_clicks > 0:
        parameters = itemgetter('parameters')(META_DATA_Val[value])
        obj = {}
        s_name = Strategy.query.filter_by(strategy_name = strategy_name).first()
        if value == 'SES':
            obj['name'] = value
        else:
            obj['name'] = value
            i=0
            for key in parameters:
                if parameters[key] == 'dropdown':
                    obj[key] = dropdown[i]
                elif parameters[key] == 'input':
                    obj[key] = input[i]
                    i=i+1   
                else:
                    pass
        json_obj = json.dumps(obj)
        # print(json_obj)
        if s_name == None:
            # print("1")
            ins = strategy_tbl.insert().values(user_id=current_user.get_id(), strategy_name = strategy_name, strategy_data = json_obj)
            # ins = strategy_tbl.update().where(strategy_tbl.c.user_id == current_user.get_id(), strategy_tbl.c.strategy_name == strategy_name).values(user_id=current_user.get_id(), strategy_name = strategy_name, strategy_data = json_obj)
        elif str(s_name.user_id) == current_user.get_id() and s_name.strategy_name == strategy_name:
            # print("2")
            ins = strategy_tbl.update().where(strategy_tbl.c.user_id == current_user.get_id(), strategy_tbl.c.strategy_name == strategy_name).values(user_id=current_user.get_id(), strategy_name = strategy_name, strategy_data = json_obj)
            # ins = strategy_tbl.insert().values(user_id=current_user.get_id(), strategy_name = strategy_name, strategy_data = json_obj)
        else:
            pass
        conn = engine.connect()
        conn.execute(ins)
        conn.close()
        return json_obj
    else:
        pass


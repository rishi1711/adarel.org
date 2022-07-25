from dash import dcc
from dash import html, ctx
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from app import app
from flask_login import current_user

login_user_2 = html.Div([dcc.Location(id = 'url_path_2', refresh=True),

    dbc.Row([
        html.H4("Training Data Result:-"),
        html.Div(id = "trigger"),
        dbc.Col([
            html.Div("The value of <Parameter1> is:", id = "p1"),
            html.Div("The value of <Parameter2> is:", id = "p2"),
        ]),
    ],class_name="notice-card"),

    dbc.Row([
        dbc.Col([
            html.Div([
                html.Button('Back', id = 'redirection_back', n_clicks=0),
            ])
        ]),
    ],class_name="notice-card")
    ])

@app.callback(
    Output(component_id='url_path_2', component_property='pathname'),
    [Input('redirection_back', 'n_clicks')],
    prevent_initial_callback = True
)
def redirect_to_page(n_clicks1):
    id = ctx.triggered_id
    if id == "redirection_back":
        if current_user.is_authenticated:
            return '/login_user_1'
        else:
            pass
    else:
        pass

    

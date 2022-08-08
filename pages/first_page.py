from dash import dcc, dash_table
from dash import html, ctx
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
from urllib.parse import quote as urlquote
from app import app
from flask_login import current_user
from flask import g
import sqlite3
import dash

#------------------------------------Front end of the logged-in user first page------------------------------------------------------------------------------------------------------------------------------------------#
first_page = html.Div([dcc.Location(id = 'url_new_page', refresh=True),
    dbc.Row([
            html.H1("My Workspace", style={'text-align' : 'left', 'color' : '#686868', 'font-size' : '3rem', 'padding-bottom' : '1rem', 'padding-top' : '40px'}),
            html.Div(id = "hi_statement"),
            html.Div("In your workspace, you are able to experiment diffrent prediction strategies." ,style={'text-align' : 'left', 'color' : '#686868', 'font-size' : '', 'padding-bottom' : '1rem'}),
            html.H3("Resume your Journey>"),
            html.Div("Below is the Dataset and Strategy that are associated with your account.", style={'text-align' : 'left', 'color' : '#686868', 'font-size' : '', 'padding-bottom' : '1rem'}),
    ]),
    dbc.Row([
        dbc.Col([
            html.H3("My Data"),
            html.Div("Below shows the dataset linked with your account. Here you can see the name of the dataset and also its type."),
            dash_table.DataTable(id = 'datalist'),
            html.Button("Create New Data", 
                        id = 'create_data', 
                        n_clicks=0,
                        style= {'background-color' : '#714FFF', 'color' : 'white', 'border' : 'none', 'border-radius' : '5px', 'display' : 'inline-block', 'height' : '30px', 'margin-left' : '450px'}),
        ]),
        dbc.Col([
            html.H3("My Strategies"),
            html.Div("Below shows the strategies linked with your account. Any of these Strategies can be used on selected dataset."),
            dash_table.DataTable(id = 'strat_tbl'),
            html.Button("Create New Strategy", 
                        id = 'create_strat', 
                        n_clicks=0,
                        style= {'background-color' : '#714FFF', 'color' : 'white', 'border' : 'none', 'border-radius' : '5px', 'display' : 'inline-block', 'height' : '30px', 'margin-left' : '440px' }),
        ]),
    ]),
    dbc.Row([
        html.Button("Create New Predictions >", 
                    id = 'create_pred', 
                    n_clicks=0,
                    style= {'background-color' : '#009933', 'color' : 'white', 'border-radius' : '5px'}
                    ),
    ],class_name='button-style'),
    ], style = {'padding-bottom' : '6rem'})
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#


#------------------------------------Show the datasets and strategies associated with the user account in the form of table-------------------------------------------------------------------------------------------------------------#
@app.callback(
    Output('hi_statement', 'children'),
    Output('datalist', 'data'),
    Output('strat_tbl', 'data'),
    Input('create_pred', 'nclicks'),
)
def showdata(nclicks):
    conn = sqlite3.connect("./database/data.sqlite")
    firstname = pd.read_sql("""select firstname from user where id = '{}'""".format(current_user.get_id()), conn)
    name = firstname["firstname"].loc[0]
    data = "Hi " + name + "!"

    datasets = pd.read_sql("""select filename, filetype from files where user_id = '{}'""".format(current_user.get_id()), conn)
    datasets = datasets.to_dict('records')
    # df = datasets
    # df1 = pd.DataFrame(columns = ['Dataset Name', 'Training', 'Testing'])
    # len(df1)
    # if df is not None:
    #     for index in df.index:
    #         temp = pd.read_sql("""select datasetname, filetype from files where user_id = '{}' and datasetname = '{}'""".format(current_user.get_id(), df['datasetname'][index]), conn) 
    #         if len(temp) == 2:
    #             df1.loc[len(df1.index)] = [temp['datasetname'].loc[0], temp['datasetname'].loc[0] + "_Training", temp['datasetname'].loc[0] + "_Testing"]  
    #             df = df.drop(df[df['datasetname'] == temp['datasetname'].loc[0]].index, inplace = True)
    # df1 = df1.to_dict('records')

    stratdf = pd.read_sql("""select strategy_name, strategy_data from strategy where user_id = '{}'""".format(current_user.get_id()), conn)
    strategy = stratdf.to_dict('records')
    return data, datasets, strategy
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#


#-----------------------------------Redirect the user to different page-----------------------------------------------------------------------------------------------------------------------------------------------------------------#
@app.callback(
    Output('url_new_page','pathname'),
    [Input('create_strat', 'n_clicks'),
    Input('create_pred', 'n_clicks'),
    Input('create_data', 'n_clicks'),],
    prevent_initial_callback = True
)
def redirect_to_new_page(nclick1, nclick2, nclicks3):
    id = ctx.triggered_id
    if id == "create_strat":
        if current_user.is_authenticated:
            return '/strategy'
        else:
            pass
    elif id == "create_pred":
        if current_user.is_authenticated:
            return '/login_user_1'
        else:
            pass
    elif id == "create_data":
        return '/create_data'
    else:
        pass
    return dash.no_update
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#





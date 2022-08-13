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
import json

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
                        style= {'background-color' : '#714FFF', 'color' : 'white', 'border' : 'none', 'border-radius' : '5px', 'display' : 'inline-block', 'height' : '30px', 'margin-left' : '250px'}),
        ]),
        dbc.Col([
            html.H3("My Strategies"),
            html.Div("Below shows the strategies linked with your account. Any of these Strategies can be used on selected dataset."),
            dash_table.DataTable(id = 'strat_tbl'),
            html.Button("Create New Strategy", 
                        id = 'create_strat', 
                        n_clicks=0,
                        style= {'background-color' : '#714FFF', 'color' : 'white', 'border' : 'none', 'border-radius' : '5px', 'display' : 'inline-block', 'height' : '30px', 'margin-left' : '250px' }),
        ]),
    ]),

    dbc.Row([
        dbc.Col([
            html.H3("My Previous Predictions"),
            html.Div("Below shows the list of predictions that you have made before. For viewing previous predictions, click on that particular cell of the [Dataset Name] column."),
            dash_table.DataTable(id = 'predictions'),
        ]),
    ]),

    dbc.Row([
        html.Button("Create New Predictions >", 
                    id = 'create_pred', 
                    n_clicks=0,
                    style= {'background-color' : '#009933', 'color' : 'white', 'border-radius' : '5px', 'border': 'none', 'width':'500px', 'height':'32px'}
                    ),
    ],class_name='button-style'),
    ], style = {'padding-bottom' : '6rem'})
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#


#------------------------------------Show the datasets and strategies associated with the user account in the form of table-------------------------------------------------------------------------------------------------------------#
@app.callback(
    [Output('hi_statement', 'children'), Output('datalist', 'data'), Output('strat_tbl', 'data'),
    Output('predictions', 'data'), Output('dataframe_prediction', 'data')],
    Input('create_pred', 'nclicks'),
)
def showdata(nclicks):
    conn = sqlite3.connect("./database/data.sqlite")
    firstname = pd.read_sql("""select firstname from user where id = '{}'""".format(current_user.get_id()), conn)
    name = firstname["firstname"].loc[0]
    data = "Hi " + name + "!"

    datasets = pd.read_sql("""select filename, filetype from files where user_id = '{}'""".format(current_user.get_id()), conn)
    datasets = datasets.to_dict('records')
    
    strategy_name = pd.read_sql("""select strategy_name from strategy where user_id = '{}'""".format(current_user.get_id()), conn)
    strat_data = pd.read_sql("""select strategy_data from strategy where user_id = '{}'""".format(current_user.get_id()), conn)
    predictions = pd.read_sql("""select * from PreviousPredictions where user_id = '{}'""".format(current_user.get_id()), conn)
    s= []
    d = []
    f0 = []
    f1 = []
    f2 = []
    m = []
    r = []
    s_i =[] 
    for i in predictions.values:
        strategyName = pd.read_sql("""select strategy_id, strategy_name from strategy where strategy_id = '{}'""".format(i[1]), conn)
        s_data = pd.read_sql("""select strategy_data from strategy where strategy_id = '{}'""".format(i[1]), conn)
        file = pd.read_sql("""select file_id, datasetname, filepath from files where file_id = '{}'""".format(i[3]), conn)
        mae = i[4]
        rmse = i[5]
        s.append(strategyName.values[0][1])
        d.append(s_data.values[0][0])
        f0.append(file.values[0][0])
        f1.append(file.values[0][1])
        f2.append(file.values[0][2])
        m.append(mae)
        r.append(rmse)
        s_i.append(strategyName.values[0][0])
    s_name = pd.DataFrame(s, columns = ['Strategy Name'])
    s_data = pd.DataFrame(d, columns = ['Strategy Data'])
    d_name = pd.DataFrame(f1, columns = ['Dataset Name'])
    d_path = pd.DataFrame(f2, columns = ['Dataset Path'])
    mae = pd.DataFrame(m, columns = ['MAE'])
    rmse = pd.DataFrame(r, columns = ['RMSE'])
    file_id = pd.DataFrame(f0, columns = ['File Id'])
    strategy_id = pd.DataFrame(s_i, columns = ['Strategy Id'])
    df = pd.concat([d_name,s_name, s_data, mae, rmse], axis=1)
    df1 = pd.concat([d_name, d_path, s_name, s_data, mae, rmse, file_id, strategy_id], axis=1)
    predictions = df.to_dict('records')
    df1 = df1.to_dict('records')

    l = []
    for i in strat_data["strategy_data"]:
        temp = json.loads(str(i))
        temp = list(temp.values())
        l.append(str(temp))

    strategy_data = pd.DataFrame(l, columns = ['Strategy Data'])

    strategy = pd.concat([strategy_name, strategy_data], join = 'outer', axis = 1)
    strategy = strategy.to_dict('records')
    return data, datasets, strategy, predictions, df1
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#


#-----------------------------------Redirect the user to different page-----------------------------------------------------------------------------------------------------------------------------------------------------------------#
@app.callback(
    [Output('url_new_page','pathname'), Output('strategy_id', 'data'), Output('testing_id', 'data')],
    [Input('create_strat', 'n_clicks'),
    Input('create_pred', 'n_clicks'),
    Input('create_data', 'n_clicks'),
    Input('predictions', 'active_cell')],
    State('dataframe_prediction', 'data'),
    prevent_initial_callback = True
)
def redirect_to_new_page(nclick1, nclick2, nclicks3, active_cell, df):
    id = ctx.triggered_id
    if id == "predictions":
        columnName = active_cell['column_id']
        if columnName == 'Dataset Name':
            row = active_cell['row']
            file_id = df[row]['File Id']
            strategy_id = df[row]['Strategy Id']
            return '/previous_prediction', strategy_id, file_id
        else:
            pass
    elif id == "create_strat":
        if current_user.is_authenticated:
            return '/strategy', None, None
        else:
            pass
    elif id == "create_pred":
        if current_user.is_authenticated:
            return '/login_user_1', None, None
        else:
            pass
        
    elif nclicks3>0 and id == "create_data":
        return '/create_data', None, None
    else:
        pass
    return dash.no_update
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#




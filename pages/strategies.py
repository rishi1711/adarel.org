from operator import itemgetter
from turtle import width
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from app import app
from dash.dependencies import Input, Output, State
from tool.strategy_list import META_DATA_Val

strategy = html.Div([dcc.Location(id = 'url_new', refresh=True),
                html.H4("Try to create your own strategy"),
                dbc.Row([
                    dbc.Col([
                        html.Div([
                                dcc.Input(
                                    id='strategy_name',
                                    placeholder="Enter the Strategy name",
                                    type='text'
                                )
                        ])
                    ], width=4),

                    dbc.Col([
                        html.Div([
                            dcc.Dropdown(
                                id ="Model Selection", 
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
            ])


@app.callback(
    Output('parameters', 'children'),
    Input('Model Selection', 'value'),
    State('parameters', 'children')
)
def set_parameters(value,children):
    if not value == None:
        
        label, parameters, default, dropdown, required = itemgetter('label', 'parameters', 'default', 'dropdown', 'required')(META_DATA_Val[value])
        if parameters == None:
            return html.Div("No extra parameters")
        else:
            i=0
            children = [html.Div("Enter the following parameters:")]
            print(children)
            for key in parameters:
                if parameters[key] == 'dropdown':
                    dropdown_values = dropdown[i]
                    v = default[i]
                    l = label[i]
                    i = i+1
                    # new_label = html.Label(l)
                    # children.append(new_label)
                    new_dropdown =  html.Div([dbc.Row([
                                                dbc.Col([
                                                    html.Label(l)
                                                ]),
                                                dbc.Col([
                                                    dcc.Dropdown(
                                                        id= key,
                                                        options= dropdown_values,
                                                        value = v
                                                    )
                                                ])
                                            ])
                                    ])
                    children.append(new_dropdown)
                else:
                    l = label[i]
                    v = default[i]
                    i = i+1
                    new_input =  html.Div([dbc.Row([
                                                dbc.Col([
                                                    html.Label(l)
                                                ]),
                                                dbc.Col([
                                                    dcc.Input(
                                                        id = key,
                                                        type='number',
                                                        value = v
                                                    )
                                                ])
                                            ])
                                    ])
                                # [dbc.Row([
                    #                 dbc.Col([
                    #                     html.Label(l)
                    #                 ]),
                    #             dbc.Col([
                    #                 dcc.Input(
                    #                     id = key,
                    #                     type='number',
                    #                     value = v
                    #                 )
                    #             ])
                    #         ])]
                    children.append(new_input)
            print(children)
            return children

        # print(label)
        # print(parameters)
        # print(default)
        # print(required)
        # print(dropdown)
    else:
        pass
        



    # if value == 'SVR':
    #     return html.Div([
    #                 dbc.Row([
    #                     dbc.Col([
    #                         html.Label("Select the kernel value")
    #                     ]),
    #                     dbc.Col([
    #                         dcc.Dropdown(
    #                             id='kernel',
    #                             options= ['linear', 'poly', 'rbf', 'sigmoid', 'precomputed'],
    #                             value = 'linear'
    #                         )
    #                     ])
    #                 ]),
    #                 dbc.Row([
    #                     dbc.Col([
    #                         html.Label("Insert value of C")
    #                     ]),
    #                     dbc.Col([
    #                         dcc.Input(
    #                             id = 'C',
    #                             type='text',
    #                             value = '0.1'
    #                         )
    #                     ])
    #                 ]),
    #                 dbc.Row([
    #                     dbc.Col([
    #                         html.Label("Insert value of gamma")
    #                     ]),
    #                     dbc.Col([
    #                         dcc.Input(
    #                             id = 'gamma',
    #     #                       placeholder= 'Insert value of gamma',
    #                             type = 'text',
    #                             value = '0.1'
    #                         ),
    #                     ])
    #                 ]),
    #                 dbc.Row([
    #                     dbc.Col([
    #                         html.Label("Insert value of epsilon")
    #                     ]),
    #                     dbc.Col([
    #                         dcc.Input(
    #                             id= 'epsilon',
    #                             type = 'text',
    #                             value = '0.0001'
    #                         )
    #                     ])
    #                 ]),
    #            ]) 

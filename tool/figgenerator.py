import click
from matplotlib import legend_handler
from matplotlib.legend import Legend
from matplotlib.pyplot import legend
import pandas as pd
import numpy as np
import plotly.graph_objects as go

import tool.datapaths as dp
from tool.datapathscsv import META_DATA_CSV
from typing import List, Union
from operator import itemgetter

META_DATA = dp.META_DATA

def get_fig_from_csv(dataset_name: str, data: list) -> go.Figure:

    fig = go.Figure()
    available_mods, file_path = itemgetter('available_models', 'path')(META_DATA_CSV[dataset_name])
    df = pd.read_csv(file_path)
    true_vals = df['true value'].to_numpy()
    x_tick = df.iloc[:,0]
    fig.add_trace( go.Scatter(
        x = x_tick,
        y = true_vals,
        mode = 'lines',
        name = 'true value'
    ))

    if not data == None:
        for mod in available_mods:  
            if mod in data:
                ys = df[mod].to_numpy()
                fig.add_trace( go.Scatter(
                    x = x_tick,
                    y = ys,
                    mode = 'lines',
                    name = mod
                ))
            else:
                ys = df[mod].to_numpy()
                fig.add_trace( go.Scatter(
                    x = x_tick,
                    y = ys,
                    mode = 'lines',
                    name = mod,
                    visible = "legendonly"
                ))
    else:
        for mod in available_mods:  
            ys = df[mod].to_numpy()
            fig.add_trace( go.Scatter(
                x = x_tick,
                y = ys,
                mode = 'lines',
                name = mod
            ))
    return fig

def get_fig_from_custom_csv(dataset_path, strategy_name) -> go.Figure:

    fig = go.Figure()
    df = pd.read_csv(dataset_path)
    true_vals = df['true value'].to_numpy()
    x_tick = df.iloc[0:,0]
    fig.add_trace( go.Scatter(
        x = x_tick,
        y = true_vals[0:],
        mode = 'lines',
        name = 'true value'
    ))

    strategy_vals = df[strategy_name].to_numpy()
    x_tick = df.iloc[0:,0]
    fig.add_trace( go.Scatter(
        x = x_tick,
        y = strategy_vals[0:],
        mode = 'lines',
        name = strategy_name
    ))

    return fig

def get_fig(dataset_name: str) -> go.Figure:
    fig = go.Figure()
    available_mods_obj = itemgetter('available_models')(META_DATA[dataset_name])
    true_vals = get_true_values(dataset_name)
    fig.add_trace( go.Scatter(
        x = [*range(len(true_vals))],
        y = true_vals,
        mode= 'lines',
        name= 'true values'
    ))

    for model, sheet_num in available_mods_obj.items():
        ys = get_prediction_points(dataset_name, sheet_num)
        fig.add_trace(go.Scatter(
            x= [*range(1, len(ys))],
            y = ys,
            mode= 'lines',
            name= model
        ))
    
    return fig

def get_true_values(name: str) -> np.ndarray:
    assert name in META_DATA

    path = itemgetter('path')(META_DATA[name])
    df = pd.read_excel(path, engine = 'openpyxl', sheet_name=0, header =1)
    return df['true value'].to_numpy()

def get_prediction_points(name: str, sheet_num: int, with_ad: bool=False) -> np.ndarray:
    assert name in META_DATA

    path = itemgetter('path')(META_DATA[name])
    df = pd.read_excel(path, engine = 'openpyxl', sheet_name=sheet_num, header=1)
    col_name = "prediction" if not with_ad else "pred\nwo anomaly detection"

    return df[col_name].to_numpy()

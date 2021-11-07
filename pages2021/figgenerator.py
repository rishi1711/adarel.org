import pandas as pd
import numpy as np
import plotly.graph_objects as go

import pages2021.datapaths as dp

from typing import List, Union
from operator import itemgetter

META_DATA = dp.META_DATA


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

if __name__ == "__main__":
    # path = itemgetter('path')(META_DATA['DataSet1'])
    # df = pd.read_excel(path, engine='openpyxl', sheet_name=2, header=1)

    # print(df.iloc[:4, :7])
    # result = get_prediction_points('DataSet1', 0)
    # print(result)
    print(get_fig("DataSet1"))
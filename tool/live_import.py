#############
# for local test
#############
import fetchData
from statsmodels.tsa.api import ExponentialSmoothing, SimpleExpSmoothing, Holt
import numpy as np
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import plotly.graph_objects as go

def gen_plot_forecast():
    es_conn = fetchData.elasticSearch(url="https://kibanaadmin:kibana@kf6-stage.ikit.org/es/_search")
    df = es_conn.get_nginx_reliability(interval='1h')
    data_in_window = df.tail(1000)
    rel_data = data_in_window["reliability"].to_numpy()
    if np.isnan(np.sum(rel_data)):
        print("NaN in data")
        exit(1)
    simple_exp_model = SimpleExpSmoothing(rel_data).fit(smoothing_level=.5)
    predicted_data = np.average(simple_exp_model.forecast(5))
    fitted_values = simple_exp_model.fittedvalues
    fig = go.figure()
    fig.add_trace(go.Scatter(x=range(1, len(rel_data)),
                    y=rel_data,
                    mode='lines',
                    name="Data in window"))
    fig.add_trace(go.Scatter(x=range(1, len(fitted_values)),
                    y=fitted_values,
                    mode='lines',
                    name="Previous Predictions"))
    return fig, predicted_data


fig, predicted_data = gen_plot_forecast()

"""
plt.plot(rel_data)
simple_exp_model = SimpleExpSmoothing(rel_data).fit(smoothing_level=.5)
#fit4 = ExponentialSmoothing(rel_data, seasonal_periods=4, trend='add', seasonal='mul', damped=True).fit(use_boxcox=True)
predicted_data = simple_exp_model.forecast(50)
#predicted_data = fit4.forecast(100)
#style='--', marker='o', color='green', legend=True
print(predicted_data)
#plt.plot(predicted_data)
#plt.show()
plt.plot(simple_exp_model.fittedvalues)
plt.show()
print(len(predicted_data))
"""

import fetchData
from statsmodels.tsa.api import ExponentialSmoothing, SimpleExpSmoothing, Holt

def data():
    lol = pd.read_csv("raw_data/ds3.csv") 
    fig = go.Figure()
    plots=['truth_value','adarel','sarima', 'SVR','Gaussian']
    for plot in plots:
        fig.add_trace(go.Scatter(x=range(1, len(lol[plot].to_numpy())),
                    y=lol[plot].to_numpy(),
                    mode='lines',
                    name=plot))
    return fig


es_conn = fetchData.elasticSearch(url="https://kibanaadmin:kibana@kf6-stage.ikit.org/es/_search")
df = es_conn.get_nginx_reliability(interval='1h')
last_3k_values = df.tail(3000)
rel_data =last_3k_values["reliability"]

fit4 = ExponentialSmoothing(saledata, seasonal_periods=4, trend='add', seasonal='mul', damped=True).fit(use_boxcox=True)
fit4.forecast(12).plot(style='--', marker='o', color='green', legend=True)
plt.show()
from statsmodels.tsa.holtwinters import SimpleExpSmoothing
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.arima.model import ARIMA
from sklearn.svm import SVR
import pandas as pd
import numpy as np

def predictOnSelectedModel(datasetPath, strategyName, strategyData):
    df = pd.read_csv(datasetPath, encoding='utf-8') 
    columnName = strategyName
    if strategyData['name'] == 'SES':
        for i in range(1000,len(df)):
            train = df.iloc[0:i]
            model = SimpleExpSmoothing(train['true value']).fit()
            data = np.array(model.forecast())
            df.loc[df.index[i], columnName] = data[0]

    elif strategyData['name'] == 'Holtwinter':
        trend = strategyData['trend']
        seasonal = strategyData['seasonal']
        seasonality_periods = strategyData['seasonality_periods']
        seasonality_periods = int(seasonality_periods)
        for i in range(1000,len(df)):
            train = df.iloc[0:i]
            model =  ExponentialSmoothing(train['true value'], trend= trend, seasonal = seasonal, seasonal_periods = seasonality_periods).fit()
            data = np.array(model.forecast())
            df.loc[df.index[i], columnName] = data[0]

    elif strategyData['name'] == 'Arima':
        a = int(strategyData['Autoregressive'])
        b = int(strategyData['Difference'])
        c = int(strategyData['Moving Average Component'])
        order1 = (a,b,c)
        for i in range(1000,len(df)):
            train = df.iloc[0:i]
            model =  ARIMA(train['true value'], order = order1).fit()
            data = np.array(model.forecast())
            print(data)
            df.loc[df.index[i], columnName] = data[0]

    elif strategyData['name'] == 'Sarimax':
        a = int(strategyData['Autoregressive'])
        b = int(strategyData['Difference'])
        c = int(strategyData['Moving Average Component'])
        order1 = (a,b,c)
        a = int(strategyData['AR parameters'])
        b = int(strategyData['Diffrences'])
        c = int(strategyData['MA parameters'])
        d = int(strategyData['Periodicity'])
        seasonal_order1 = (a,b,c,d)
        for i in range(1000,len(df)):
            train = df.iloc[0:i]
            model =  ARIMA(train['true value'], order = order1, seasonal_order = seasonal_order1).fit()
            data = np.array(model.forecast())
            print(data)
            df.loc[df.index[i], columnName] = data[0]
            
    print(df)
    df.to_csv(datasetPath, index=True)



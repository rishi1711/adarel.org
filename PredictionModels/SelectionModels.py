# For training and testing of the models

from statsmodels.tsa.holtwinters import SimpleExpSmoothing
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.arima.model import ARIMA
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, WhiteKernel
from sklearn.metrics import mean_squared_error
from math import sqrt
import pandas as pd
import numpy as np

#------- Differentiate between whether it is for training or for testing and calls the method accordingly---------------------------------------------------------------- 
def predictOnSelectedModel(datasetPath_train, datasetPath_test, strategyName, strategyData, type):
    df = pd.read_csv(datasetPath_train, encoding='utf-8') 
    columnName = strategyName
    if type == "training":
        # Use 70% for training and 30% for validation
        index = int((len(df) * 70) / 100)
        df = train_models(df, index, strategyData, strategyName)
        #Get the true values till the end of training dataset
        value1 = df['true value'].iloc[index : len(df)]
        #get the predicted values for the same
        value2 = df[columnName].iloc[index : len(df)]
        #calculate the absolute error among true value and prediction points 
        summary = get_prediction(value1, value2)
        #calculate mean absolute error
        mae = calculate_mae(value1, value2)
        #calculate root mean squared error
        rmse = calculate_rmse(value1, value2)
        return [mae, rmse, summary]
    elif type == "testing":
        df2 = pd.read_csv(datasetPath_test, encoding='utf-8') 
        index2 = len(df)
        #concatenate training and testing dataset
        dataset = pd.concat([df, df2], ignore_index=True)
        #training the models and providing index from which prediction should start
        dataset = train_models(dataset, index2, strategyData, strategyName)
        d1 = dataset[columnName].iloc[index2:]
        d1 = d1.reset_index()
        #Dropping the unwanted columns generated after concatenation
        if columnName in df2.columns:
            df2.drop([columnName], axis=1, inplace=True)
        df2 = pd.concat([df2, d1], axis=1)
        df2.drop(['index'], axis=1, inplace=True)
        df = df2

    # Writing back to the csv file 
    df_col = list(df.columns)
    if "Unnamed" not in df_col[0]:
        df.to_csv(datasetPath_test, index=True)
    else:
        df.to_csv(datasetPath_test, index=False)   
#------------------------------------------------------------------------------------------------------------------------------

#-----Function to train the model using training data and then predicting the values of testing dataset
def train_models(df, index, strategyData, columnName):
    if strategyData['name'] == 'SES':
        for i in range(index,len(df)):
            train = df.iloc[0:i+1]
            #training the model
            model = SimpleExpSmoothing(train['true value']).fit()
            #predicting the values
            data = np.array(model.forecast())
            # storing in the dataframe
            df.loc[df.index[i], columnName] = data[0]
        return df

    elif strategyData['name'] == 'Holtwinter':
        #getting the prarmeters from the json object startegyData
        trend = strategyData['trend']
        seasonal = strategyData['seasonal']
        seasonality_periods = strategyData['seasonality_periods']
        seasonality_periods = int(seasonality_periods)
        for i in range(index,len(df)):
            train = df.iloc[0:i+1]
            #training the model
            model =  ExponentialSmoothing(train['true value'], trend= trend, seasonal = seasonal, seasonal_periods = seasonality_periods).fit()
             #predicting the values
            data = np.array(model.forecast())
            # storing in the dataframe
            df.loc[df.index[i], columnName] = data[0]
        return df

    elif strategyData['name'] == 'Arima':
        #getting the prarmeters from the json object startegyData
        a = int(strategyData['Autoregressive'])
        b = int(strategyData['Difference'])
        c = int(strategyData['Moving Average Component'])
        order1 = (a,b,c)
        for i in range(index,len(df)):
            train = df.iloc[0:i+1]
            #training the model
            model =  ARIMA(train['true value'], order = order1).fit()
             #predicting the values
            data = np.array(model.forecast())
            # storing in the dataframe
            df.loc[df.index[i], columnName] = data[0] 
        return df   

    elif strategyData['name'] == 'Sarimax':
        #getting the prarmeters from the json object startegyData
        a = int(strategyData['Autoregressive'])
        b = int(strategyData['Difference'])
        c = int(strategyData['Moving Average Component'])
        #creating a tupple manually
        order1 = (a,b,c)
        a = int(strategyData['AR parameters'])
        b = int(strategyData['Diffrences'])
        c = int(strategyData['MA parameters'])
        d = int(strategyData['Periodicity'])
        #creating a tupple manually
        seasonal_order1 = (a,b,c,d)
        for i in range(index,len(df)):
            train = df.iloc[0:i+1]
            #training the model
            model =  ARIMA(train['true value'], order = order1, seasonal_order = seasonal_order1).fit()
             #predicting the values
            data = np.array(model.forecast())
            print(data)
            # storing in the dataframe
            df.loc[df.index[i], columnName] = data[0]
        return df

    elif strategyData['name'] == 'SVR':
        #getting the prarmeters from the json object startegyData
        a = strategyData['kernel']
        b = float(strategyData['C'])
        c = float(strategyData['gamma'])
        d = float(strategyData['epsilon'])
        for i in range(index,len(df)):
            #original true values from start
            trainX = df['true value'].iloc[0:i].values
            # next true value beiginning from second element
            trainY = df['true value'].iloc[1:i+1].values
            trainX = trainX.reshape(-1,1)
            trainY = trainY.reshape(-1,1)
            #training the model
            model = SVR(kernel=a, C=b, gamma=c, epsilon=d).fit(trainX, trainY)
             #predicting the values
            data = np.array(model.predict([[df['true value'].iloc[i]]]))
            print(data)
            # storing in the dataframe
            df.loc[df.index[i], columnName] =  data[0]    
        return df    
    
    elif strategyData['name'] == 'RF':
        #getting the prarmeters from the json object startegyData
        a = int(strategyData['n_estimators'])
        b = int(strategyData['max_depth'])
        c = int(strategyData['random_state'])
        for i in range(index,len(df)):
            #original true values from start
            trainX = df['true value'].iloc[0:i].values
            # next true value beiginning from second element
            trainY = df['true value'].iloc[1:i+1].values
            trainX = trainX.reshape(-1,1)
            trainY = trainY.reshape(-1,1)
            #training the model
            model = RandomForestRegressor(n_estimators=a, max_depth=b, random_state=c).fit(trainX, trainY)
             #predicting the values
            data = np.array(model.predict([[df['true value'].iloc[i]]]))
            print(data)
            # storing in the dataframe
            df.loc[df.index[i], columnName] = data[0]
        return df
    
    elif strategyData['name'] == 'NN':
        #getting the prarmeters from the json object startegyData
        a = strategyData['activation']
        b = strategyData['solver']
        c = eval(strategyData['hidden_layer_sizes'])
        d = float(strategyData['alpha'])
        e = float(strategyData['learning_rate_init'])
        f = int(strategyData['random_state'])
        print(a,b,c,d,e,f)
        for i in range(index,len(df)):
            #original true values from start
            trainX = df['true value'].iloc[0:i].values
            # next true value beiginning from second element
            trainY = df['true value'].iloc[1:i+1].values
            trainX = trainX.reshape(-1,1)
            trainY = trainY.reshape(-1,1)
            #training the model
            model = MLPRegressor(hidden_layer_sizes=c, alpha=d, activation=a, solver=b, learning_rate_init=e, random_state=f).fit(trainX, trainY)
             #predicting the values
            data = np.array(model.predict([[df['true value'].iloc[i]]]))
            print(data)
            # storing in the dataframe
            df.loc[df.index[i], columnName] = data[0]
        return df
    
    elif strategyData['name'] == 'GPR':
        #getting the prarmeters from the json object startegyData
        a = float(strategyData['alpha'])
        b = float(strategyData['RBF_Coefficient'])
        c = float(strategyData['length_scale'])
        d = float(strategyData['WhiteKernel_coefficient'])
        e = float(strategyData['noise_level'])
        f = eval(strategyData['noise_level_bounds'])
        kernel = b * RBF(length_scale=c) + d * WhiteKernel(noise_level=e, noise_level_bounds=f)
        for i in range(index,len(df)):
            print(i)
            train = df.iloc[0:i+1]
            #original true values from start
            trainX = df['true value'].iloc[0:i].values
            # next true value beiginning from second element
            trainY = df['true value'].iloc[1:i+1].values
            trainX = trainX.reshape(-1,1)
            trainY = trainY.reshape(-1,1)
            #training the model
            model = GaussianProcessRegressor(kernel=kernel, alpha=a).fit(trainX, trainY)
             #predicting the values
            data = np.array(model.predict([[df['true value'].iloc[i]]]))
            print(data)
            # storing in the dataframe
            df.loc[df.index[i], columnName] = data[0]
        return df
    else:
        pass
#--------------------------------------------------------------------------------------------------------------------------------------

#--------Calculate the mean absolute error---------------------------------------------------------------------------
def calculate_mae(value1, value2):
    aes = np.array([abs(u - v) for u, v in zip(value1, value2)])
    mae = np.average(aes)
    return mae
#----------------------------------------------------------------------------------------

#-------------Calculate the root mean squared error--------------------------------------------------------------------------
def calculate_rmse(value1, value2):
    rmse =  sqrt(mean_squared_error(value1,value2))
    return rmse
#---------------------------------------------------------------------------------------------------------

#-----Calulate the absolute error and divide them into the respected categories which will be used to display summary graph--------------------------------------------------------
def get_prediction(value1, value2):
    aes = np.array([abs(u - v) for u, v in zip(value1, value2)])
    cnt1 = [0] * 9
    for i in aes:
        if i>=0 and i<=0.0005:
            cnt1[0] += 1
        elif i>0.0005 and i<=0.001:
            cnt1[1] += 1
        elif i>0.001 and i<=0.005:
            cnt1[2] += 1   
        elif i>0.005 and i<=0.01:
            cnt1[3] += 1
        elif i>0.01 and i<=0.05:
            cnt1[4] += 1
        elif i>0.05 and i<=0.1:
            cnt1[5] += 1
        elif i>0.1 and i<=0.5:
            cnt1[6] += 1
        elif i>0.5 and i<=1:
            cnt1[7] += 1
        else:
            cnt1[8] += 1
    return cnt1
        

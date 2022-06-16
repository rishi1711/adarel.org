META_DATA_Val = {
    'SES':{
        'name' : 'Simple Exponential Smoothing',
        'label' : None,
        'parameters' : None,
        'default' : None,
        'dropdown' : None,
        'required' : None
    },
    'Holtwinter': {
        'name' : 'Holtwinter',
        'label' : ["Select the trend", "Select the seasonal", "Select the seasonality_periods"],
        'parameters' : {'trend' : 'dropdown', 'seasonal' : 'dropdown', 'seasonality_periods' : 'int'},
        'default' : ['add', 'add', '0'],
        'dropdown' : [['add', 'mul', 'additive', 'multiplicative', None], ['add', 'mul', 'additive', 'multiplicative', None]],
        'required' : ['seasonality_periods']
    },
    'Arima' : {
        'name' : 'Arima',
        'parameters' : {'order' : (0,0,0)}
    },
    'Sarimax' : {
        'name' : 'Sarimax',
        'parameters' : {'order' : (0,0,0), 'seasonal_order' : (0,0,1,24)}
    },
    'SVR' : {
        'name' : 'Support Vector Machine Regressor',
        'parameters' : {'kernel' : 'linear', 'C' : '0.1', 'gamma' : '0.1', 'epsilon' : '0.0001'}
    },
    'GPR' : {
        'name' : 'Gaussian Process Regression',
        'parameters' : {'kernel' : '0.35 * RBF(length_scale=0.5) + WhiteKernel(noise_level=1, noise_level_bounds=(1e-10, 1e+1))', 'alpha' : '1e-6'}
    },
    'NN' : {
        'name' : 'Neural Network',
        'parameters' : {'hidden_layer_sizes' : '(32,16,8)', 'alpha' : '0.1', 'activation' : 'relu', 'solver' : 'lbfgs', 'learning_rate_init' : '0.001', 'random_state' : '1'}
    },
    'RF' : {
        'name' : 'Random Forest Regressor',
        'parameters' : {'n_estimators' : '100', 'max_depth' : '1', 'random_state' : '1'}
    },
}
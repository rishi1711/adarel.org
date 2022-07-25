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
        'label' : ["Select the trend:", "Select the seasonal:", "Enter the seasonality_periods:"],
        'parameters' : {'trend' : 'dropdown', 'seasonal' : 'dropdown', 'seasonality_periods' : 'input'},
        'default' : ['add', 'add', '0'],
        'dropdown' : [['add', 'mul', 'additive', 'multiplicative', None], ['add', 'mul', 'additive', 'multiplicative', None]],
        'required' : ['seasonality_periods']
    },
    'Arima' : {
        'name' : 'Arima',
        'label' : ["Enter the Order tupple values:", "Enter AutoRegressive:", "Enter Difference:", "Enter Moving Average Components:"],
        'parameters' : {'order' : 'tupple', 'Autoregressive' : 'input', 'Difference' : 'input', 'Moving Average Component' : 'input'},
        'default' : ['None','0', '0', '0'],
        'dropdown' : None,
        'required' : None
    },
    'Sarimax' : {
        'name' : 'Sarimax',
        'label' : ["Enter the Order tupple values:", "Enter AutoRegressive:", "Enter Difference:", "Enter Moving Average Components:", "Enter Seasonal Order tupple values:","Enter AR parameters:", "Enter Differences:", "Enter MA parameters:","Enter periodicity:"],
        'parameters' : {'order' : 'tupple', 'Autoregressive' : 'input', 'Difference' : 'input', 'Moving Average Component' : 'input', 'Seasonal Order': 'tupple', 'AR parameters' : 'input', 'Diffrences' : 'input', 'MA parameters' : 'input', 'Periodicity' : 'input'},
        'default' : ['None','0', '0', '0', None, '0','0', '1', '24'],
        'dropdown' : None,
        'required' : None
    },
    'SVR' : {
        'name' : 'Support Vector Machine Regressor',
        'label' : ["Select the kernel type:", "Enter Regularization parameter(C):", "Enter gamma values:", "Enter Epsilon values:"],
        'parameters' : {'kernel' : 'dropdown', 'C' : 'input', 'gamma' : 'input', 'epsilon' : 'input'},
        'default' : ['linear', '0.1', '0.1', '0.0001'],
        'dropdown' : [['linear', 'poly', 'rbf', 'sigmoid', 'precomputed']],
        'required' : None
    },
    'RF' : {
        'name' : 'Random Forest Regressor',
        'label' : ["Enter the n_estimatore:", "Enter maximum depth:", "Enter random state:"],
        'parameters' : {'n_estimators' : 'input', 'max_depth' : 'input', 'random_state' : 'input'},
        'default' : ['100', '1', '1'],
        'dropdown' : None,
        'required' : None
    },
    'NN' : {
        'name' : 'Neural Network',
        'label' : ["Select Activation function:", "Select solver:", "Enter the hidden layer sizes(tupple):", "Enter L2 Regularization term(aplha):",  "Enter learning rate schedule:", "Enter random number:"],
        'parameters' : {'activation' : 'dropdown', 'solver' : 'dropdown', 'hidden_layer_sizes' : 'input', 'alpha' : 'input', 'learning_rate_init' : 'input', 'random_state' : 'input'},
        'default' : ['relu', 'lbfgs', '32,16,8', '0.1', '0.001', '1'],
        'dropdown' : [['identity', 'logistic', 'tanh', 'relu'], ['lbfgs', 'sgd', 'adam']],
        'required' : None
    },
    'GPR' : {
        'name' : 'Gaussian Process Regression',
        'parameters' : {'kernel' : '0.35 * RBF(length_scale=0.5) + WhiteKernel(noise_level=1, noise_level_bounds=(1e-10, 1e+1))', 'alpha' : '1e-6'}
    },

}
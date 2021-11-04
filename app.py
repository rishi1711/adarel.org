# -*- coding: utf-8 -*-
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

from navbar import navbar
from flask_caching import Cache


app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
#pip install Flask-Caching==1.7.2
cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache-directory'
})
#https://dash.plotly.com/performance

import sqlite3
from flask_login import UserMixin
from sqlalchemy import ForeignKey, Table, create_engine, inspect
from sqlalchemy.sql import select
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, create_database
import pandas as pd


engine = create_engine('sqlite:///database/data.sqlite')
insp = inspect(engine)
db = SQLAlchemy()
#class for the table Users
class Users(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), nullable = False)
    lastname = db.Column(db.String(80), nullable = False)
    username = db.Column(db.String(50), unique=True, nullable = False)
    password = db.Column(db.String(80))
    companyName = db.Column(db.String(80))
Users_tbl = Table('user', Users.metadata)

#class for the uploaded files
class Uploadedfiles(db.Model):
    __tablename__ = 'files'
    file_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    filepath = db.Column(db.String(80))
    filetype = db.Column(db.String(80))
    datasetname = db.Column(db.String(80))
    filename = db.Column(db.String(80), nullable = False)
Uploaded_files_tbl = Table('files', Uploadedfiles.metadata)

#class for the table Strategy
class Strategy(db.Model):
    __tablename__ = 'strategy'
    strategy_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    strategy_name = db.Column(db.String(50), unique=True, nullable = False)
    strategy_data = db.Column(db.String, nullable = False)
strategy_tbl = Table('strategy', Strategy.metadata)

#class for the table Previous predictions
class PreviousPredictions(db.Model):
    __tablename__ = 'PreviousPredictions'
    id = db.Column(db.Integer, primary_key=True)
    strategy_id = db.Column(db.Integer, db.ForeignKey('strategy.strategy_id'), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    file_id = db.Column(db.Integer, db.ForeignKey('files.file_id'), nullable = False)
    mae = db.Column(db.String(50), nullable = False)
    rmse = db.Column(db.String(), nullable = False)
    graph_values = db.Column(db.String(), nullable = False)
previousPredictions_tbl = Table('PreviousPredictions', PreviousPredictions.metadata)


#create the table only once.
#fuction to create table using Users class
def create_users_table():
    Users.metadata.create_all(engine)

def create_upload_table():
    Uploadedfiles.metadata.create_all(engine)

def create_strategy_table():
    Strategy.metadata.create_all(engine)

def create_previousPrediction_table():
    PreviousPredictions.metadata.create_all(engine)
# if not insp.has_table("Uploadedfiles", schema="db"):
#     create_upload_table()
# else:
#     pass
#create the table
if not database_exists('sqlite:////database/data.sqlite'):
    create_users_table()
    create_upload_table()
    create_strategy_table()
    create_previousPrediction_table()


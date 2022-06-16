import sqlite3
from flask_login import UserMixin
from sqlalchemy import Table, create_engine
from sqlalchemy.sql import select
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
conn = sqlite3.connect('./database/data.sqlite')

engine = create_engine('sqlite:///database/data.sqlite')
db = SQLAlchemy()
#class for the table Users
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable = False)
    password = db.Column(db.String(80))
    companyName = db.Column(db.String(80))
Users_tbl = Table('users', Users.metadata)

#create the table only once.
#fuction to create table using Users class
def create_users_table():
    Users.metadata.create_all(engine)
#create the table
if not database_exists('sqlite:////database/data.sqlite'):
    create_users_table()
else:
    c = conn.cursor()
    df = pd.read_sql('select * from users', conn)
    print(df)



import sqlite3
from flask_login import UserMixin
from sqlalchemy import ForeignKey, Table, create_engine, inspect
from sqlalchemy.sql import select
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
conn = sqlite3.connect('./database/data.sqlite')

engine = create_engine('sqlite:///database/data.sqlite')
insp = inspect(engine)
db = SQLAlchemy()
#class for the table Users
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable = False)
    password = db.Column(db.String(80))
    companyName = db.Column(db.String(80))
Users_tbl = Table('user', Users.metadata)

#class for the uploaded files
class Uploadedfiles(db.Model):
    __tablename__ = 'files'
    file_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    filepath = db.Column(db.String(50), unique=True, nullable = False)
Uploaded_files_tbl = Table('files', Uploadedfiles.metadata)

#create the table only once.
#fuction to create table using Users class
def create_users_table():
    Users.metadata.create_all(engine)

def create_upload_table():
    Uploadedfiles.metadata.create_all(engine)

# if not insp.has_table("Uploadedfiles", schema="db"):
#     create_upload_table()
# else:
#     pass
#create the table
if not database_exists('sqlite:////database/data.sqlite'):
    create_users_table()
    create_upload_table()
else:
    c = conn.cursor()
    df = pd.read_sql('select * from users', conn)
    print(df)


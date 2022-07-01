import pandas as pd
import matplotlib.pyplot as plt
import datetime
import sqlite3
import sqlalchemy
import os
import psycopg2
from datetime import datetime
from datetime import date
pd.options.mode.chained_assignment = None
from datetime import timedelta
import numpy as np
dirname = os.path.dirname(__file__)
Database = os.path.join(dirname, 'data/PersonalData.db')

connection = sqlite3.connect(r'PersonalData.db')
cursor = connection.cursor()
new_engine = sqlalchemy.create_engine('postgresql://postgres:PhysicsKing123!@database-1.cvz7mc32ef1r.us-east-2.rds.amazonaws.com:5432/postgres')
engine = sqlalchemy.create_engine(r'sqlite:///{}'.format(Database)).connect()
df = pd.read_sql_table('PersonalData',engine,index_col=1)
print(df.head())
df.to_sql('PersonalData', new_engine, if_exists='replace', index=False)
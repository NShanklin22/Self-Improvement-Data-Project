import sqlite3
import pandas as pd
import sqlalchemy
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.dates as mdates

#Functions

#Code Start
connection = sqlite3.connect('Data/PersonalData.db')
cursor = connection.cursor()
engine = sqlalchemy.create_engine('sqlite:///Data/PersonalData.db').connect()

#Create dataframe from SQL database
df = pd.read_sql_table('PersonalData',engine,index_col=1)

#Read csv daTa that I cleaned up in Jupyter Notebooks
df['electronics'] = pd.to_numeric(df['electronics'],errors='coerce')
df['programming'] = pd.to_numeric(df['programming'],errors='coerce')
df['gaming'] = pd.to_numeric(df['gaming'],errors='coerce')
df['design'] = pd.to_numeric(df['design'],errors='coerce')

#Add new columns based of calculation on existing column data
df['cumgaming'] = df['gaming'].cumsum(axis=0)
df['cumprogramming'] = df['programming'].cumsum(axis=0)
df['cumelectronics'] = df['electronics'].cumsum(axis=0)
df['cumdesign'] = df['design'].cumsum(axis=0)

#Plot the cumulative data
plt.plot(df.date,df.cumgaming/60, label = "Gaming")
plt.plot(df.date,df.cumprogramming/60, label = "Programming")
plt.plot(df.date,df.cumelectronics/60, label = "Electronics")
plt.plot(df.date,df.cumdesign/60, label = "Design")
plt.legend()
plt.show()

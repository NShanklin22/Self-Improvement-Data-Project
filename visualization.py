import sqlite3
import pandas as pd
import sqlalchemy
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.dates as mdates


# Functions
def createBarGraph():
    return


def createPieChart(df):
    # Determine the total for each category
    CatTotal = df.sum()
    RangeTotal = CatTotal.sum()
    CatPercent = (CatTotal / RangeTotal * 100)

    # Create the pie chart and set the settings
    labels = 'Programming', 'Gaming', 'Electronics', 'Design'
    fig1, ax1 = plt.subplots()
    ax1.pie(CatPercent, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title(label="Percent Time per Category", fontsize=18, loc="left")
    plt.show()


def createLineChart(df):
    # Create a new dataframe with cumulative sums of each category
    sums = df[["gaming", "programming", "design", "electronics"]].cumsum()
    # Create the figure and axes
    fig = plt.figure()
    ax = plt.axes()
    weight = 60
    # Set the dates using mdates for easier formating
    df['date'] = pd.to_datetime(df['date'],format='%m/%d/%y')
    dates = mdates.date2num(df['date'])

    # Create a line plot of the x and y variables
    ax.plot(df.date, sums.gaming / weight, label="Gaming")
    ax.plot(df.date, sums.programming / weight, label="Programming")
    ax.plot(df.date, sums.electronics / weight, label="Electronics")
    ax.plot(df.date, sums.design / weight, label="Design")
    # Additional fromating of the table
    ax.set_title('Category Values Vs Time')
    ax.set_ylabel('Category Data (m)')
    ax.set_xlabel('Date')
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=7))
    ax.xaxis.set_minor_locator(mdates.DayLocator())
    ax.grid(True)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    fig.legend(loc='upper left', bbox_to_anchor=(.15, .85))
    fig.autofmt_xdate()
    fig.set_size_inches(18.5, 10.5)
    plt.show()

# # Code Start
# connection = sqlite3.connect('Data/PersonalData.db')
# cursor = connection.cursor()
# engine = sqlalchemy.create_engine('sqlite:///Data/PersonalData.db').connect()
#
# # Create dataframe from SQL database
# df = pd.read_sql_table('PersonalData', engine, index_col=1)
#
# # Read csv daTa that I cleaned up in Jupyter Notebooks
# df['electronics'] = pd.to_numeric(df['electronics'], errors='coerce')
# df['programming'] = pd.to_numeric(df['programming'], errors='coerce')
# df['gaming'] = pd.to_numeric(df['gaming'], errors='coerce')
# df['design'] = pd.to_numeric(df['design'], errors='coerce')
#
# # Add new columns based of calculation on existing column data
# df['cumgaming'] = df['gaming'].cumsum(axis=0)
# df['cumprogramming'] = df['programming'].cumsum(axis=0)
# df['cumelectronics'] = df['electronics'].cumsum(axis=0)
# df['cumdesign'] = df['design'].cumsum(axis=0)
#
# # Plot the cumulative data
# plt.plot(df.date, df.cumgaming / 60, label="Gaming")
# plt.plot(df.date, df.cumprogramming / 60, label="Programming")
# plt.plot(df.date, df.cumelectronics / 60, label="Electronics")
# plt.plot(df.date, df.cumdesign / 60, label="Design")
# plt.legend()
# plt.show()

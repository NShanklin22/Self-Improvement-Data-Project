import sqlite3
import pandas as pd
import sqlalchemy
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.dates as mdates


# Functions
def createBarChart(DataRange):
    # Create a bar chart
    labels = ['Programming', 'Gaming', 'Electronics', 'Design']
    DateTimeRange = pd.to_datetime(DataRange['date'])
    data = DataRange.sum()
    data = data / 60
    fig1, ax1 = plt.subplots()
    ax1.bar(labels, data, color=['green', 'red', 'blue', 'purple'])
    ax1.set_ylabel('Category Totals (m)')
    ax1.set_xlabel('Category')
    plt.title(label="Time Spent Per Category from: {} to: {}".format(DateTimeRange.iloc[0].date(), DateTimeRange.iloc[-1].date()),
              fontsize=14, loc="center")
    plt.grid()
    plt.show()
    return

def createPieChart(DataRange):
    # Determine the total for each category
    DateTimeRange = pd.to_datetime(DataRange['date'])
    DataRange = DataRange.drop('date',axis=1)
    CatTotal = DataRange.sum()
    RangeTotal = CatTotal.sum()
    CatPercent = (CatTotal / RangeTotal * 100)

    # Create the pie chart and set the settings
    labels = 'Programming', 'Gaming', 'Electronics', 'Design'
    fig1, ax1 = plt.subplots()
    ax1.pie(CatPercent, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title(label="Percent Time per Category from {} to {}".format(DateTimeRange.iloc[0].date(),DateTimeRange.iloc[-1].date()), fontsize=18, loc="left")
    fig1.set_size_inches(10.5, 10.5)
    plt.show()

def createLineChart(DataRange):
    # Create a new dataframe with cumulative sums of each category
    sums = DataRange[["gaming", "programming", "design", "electronics"]].cumsum()
    # Create the figure and axes
    fig = plt.figure()
    ax = plt.axes()
    weight = 60
    # Set the dates using mdates for easier formating
    DataRange['date'] = pd.to_datetime(DataRange['date'],format='%m/%d/%y')
    dates = mdates.date2num(DataRange['date'])

    # Create a line plot of the x and y variables
    ax.plot(DataRange.date, sums.gaming / weight, label="Gaming")
    ax.plot(DataRange.date, sums.programming / weight, label="Programming")
    ax.plot(DataRange.date, sums.electronics / weight, label="Electronics")
    ax.plot(DataRange.date, sums.design / weight, label="Design")
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

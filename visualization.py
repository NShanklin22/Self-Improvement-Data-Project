import datetime
import sqlite3
import time
import os
import pandas as pd
import sqlalchemy
import numpy as np
from datetime import datetime
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
from otherFunctions import *

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

    plt.title(label="Time Spent Per Category from: {} to: {}".format(DateTimeRange.iloc[0].date(), DateTimeRange.iloc[-1].date()), fontsize=14, loc="center")
    plt.grid()
    plt.show()
    return

def createDateRangeBarChart(DataRange):
    return

def createPieChart(DataRange):

    reqPrint = input("would you like to print this chart? (y/n): ")

    # Determine the total for each category
    DateTimeRange = pd.to_datetime(DataRange['date'])
    DataRange = DataRange.drop('date',axis=1)
    CatTotal = DataRange.sum()
    RangeTotal = CatTotal.sum()
    CatPercent = (CatTotal / RangeTotal * 100)

    # Create the pie chart and set the settings
    labels = 'Programming', 'Gaming', 'Electronics', 'Design'
    fig1, ax1 = plt.subplots()
    fig1.set_size_inches(10.5, 10.5)

    ax1.pie(CatPercent, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.title(label="Percent Time per Category from {} to {}".format(DateTimeRange.iloc[0].date(),DateTimeRange.iloc[-1].date()), fontsize=18, loc="left")
    if reqPrint == "y":
        my_path = os.path.abspath(__file__)
        plt.savefig(os.path.join(my_path, '..\Charts\PieChart_{}.png'.format(datetime.today().date())))
    plt.show()

def createLineChart(DataRange):
    # Create a new dataframe with cumulative sums of each category
    sums = DataRange[["gaming", "programming", "design", "electronics"]].cumsum()

    # Set the interval for the chart
    if len(DataRange) < 7:
        X_Interval = 1
    else:
        X_Interval = 7

    # Create the figure and axes
    fig = plt.figure()
    ax = plt.axes()
    weight = 60

    # Set the dates using mdates for easier formating
    DataRange['date'] = pd.to_datetime(DataRange['date'])
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
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=X_Interval))
    ax.xaxis.set_minor_locator(mdates.DayLocator())
    ax.grid(True)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))

    fig.legend(loc='upper left', bbox_to_anchor=(.15, .85))
    fig.autofmt_xdate()
    fig.set_size_inches(18.5, 10.5)

    plt.show()

def animateLineGraph(df):
    x_values = []
    y_values = []
    y_values_02 = []
    y_values_03 = []
    sums = df[["gaming", "programming", "design", "electronics"]].cumsum()
    df['date'] = pd.to_datetime(df['date'])
    sums['productive'] = sums['programming'] + sums['electronics'] + sums['design']
    sums['difference'] = sums['gaming'] - sums['productive']

    # This section is a stagnate graph showing the data for the entire time range
    # Create the figure and axes
    fig = plt.figure()
    ax = plt.axes()
    dates = mdates.date2num(df['date'])
    fig.legend(loc='upper left', bbox_to_anchor=(.15, .85))

    fig.autofmt_xdate()
    fig.set_size_inches(18, 10)

    for i in range(len(df)):
        x_values.append(df.iloc[i]['date'].date())
        y_values.append(sums.iloc[i]['productive'])
        y_values_02.append(sums.iloc[i]['gaming'])
        y_values_03.append(sums.iloc[i]['difference'])
        plt.xlim(df.iloc[0]['date'], datetime.today())
        plt.ylim(0, sums['gaming'].max())
        ax.set_title('Category Values Vs Time Animated')
        ax.set_ylabel('Category Data (m)')
        ax.set_xlabel('Date')
        ax.plot(x_values, y_values, label="Productive", color="green")
        ax.plot(x_values, y_values_02, label="Gaming", color="red")
        ax.plot(x_values, y_values_03, label="Difference", color="orange")
        ax.set_title('Category Values Vs Time')
        ax.set_ylabel('Category Data (m)')
        ax.set_xlabel('Date')
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=7))
        ax.xaxis.set_minor_locator(mdates.DayLocator())
        ax.grid(True)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        if (i == 0):
            fig.legend(loc='upper left', bbox_to_anchor=(.15, .85))
        plt.pause(.01)

    plt.show()
    input("Press any key to continue...")
    return

def animatePieChart(df):
    df['date'] = pd.to_datetime(df['date'])
    fig1, ax1 = plt.subplots()

    # Determine the total for each category
    for i in range(len(df)):
        plt.cla()
        CatTotal = df[0:i + 1].sum()
        RangeTotal = CatTotal.sum()
        CatPercent = (CatTotal / RangeTotal * 100)

        # Create the pie chart and set the settings
        labels = 'Programming', 'Gaming', 'Electronics', 'Design'
        ax1.pie(CatPercent, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title(label="Percent Time per Category from {} to {}".format(df.iloc[0]['date'].date().strftime("%m/%d"),
                                                                         df.iloc[i]['date'].date().strftime("%m/%d")),
                  fontsize=18, loc="left")
        fig1.set_size_inches(18.5, 10.5)
        plt.pause(.05)
    plt.show()
    input("Press any key to continue...")
    return

def createGamingChart(df):
    # Create the figure and axes
    fig = plt.figure()
    ax = plt.axes()
    plt.title('Gaming Trend Data', fontsize=30)
    fig.legend(loc='upper left', bbox_to_anchor=(.15, .85))
    weight = 60
    dates = mdates.date2num(df['date'])

    rollAvg7 = df.rolling(7).mean()
    rollAvg15 = df.rolling(15).mean()
    rollAvg30 = df.rolling(30).mean()

    line1 = ax.plot(dates, rollAvg7['gaming'], color='green', label="7 day average", linewidth=4)
    line2 = ax.plot(dates, rollAvg15['gaming'], color='blue', label='15 day average', linewidth=5)
    line3 = ax.plot(dates, rollAvg30['gaming'], color='yellow', label='30 day average', linewidth=6)
    df = df['gaming']


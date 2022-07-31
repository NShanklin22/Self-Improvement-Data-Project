# This program takes in a user input of a date range and return data from that range

# Imports
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import sqlite3
import sqlalchemy
from datetime import datetime
from datetime import date
pd.options.mode.chained_assignment = None
from datetime import timedelta
import numpy as np
from otherFunctions import *

# Functions
# Return a dataframe of a certain week based off of a provided number
def getDataByCurrentWeek(df):
    WeekMask = getWeekMask()
    today = datetime.today()
    df['date'] = pd.to_datetime(df['date']).dt.date
    RangeEnd = datetime.today().date()
    RangeStart_temp = WeekMask.where((WeekMask < today) & (WeekMask > today - timedelta(days=7))).dropna()
    RangeStart_temp = RangeStart_temp.iloc[0]
    RangeStart = RangeStart_temp.iloc[0].date()
    DataRange = df.where((df['date'] >= RangeStart) & (df['date'] <= RangeEnd)).dropna()
    return DataRange

# Return a dataframe by providing a certain date range
def getDataByDateRange(df):
    # Simple code block for requesting a date range from the user and pulling data
    ReqRangeStart = input('Please enter a start day (MM/DD/YY) : ')
    ReqRangeEnd = input('Please enter an end day (MM/DD/YY) : ')
    print('Pulling data from {} to {}'.format(ReqRangeStart, ReqRangeEnd))
    DataRange = df.where((df['date'] >= ReqRangeStart) & (df['date'] <= ReqRangeEnd)).dropna()
    DataRange['date'] = pd.to_datetime(DataRange['date'])
    return DataRange

# Return a dataframe by providing a certain date range
def getDataByMonth(df,ReqMonth):
    months = {1:"January",2:"February",3:"March",4:"April",5:"May",6:"June",7:"July",8:"August",9:"September",10:"October",11:"November",12:"December"}
    df['date'] = pd.to_datetime(df['date'])
    # Simple code block for pulling data by a given month
    while True:
        # Ask the user for a month to pull data from and cast as an int
        # Check if the month provided is a valid month
        if ReqMonth in months:
            MonthData = df.where(df['date'].dt.year == datetime.now().year).dropna()
            MonthData = MonthData.where(df['date'].dt.month==ReqMonth).dropna()
            if MonthData.empty:
                print("There is no data for that month")
                MonthData = df.where(df['date'].dt.month == datetime.now().month).dropna()
                return MonthData
            else:
                print("Pulling data for {}".format(months[ReqMonth]))
                return MonthData
        # If month is not valid ask the user for a new input
        else:
            return months[datetime.now().month]

def getDataByYear(df, ReqYear):
    df['date'] = pd.to_datetime(df['date'])
    years = pd.DatetimeIndex(df['date']).year.unique()
    # Simple code block for pulling data by a given month
    print(ReqYear)
    print(df)
    if ReqYear == 2021:
        YearData = df.where(df['date'].dt.year == 2021).dropna()
        return YearData
    elif ReqYear == 2022:
        YearData = df.where(df['date'].dt.year == 2022).dropna()
        return YearData
    else:
        YearData = df.iloc[-365:]
        return  YearData
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
# Determine the current week based off of todays date
def getCurrentWeek():
    WeekMask = getWeekMask()
    today = datetime.today()
    CurrentWeek = WeekMask.where((WeekMask < today) & (WeekMask > today - timedelta(days=7))).dropna()
    CurrentWeek['WeekNum'] = CurrentWeek.index
    print("The current week is: {} \nThe week started on: {}".format(CurrentWeek.iloc[0]['WeekNum'],CurrentWeek.iloc[0]['WeekStart'].date()))

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
def getDataByMonth(df):
    months = {1:"January",2:"February",3:"March",4:"April",5:"May",6:"June",7:"July",8:"August",9:"September",10:"October",11:"November",12:"December"}
    df['date'] = pd.to_datetime(df['date'])
    # Simple code block for pulling data by a given month
    while True:
        # Ask the user for a month to pull data from and cast as an int
        ReqMonth = int(input('Please enter a month # (1-12): '))
        # Check if the month provided is a valid month
        if ReqMonth in months:
            MonthData = df.where(df['date'].dt.month==ReqMonth).dropna()
            if MonthData.empty:
                print("There is no data for that month")
            else:
                print("Pulling data for {}".format(months[ReqMonth]))
                return MonthData
        # If month is not valid ask the user for a new input
        else:
            print("{} is not a valid month #".format(ReqMonth))

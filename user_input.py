# This program takes in a user input and stores it to an SQL database

import pdb
import datetime
import sqlite3
import pandas as pd
import sqlalchemy
import datetime
from datetime import datetime

# Create connection to SQL and an engine for SQLalchemy
connection = sqlite3.connect(r'C:\Users\Shanky\Desktop\Python\Main_Projects\Self_Improvement_Project\data\PersonalData.db')
cursor = connection.cursor()
engine = sqlalchemy.create_engine(r'sqlite:///C:\Users\Shanky\Desktop\Python\Main_Projects\Self_Improvement_Project\data\PersonalData.db').connect()

# Create a temporary dataframe to manipulate data from SQL database
df = pd.read_sql_table('PersonalData', engine, index_col=1)


###Functions###
# Asks user for the category of the data
def getCategory():
    while True:
        value = str(input("Please Enter the data category (programming,gaming,electronics,design,finance): "))
        if value == "electronics" or value == "programming" or value == "gaming" or value == "design" or value == 'finance':
            break
        else:
            print("That is not a valid category, please try again")
    return value


# Asks user for the date of the data
def getDate():
    while True:
        userDate = str(input("Please Enter the data date (MM/DD/YY) or t for today: "))
        isValidDate = True
        if(userDate == 't'):
            userDate = datetime.strftime(datetime.today().date(),'%m/%d/%y')
            return userDate
        try:
            month, day, year = userDate.split('/')
            datetime(int(year), int(month), int(day))
        except ValueError:
            isValidDate = False

        if isValidDate:
            return userDate
        else:
            print("That is not a valid date")


# Asks user for the duration value of the category and converts to seconds
def getDuration():
    # Converts time in HH:MM:SS format to a integer in seconds
    while True:
        value = str(input("Please Enter the duration (HH:MM:SS or '0'): "))
        if value == '0':
            return 0
        try:
            h, m, s = value.split(':')
        except ValueError:
            print("That is not a valid date")
        else:
            return int(h) * 3600 + int(m) * 60 + int(s)


# Used to convert HH:MM:SS to seconds
def get_sec(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)


def addEntryToDataframe(df, category, date, duration):
    # Use the match function to update the dataframe depending on catagory passed into this function
    if (category == 'programming'):
        new_data = {'date': str(date), 'programming': duration, 'gaming': 0, 'electronics': 0, 'design': 0, 'finance': 0}
    if (category == 'gaming'):
        new_data = {'date': str(date), 'programming': 0, 'gaming': duration, 'electronics': 0, 'design': 0, 'finance': 0}
    if (category == 'electronics'):
        new_data = {'date': str(date), 'programming': 0, 'gaming': 0, 'electronics': duration, 'design': 0, 'finance': 0}
    if (category == 'design'):
        new_data = {'date': str(date), 'programming': 0, 'gaming': 0, 'electronics': 0, 'design': duration, 'finance': 0}
    if (category == 'finance'):
        new_data = {'date': str(date), 'programming': 0, 'gaming': 0, 'electronics': 0, 'design': 0, 'finance': duration}

    # Create a new single row series based off of the new data
    new_row = pd.DataFrame(new_data, index=[0])

    # Append the main dataframe with the new row
    df = df.append(new_row, ignore_index=True)
    # Sort values by date
    df['date'] = pd.to_datetime(df['date'])
    df.sort_values('date', inplace=True)
    # Merge the data for duplicate dates
    df = df.groupby(['date'], as_index=False).sum()

    return df

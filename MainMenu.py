# This program will serve as the main navigation program, all others will be called from here
import visualization
from user_input import *
from pull_entry import *
from visualization import *
import pdb
import datetime
import sqlite3
import pandas as pd
import sqlalchemy
import datetime

# Create connection to SQL and an engine for SQLalchemy
connection = sqlite3.connect("D:\\Libraries\\Desktop\\Python\\Projects\\Self_Improvement_Data\\Data\\PersonalData.db")
cursor = connection.cursor()
engine = sqlalchemy.create_engine(
    'sqlite:///D:\Libraries\Desktop\Python\Projects\Self_Improvement_Data\Data/PersonalData.db').connect()

# Create a temporary dataframe to manipulate data from SQL database
df = pd.read_sql_table('PersonalData', engine, index_col=1)

# Prints the main welcome message
print('Welcome to Onward\u2122 - a self improvement data tracking program\n')

# Function which handles the main menu screen prompt
def mainMenu():
    global df
    print("Main Menu")
    while True:
        print('Menu Options:')
        # Create the option menu
        print('1 - Enter new data to the database')
        print('2 - Read old data from the database')
        print('3 - Exit the program')
        # Asks the user for their input
        MenuSelect = input('\nPlease select a menu option: ')
        # Menu option 1 will enter new data, uses functions from user input program
        if MenuSelect == '1':
            dataEntryMenu()
        elif MenuSelect == '2':
            pullEntryMenu()
        elif MenuSelect == '3':
            exit()

# Function for call data entry functions
def dataEntryMenu():
    global df
    category = getCategory()
    date = getDate()
    duration = getDuration()
    df = addToDataframe(df, category, date, duration)
    df.to_sql('PersonalData', engine, if_exists='replace', index=False)
    print("Entry has been successfully saved to the database")
    return df

# Function for pulling data menu
def pullEntryMenu():
    global df
    # Gets data by a date range provided by the user, returns dataframe
    print('Would you like to view all data or data range?')
    print('1 - View data by range')
    print('2 - View all data')
    print('3 - Get data by month ')
    print('4 - Return to Main Menu')
    MenuSelect = input('\nSelect a menu option: ')
    print("\n")
    # Pull different data based off of user input
    if MenuSelect == '1':
        DataRange = getDataByDateRange()
    elif MenuSelect == '2':
        DataRange = df
    elif MenuSelect == '3':
        DataRange = getDataByMonth()
    elif MenuSelect == '4':
        mainMenu()
    visualMenu(DataRange)

# Function will be used by the pullEntry function and work with visualMenu()
def dataManipMenu(df):
    return

# Function for selecting the visualization method
def visualMenu(DataRange):
    while True:
        # Ask user how they would like to view this data
        print(("How would you like to view this data? "))
        print('1 - Display data in a table')
        print('2 - Display data as a pie chart')
        print('3 - Display data as a bar chart')
        print('4 - Display data as a line chart')
        print('5 - Select different data set')
        MenuSelect = input('\nSelect a menu option: ')
        if MenuSelect == '1':
            print(DataRange)
        elif MenuSelect == '2':
            visualization.createPieChart(DataRange)
        elif MenuSelect == '3':
            continue
        elif MenuSelect == '4':
            visualization.createLineChart(DataRange)
        elif MenuSelect == '5':
            pullEntryMenu()
        while True:
            UserInput = input("Would you like to view this data another way? (y/n): ")
            if UserInput == 'y':
                visualMenu(DataRange)
            if UserInput == 'n':
                mainMenu()
            else:
                print("That is not a valid response")

# Call the main menu option function
mainMenu()

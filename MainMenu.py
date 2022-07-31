# This program will serve as the main navigation program, all others will be called from here
import time

import visualization
from user_input import *
from pull_entry import *
from visualization import *
from otherFunctions import *
from analyzeData import *
import pdb
import datetime
import sqlite3
import pandas as pd
import sqlalchemy
import datetime

# Create connection to SQL and an engine for SQLalchemy
connection = sqlite3.connect(r'C:\Users\Shanky\Desktop\Python\Main_Projects\Self_Improvement_Project\data\PersonalData.db')
cursor = connection.cursor()
engine = sqlalchemy.create_engine(r'sqlite:///C:\Users\Shanky\Desktop\Python\Main_Projects\Self_Improvement_Project\data\PersonalData.db').connect()

# Create a temporary dataframe to manipulate data from SQL database
df = pd.read_sql_table('PersonalData', engine, index_col=1)

# Prints the main welcome message
print('Welcome to Onward\u2122 - a self improvement data tracking program\n')
printQuote()

# Function which handles the main menu screen prompt
def mainMenu():
    global df
    #playSound()
    print("Main Menu")
    while True:
        print('\nMenu Options:')
        # Create the option menu
        print('1 - Enter new data to the database')
        print('2 - Read old data from the database')
        print('3 - Analyze data')
        print('4 - Help Page')
        print('5 - Exit the program')
        # Asks the user for their input')
        MenuSelect = input('\nPlease select a menu option: ')
        # Menu option 1 will enter new data, uses functions from user input program
        if MenuSelect == '1':
            addNewDataEntry()
        elif MenuSelect == '2':
            pullEntryMenu()
        elif MenuSelect == '3':
            analysisMenu(df)
        elif MenuSelect == '4':
            helpMenu()
        elif MenuSelect == '5':
            print("Program exiting...")
            time.sleep(2)
            exit()
        else:
            print('That is not a valid option')

def addNewDataEntry():
    global df

    category = getCategory()
    date = getDate()
    duration = getDuration()
    df = addEntryToDataframe(df, category, date, duration)
    df.to_sql('PersonalData', engine, if_exists='replace', index=False)
    print("Entry has been successfully saved to the database")

def pullEntryMenu():
    df = pd.read_sql_table('PersonalData', engine, index_col=1)
    # Gets data by a date range provided by the user, returns dataframe
    print('\nHow would you like to select the data? ')
    print('1 - Select data by range')
    print('2 - Select all data')
    print('3 - Select data from today')
    print('4 - Select data from this week')
    print('5 - Select data by month ')
    print('6 - Select data by year')
    print('7 - Return to Main Menu')
    MenuSelect = input('\nSelect a menu option: ')
    print("\n")
    # Pull different data based off of user input
    if MenuSelect == '1':
        DataRange = getDataByDateRange(df)
    elif MenuSelect == '2':
        DataRange = df
    elif MenuSelect == '3':
        DataRange = df.iloc[-1].to_frame().T
        DataRange['date'] = pd.to_datetime(DataRange['date'])
    elif MenuSelect == '4':
        DataRange = getDataByCurrentWeek(df)
    elif MenuSelect == '5':
        DataRange = getDataByMonth(df)
    elif MenuSelect == '6':
        DataRange = getDataByYear(df)

    elif MenuSelect == '7':
        mainMenu()

    visualMenu(DataRange)

# Function will be used by the pullEntry function and work with visualMenu()
def analysisMenu(df):
    # Display menu options and request a input
    print(("data Analysis Options: "))
    print('1 - Run cumulative data animation (Line Chart)')
    print('2 - Run % weekly data animation (Pie Chart)')
    print('3 - Analyze Gaming Trends (DEV)')
    print('4 - Calculate Key Metrics')
    MenuSelect = input('\nSelect a menu option: ')
    if MenuSelect == '1':
        animateLineGraph(df)
    elif MenuSelect == '2':
        animatePieChart(df)
    elif MenuSelect == '3':
        createGamingChart(df)
    elif MenuSelect == '4':
        analyzeCategory(df)
        return

    return
# TODO: Be nate
# Function for selecting the visualization method
def visualMenu(DataRange):
    while True:
        # Ask user how they would like to view this data
        print(("How would you like to view this data? "))
        print('1 - Display data in a table')
        print('2 - Display data in a pie chart')
        print('3 - Display data in a bar chart')
        print('4 - Display data in a line chart')
        print('5 - Select different data set')
        MenuSelect = input('\nSelect a menu option: ')
        if MenuSelect == '1':
            print(DataRange)
        elif MenuSelect == '2':
            visualization.createPieChart(DataRange)
        elif MenuSelect == '3':
            createBarChart(DataRange)
        elif MenuSelect == '4':
            showLoading()
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

# Function to display helpfull information about the menu
def helpMenu():
    open("readme.txt")
    input("Press any key to return to the main menu...")


# Call the main menu option function
mainMenu()

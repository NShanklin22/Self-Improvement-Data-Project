import visualization
import pdb
import datetime
from datetime import datetime
import sqlite3
import random
import pandas as pd
import sqlalchemy

ActivityList = ['Read a book',
 'Exercise',
 'Program',
 'Online Course',
 'Play video games',
 'Work',
 'Clean/Organize',
 '3D Print something',
 'Craft',
 'Watch TV',
 'Cook',
 'Practice physics']

pd.set_option('display.max_columns', None)

df = pd.read_csv("data/ActivityLog",index_col = 0)
df.index = pd.to_datetime(df.index)

print(df.head())

global today
today = pd.to_datetime(datetime.today().date())

if today in df.index:
    print("okay!")
else:
    df.at[today] = [0,0,0,0,0,0,0,0,0,0,0,0]

def listActivities():
    print("Activity Selector: ")
    for i in range(len(ActivityList)):
        print("\t" + str(i+1) + ") " + ActivityList[i])

def mainMenu(df):
    print("Activity Selector")
    print("1 - Show current activities")
    print("2 - Select an activity for me")
    print("3 - Exit Program")
    while True:
        MenuSelect = input("Please select an option: ")
        if MenuSelect == str(1):
            return
        elif MenuSelect == str(2):
            selectActivity(df)
        elif MenuSelect == str(3):
            exit()
        else:
            print("That is not a valid option")

def selectActivity(df):
    print("Please complete the following activity: ")
    randint = random.randint(1,11)
    activity = df.columns[randint]
    print(activity)
    while True:
        response = input("Did you complete the activity (Y/N)? ")
        if response == "Y":
            df.at[today, activity] += 1
            return
        elif response == "N":
            print("You suck")
            return
        else:
            print("That is not a valid response")

mainMenu(df)
df.to_csv("data/ActivityLog")
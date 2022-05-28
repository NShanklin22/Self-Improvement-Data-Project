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

global today
today = pd.to_datetime(datetime.today().date())

if today in df.index:
    print("okay!")
else:
    df.at[today] = [0,0,0,0,0,0,0,0,0,0,0,0]

def getActivityMask(df):
    return


def listActivities():
    print("Activity Selector: ")
    for i in range(len(ActivityList)):
        print("\t" + str(i+1) + ") " + ActivityList[i])

def mainMenu(df):
    print("Activity Selector")
    print("1 - Show open activities")
    print("2 - Select an activity for me")
    print("3 - Show all entries for today")
    print("4 - Exit Program")
    while True:
        MenuSelect = input("Please select an option: ")
        if MenuSelect == str(1):
            viewActivities(df)
        elif MenuSelect == str(2):
            df = selectActivity(df)
        elif MenuSelect == str(3):
            print("Feature not yet implemented")
            return
        elif MenuSelect == str(4):
            return
        else:
            print("That is not a valid option")

def viewActivities(df):
    TodaysActivies = df.iloc[-1]
    ActivityList = TodaysActivies.index.tolist()
    CompleteList = TodaysActivies.values.tolist()
    for i in range(len(ActivityList)):
        if(CompleteList[i] > 0.0):
            print(f"{ ActivityList[i] : <40}{'Complete' : ^10}")
        else:
            print(f"{ ActivityList[i] : <40}{'Incomplete' : ^10}")



def selectActivity(df):
    print("Please complete the following activity: ")
    randint = random.randint(1,11)
    activity = df.columns[randint]
    print(activity)
    while True:
        response = input("Did you complete the activity (Y/N)? ")
        if response == "Y":
            df.at[today, activity] += 1
            return df
        elif response == "N":
            print("You suck")
            return df
        else:
            print("That is not a valid response")

mainMenu(df)
df.to_csv("data/ActivityLog")
#This application is intended to be used as a tool to track personal development data in the form of stopwatch and timer data for different subjects
import pandas as pd
from datetime import datetime

#function to check if the dataframe has todays date and if not add it with "0" for other columns
def checkDate(data,today):
    format_str = '%m/%d/%y'  # The format
    date_str = FocusData['Date'].iloc[-1]  # The date - 29 Dec 2017
    if(date_str == today):
        print("The Dataframe is Current")
        return True
    else:
        NewDateSeries = {'Date':today,'Programming':0,"Gaming":0}
        new_data = data.append(NewDateSeries, ignore_index=True)
        return new_data

#Declare the two column variables
GamingToday = "0"
ProgrammingToday = "0"
Today = datetime.today().strftime("%m/%d/%y")

#Checking the last date in dataframe, this can be improved
if(checkDate(FocusData,Today) == True):
    pass
else:
    FocusData = checkDate(FocusData,Today)

#Getting user input
GamingToday = input("Enter time spent gaming: ")
ProgrammingToday = input("Enter Time Spent Programming: ")


#if(FocusData['Date'].get(-1) != datetime.date()):
#    print("Hello World")

#Saving out the updated CSV
FocusData.to_csv("Personal Data.csv")
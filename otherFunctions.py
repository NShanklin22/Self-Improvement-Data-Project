import random
import json
import time
import pandas as pd
from datetime import datetime
from datetime import timedelta


def printQuote():
    # Open the file of quotes, read json, select a random number
    f = open('D:\\Libraries\\Desktop\\Python\\Projects\\Self_Improvement_Data\\quotes.json', encoding='UTF-8')
    quoteData = json.load(f)
    randomNum = random.randint(1, 25)

    # Print the quote and author based off of the random number
    print("Motivational Quote:")
    print('"' + quoteData['quotes'][randomNum]['quote'] + '"')
    print("By: " + quoteData['quotes'][randomNum]['author'] + "\n")


# Creates a dataframe of weeks in year by # and the start date
def getWeekMask():
    YearRange = pd.date_range(start='01/01/' + str(datetime.today().year), end='12/31/' + str(datetime.today().year),
                              freq='W-SAT')
    WeekMask = pd.DataFrame(YearRange, columns=['WeekStart'])
    return WeekMask

# Determine the current week based off of todays date
def getCurrentWeek():
    WeekMask = getWeekMask()
    today = datetime.today()
    CurrentWeek = WeekMask.where((WeekMask < today) & (WeekMask > today - timedelta(days=7))).dropna()
    CurrentWeek['WeekNum'] = CurrentWeek.index + 1
    return CurrentWeek

def printCurrentWeek():
    CurrentWeek = getCurrentWeek()
    WeekStart = datetime.strftime(CurrentWeek.iloc[0]['WeekStart'].date(),"%m-%d-%y")
    return ("The current week is: {} \nThe week started on: {}".format(CurrentWeek.iloc[0]['WeekNum'],WeekStart))

# Function to simulate loading for user
def showLoading():
    print("Loading.")
    time.sleep(.5)
    print("Loading..")
    time.sleep(.5)
    print("Loading...")
    time.sleep(.5)


def timeConversion(InputTime):
    ConvertedTime = timedelta(seconds=InputTime)
    return ConvertedTime

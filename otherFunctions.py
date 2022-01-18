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


def showLoading():
    print("Loading.")
    time.sleep(1)
    print("Loading..")
    time.sleep(1)
    print("Loading...")
    time.sleep(1)


def timeConversion(InputTime):
    ConvertedTime = timedelta(seconds=InputTime)
    return ConvertedTime

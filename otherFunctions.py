import random
import json
import time

def printQuote():
    # Open the file of quotes, read json, select a random number
    f = open('D:\\Libraries\\Desktop\\Python\\Projects\\Self_Improvement_Data\\quotes.json',encoding='UTF-8')
    quoteData = json.load(f)
    randomNum = random.randint(1,25)

    # Print the quote and author based off of the random number
    print("Motivational Quote:")
    print('"' + quoteData['quotes'][randomNum]['quote'] + '"')
    print("By: " + quoteData['quotes'][randomNum]['author'] + "\n")
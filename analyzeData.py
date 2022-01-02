# This program will be used to calculate specific information about the data

def analyzeData():
    print("What category would you like to analyze?")
    category = getCategory()
    print("What would you like to know about this category?")
    print("1) Max time spent in this category")
    print("2) Average time spent in this category")
    print("3) I needed to have a third option")


def getCategory():
    print("Category options are: \n 1) Programming \n 2) Gaming \n 3) Design \n 4) Electronics")
    category = input("Please select a category: ")
    return

def getCategoryMax(df):
    category = input("Please select a category (1-4) ")
    return

def getCategoryAverage(df):
    return

def calcLongestRun(df):
    print("Your previous longest run was")
    return

analyzeData()
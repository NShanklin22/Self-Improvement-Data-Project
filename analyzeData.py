# This program will be used to calculate specific information about the data

def getCategory():
    print("Category options are: \n 1 - Programming \n 2 - Gaming \n 3 - Design \n 4 - Electronics")
    category = input("Please select a category (1-4): ")
    return category

def getDataMax(df):
    MaxTime = df.max().drop('date')
    return MaxTime

def getDataMean(df):
    AverageTime = df.mean().drop('date')
    return AverageTime

def analyzeCategory(df):
    while True:
        getCategory()
        print("What would you like to know?")
        print("1 - Maximum time spent in category")
        print("2 - Average time spent in category")
        MenuSelect = input("Please select an option: ")

        if MenuSelect == 1:
            MaximumTime = getDataMax(df)
        elif MenuSelect == 2:
            AverageTime = getDataMean()
        else:
            print("Please select a different option")
        input("\nPress any key to continue")



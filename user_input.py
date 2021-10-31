import pdb
import datetime
import sqlite3
import pandas as pd
import sqlalchemy
import datetime

# Create connection to SQL and an engine for SQLalchemy
connection = sqlite3.connect('D:\Libraries\Desktop\Python\Projects\Self_Improvement_Data\Data\PersonalData.db')
cursor = connection.cursor()
engine = sqlalchemy.create_engine('sqlite:///D:\Libraries\Desktop\Python\Projects\Self_Improvement_Data\Data/PersonalData.db').connect()

# Create a temporary dataframe to manipulate data from SQL database
df = pd.read_sql_table('PersonalData',engine,index_col=1)

###Functions###y
#Asks user for the category of the data
def getCategory():
    while True:
        value = str(input("Please Enter the data category (programming,gaming,electronics,design): "))
        if value == "electronics" or value == "programming" or value == "gaming" or value == "design":
            break
        else:
            print("That is not a valid category, please try again")
    return value

#Asks user for the date of the data
def getDate():
    while True:
        value = str(input("Please Enter the data date (MM/DD/YY): "))
        isValidDate = True
        try:
            month, day, year = value.split('/')
            datetime.datetime(int(year), int(month), int(day))
        except ValueError:
            isValidDate = False

        if isValidDate:
            return value
        else:
            print("That is not a valid date")

#Asks user for the duration value of the category and converts to seconds
def getDuration():
    # Converts time in HH:MM:SS format to a integer in seconds
    while True:
        value = str(input("Please Enter the duration (HH:MM:SS or '0'): "))
        if value == '0':
            return 0
        try:
            h, m, s = value.split(':')
        except ValueError:
            print("That is not a valid date")
        else:
            return int(h) * 3600 + int(m) * 60 + int(s)

#Used to convert HH:MM:SS to seconds
def get_sec(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

# Function to add new entry to the local dataframe
def addToDataframe(df,category, date, duration):
    #Use the match function to update the dataframe depending on catagory passed into this function
    if(category == 'programming'):
        new_data = {'date':str(date),'programming':duration,'gaming':0,'electronics':0,'design':0}
    if(category == 'gaming'):
        new_data = {'date':str(date),'programming':0,'gaming':duration,'electronics':0,'design':0}
    if(category == 'electronics'):
        new_data = {'date':str(date),'programming':0,'gaming':0,'electronics':duration,'design':0}
    if(category == 'design'):
        new_data = {'date':str(date),'programming':0,'gaming':0,'electronics':0,'design':duration}

    #Create a new single row series based off of the new data
    new_row = pd.DataFrame(new_data, index=[0])

    #Append the main dataframe with the new row
    df = df.append(new_row, ignore_index=True)

    return df

# Section creates a dummy dataframe of expected dates and compares it to the saved dataframe
##########################
# Section to take in new data and add it to the respective database table
prompt = input("Would you like to enter new data y/n? ")
if(prompt == 'y'):
    #Get User input of category,date, and duration
    category = getCategory()
    date = getDate()
    duration = getDuration()
    #Add Data to respective table based off of user input
    df = addToDataframe(df,category,date,duration)
    #Sort the data by date
    df.sort_values('date',inplace=True)
    #Merge the data for duplicate dates
    df = df.groupby(['date'],as_index=False).sum()
    #Save the updated dataframe back to the SQL database, erase existing data
    df.to_sql('PersonalData', engine, if_exists='replace', index=False)
    # Let the user know the data was saved successfully
    print("Entry has been successfully saved to the database")

else:
    # Added line in case user says "N" to first prompt
    print("Operation aborted, have a nice day!")

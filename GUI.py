# Import tkinter
import tkinter as tk
import time
# ttk is basically the css for tkinter
from tkinter import ttk

# Import matplotlib libraries
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.dates as mpl_dates
#from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import matplotlib.dates as dates
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import psycopg2
import matplotlib.ticker as mticker
import pandastable
import datetime
from pandastable import Table, TableModel,config
from tkcalendar import Calendar

matplotlib.use("TkAgg")
style.use("ggplot")
import json
import os

# Import local functions
from GUI_Functions import *

XLARGE_FONT  = ("Verdana",30, 'bold')
LARGE_FONT = ("Verdana",20, 'bold')
RADIO_FONT = ("Verdana",20)
NORM_FONT = ("Verdana", 12,'bold')
SMALL_FONT = ("Verdana", 8)

dirname = os.path.dirname(__file__)
Database = os.path.join(dirname, 'data/PersonalData.db')

# Setting pandastable configuration options
options = config.load_options()
options = {'fontsize':14,'rowheight':30,'cellwidth':250,'align':'w'}

#connection = sqlite3.connect(r'C:\Users\Shanky\Desktop\Python\Main_Projects\Self_Improvement_Project\data\PersonalData.db')
connection = sqlite3.connect(Database)
cursor = connection.cursor()
#engine = sqlalchemy.create_engine(r'sqlite:///C:\Users\Shanky\Desktop\Python\Main_Projects\Self_Improvement_Project\data\PersonalData.db').connect()
engine = sqlalchemy.create_engine(r'sqlite:///{}'.format(Database)).connect()
#engine = sqlalchemy.create_engine('postgresql://postgres:PhysicsKing123!@database-1.cvz7mc32ef1r.us-east-2.rds.amazonaws.com:5432/postgres')
f = plt.figure(figsize=(15,10))

Categories = ['programming', 'gaming', 'electronics', 'design','finance']
CategoryDict = {"programming":0,"gaming":1,"electronics":0,"design":0,"finance":0}
Counter = 9000
time = "all"
chart = "line"
month = datetime.now().month
year = 365
NewCatEntry = None
NewDateEntry =  None
NewTimeEntry = None
midIndicator = "none"
botIndicator = "none"
DisplayTrend = 0
EntryResponse = ""

def addEntryToDataframe(category, date, duration):
    global EntryResponse

    # Verify that the date is correct
    if (datetime.strptime(date,"%m/%d/%y") > datetime.today()):
        EntryResponse = "Date can not be in the future"
        return
    try:
        month, day, year = date.split('/')
        datetime(int(year), int(month), int(day))
    except ValueError:
        EntryResponse =  "That is not a valid date"
        return

    # Verify that the time entry is correct
    if duration == '0':
        EntryResponse = "No time entered"
        return
    try:
        h, m, s = duration.split(':')
    except ValueError:
        EntryResponse =  "That is not a valid time value"
        return
    else:
        duration = int(h) * 3600 + int(m) * 60 + int(s)

    df = pd.read_sql_table('PersonalData', engine, index_col=1)
    # Use the match function to update the dataframe depending on catagory passed into this function
    if (category == 'programming'):
        new_data = {'date': str(date), 'programming': duration, 'gaming': 0, 'electronics': 0, 'design': 0, 'finance': 0}
    if (category == 'gaming'):
        new_data = {'date': str(date), 'programming': 0, 'gaming': duration, 'electronics': 0, 'design': 0, 'finance': 0}
    if (category == 'electronics'):
        new_data = {'date': str(date), 'programming': 0, 'gaming': 0, 'electronics': duration, 'design': 0, 'finance': 0}
    if (category == 'design'):
        new_data = {'date': str(date), 'programming': 0, 'gaming': 0, 'electronics': 0, 'design': duration, 'finance': 0}
    if (category == 'finance'):
        new_data = {'date': str(date), 'programming': 0, 'gaming': 0, 'electronics': 0, 'design': 0, 'finance': duration}

    # Create a new single row series based off of the new data
    new_row = pd.DataFrame(new_data, index=[0])

    # Append the main dataframe with the new row
    df = df.append(new_row, ignore_index=True)
    # Sort values by date
    df['date'] = pd.to_datetime(df['date'])
    df.sort_values('date', inplace=True)
    # Merge the data for duplicate dates
    df = df.groupby(['date'], as_index=False).sum()

    df.to_sql('PersonalData', engine, if_exists='replace', index=False)
    EntryResponse = "{}min Logged in {} for {}".format(int(duration / 60),category,date)

def getKeyInfo(Category):
    df = pd.read_sql_table('PersonalData', engine, index_col=1)
    df = df[['date',Category]]
    KeyInfo = {}

    # Determine last day logged

    LastDate = df.where(df[Category] > 0).dropna().iloc[-1]['date'].strftime('%m/%d/%y')
    if LastDate == datetime.today().date().strftime('%m/%d/%y'):
        LastDate = "Today"

    # Determine the maximum time in a day
    MaxLogged = df.max().drop('date') / 3600

    # Determine the day max was made
    MaxDay = df.where(df[Category] / 3600 == MaxLogged[Category]).dropna()['date']
    MaxDay = pd.to_datetime(MaxDay.values[0]).strftime('%m/%d/%y')

    # Clean up Max Logged after comparison
    MaxLogged = MaxLogged[Category].round(2)

    # Determine average time logged per day
    CurrentAvgLogged = round(df.iloc[-30:][Category].mean()/60,2)
    PreviousAvgLogged = round(df.iloc[-31:-1][Category].mean()/60,2)
    AvgLoggedChange = round(CurrentAvgLogged - PreviousAvgLogged,2)

    KeyInfo['LastDay'] = LastDate
    KeyInfo['MaxLogged'] = MaxLogged
    KeyInfo['MaxDay'] = MaxDay
    KeyInfo['CurrentAvgLogged'] = CurrentAvgLogged
    KeyInfo['PreviousAvgLogged'] = PreviousAvgLogged
    KeyInfo['AvgLoggedChange'] = AvgLoggedChange

    return KeyInfo

def pieText(values):
    def my_format(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{:.1f}%\n({v:.1f} hours)'.format(pct, v=val/3600)
    return my_format

def printQuote():
    # Open the file of quotes, read json, select a random number
    #f = open('C:\\Users\\Shanky\\Desktop\\Python\\Main_Projects\\Self_Improvement_Project\\quotes.json', encoding='UTF-8')
    f = open('{}\\quotes.json'.format(dirname), encoding='UTF-8')
    quoteData = json.load(f)
    randomNum = random.randint(1, 25)

    # Print the quote and author based off of the random number
    RandomQuote = '''" {} " \nBy {}'''.format(quoteData['quotes'][randomNum]['quote'],quoteData['quotes'][randomNum]['author'])
    return RandomQuote

def enableTrendline(EnaDis):
    global DisplayTrend
    DisplayTrend = EnaDis.get()
    return

def changeChartType(ChartType):
    global chart
    chart = ChartType
    return

def changeCategory(NewCategory, CategoryVal):
    global CategoryDict
    print(NewCategory)
    print(CategoryVal.get())
    CategoryDict[NewCategory] = CategoryVal.get()
    print(CategoryDict)
    return

def changeTimeFrame(NewTimeFrame):
    global time
    time = NewTimeFrame
    return

def changeReqMonth(reqMonth):
    global month
    month = reqMonth
    return

def changeReqYear(reqYear):
    global year
    year = reqYear
    return

def animate(i):
    global category
    global Categories
    global CategoryDict
    global Counter
    global chart
    global time
    global month
    global year
    global DisplayTrend

    df = pd.read_sql_table('PersonalData', engine, index_col=1)

    a = plt.subplot2grid((2,2),(0,0), rowspan=5,colspan= 2)
    #a2 = plt.subplot2grid((6,4),(0,0),rowspan=1,colspan=4, sharex = a)

    data = None
    a.clear()

##################################################
########  MAJOR REWORK REQUIRED  #################

    if time == "today":
        data =  df.tail(1)
    if time == "week":
        data = getDataByCurrentWeek(df)
    elif time == "month":
        data = getDataByMonth(df,month)
    elif time == "year":
        print("here!")
        data = getDataByYear(df,year)
    elif time == "all":
        data = df
##################################################

# Create a data range string to update chart titles
    if time == "today":
        dataRangeStr = "Today"
    else:
        dataRangeStart = data.iloc[0]['date']
        dataRangeEnd = data.iloc[-1]['date']
        dataRangeStr = dataRangeStart.strftime("%m/%d/%y") + " - " + dataRangeEnd.strftime("%m/%d/%y")

# Create a pie chart
    if chart == 'pie':
        explode = [0,0,0,0]

        DateTimeRange = pd.to_datetime(data['date'])
        DataRange = data.drop('date', axis=1)
        CatTotal = DataRange.sum()
        RangeTotal = CatTotal.sum()
        CatPercent = (CatTotal / RangeTotal * 100)
        labels = Categories
        a.pie(CatPercent, labels=labels, autopct= pieText(CatTotal), colors=['g','r','b','purple','yellow'], shadow=True, startangle=90)
        a.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        title = "Percent Time per Category: {}".format(dataRangeStr)
        a.set_title(title)

# Create a bar chart
    elif chart == 'bar':
        labels = ['Programming', 'Gaming', 'Electronics', 'Design','Finance']
        data = data.drop('date', axis=1).sum()
        data = data / 60

        a.bar(labels, data, color=['green', 'red', 'blue', 'purple','yellow'])
        a.set_ylabel('Category Totals (m)')
        a.set_xlabel('Category')
        title = "Total Data Per Category: {}".format(dataRangeStr)
        a.set_title(title)

# Create a line chart
    else:
        ChartData = data
        if CategoryDict["programming"] == 1:

            # Set the x and y for basic line plot
            x_dates = ChartData['date']
            y = ChartData['programming'].cumsum() / 3600
            # If option is select create a trend line
            if DisplayTrend == 1:

                # Set the x values for trendline (convert to num)
                x_num = dates.date2num(x_dates)

                # Calculate the trend line
                trend = np.polyfit(x_num, y, 1)
                fit = np.poly1d(trend)

                # Create the fit
                x_fit = np.linspace(x_num.min(), x_num.max())
                a.plot(dates.num2date(x_fit), fit(x_fit), "g--")
                a.annotate("Slope = {}".format(round(trend[0],2)), xy=(dates.num2date(x_num.mean()), fit(x_fit).mean()),
                           xytext=(dates.num2date(x_num.mean()),fit(x_fit).mean() + y.max()*.2 ),
                           arrowprops=dict(arrowstyle="->", color='black'))
            a.plot_date(x_dates, y, 'g',label='Programming')

        if CategoryDict["gaming"] == 1:
            # Set the x and y for basic line plot
            x_dates = ChartData['date']
            y = ChartData['gaming'].cumsum() / 3600
            # If option is select create a trend line
            if DisplayTrend == 1:

                # Set the x values for trendline (convert to num)
                x_num = dates.date2num(x_dates)

                # Calculate the trend line
                trend = np.polyfit(x_num, y, 1)
                slope = np.polyfit(x_num, y, 1)
                print(slope)
                fit = np.poly1d(trend)

                # Create the fit
                x_fit = np.linspace(x_num.min(), x_num.max())
                a.plot(dates.num2date(x_fit), fit(x_fit), "r--")
                a.annotate("Slope = {}".format(round(trend[0],2)), xy=(dates.num2date(x_num.mean()), fit(x_fit).mean()),
                           xytext=(dates.num2date(x_num.mean()),fit(x_fit).mean() + y.max()*.2 ),
                           arrowprops=dict(arrowstyle="->", color='black'))
            a.plot_date(x_dates, y, 'r',label='Gaming')

        if CategoryDict["electronics"] == 1:
            # Set the x and y for basic line plot
            x_dates = ChartData['date']
            y = ChartData['electronics'].cumsum() / 3600
            # If option is select create a trend line
            if DisplayTrend == 1:

                # Set the x values for trendline (convert to num)
                x_num = dates.date2num(x_dates)

                # Calculate the trend line
                trend = np.polyfit(x_num, y, 1)
                fit = np.poly1d(trend)

                # Create the fit
                x_fit = np.linspace(x_num.min(), x_num.max())
                a.plot(dates.num2date(x_fit), fit(x_fit), "b--")
                a.annotate("Slope = {}".format(round(trend[0],2)), xy=(dates.num2date(x_num.mean()), fit(x_fit).mean()),
                           xytext=(dates.num2date(x_num.mean()),fit(x_fit).mean() + y.max()*.2 ),
                           arrowprops=dict(arrowstyle="->", color='black'))
            a.plot_date(x_dates, y, 'b',label='Electronics')

        if CategoryDict["design"] == 1:
            # Set the x and y for basic line plot
            x_dates = ChartData['date']
            y = ChartData['design'].cumsum() / 3600
            # If option is select create a trend line
            if DisplayTrend == 1:

                # Set the x values for trendline (convert to num)
                x_num = dates.date2num(x_dates)

                # Calculate the trend line
                trend = np.polyfit(x_num, y, 1)
                fit = np.poly1d(trend)

                # Create the fit
                x_fit = np.linspace(x_num.min(), x_num.max())
                a.plot(dates.num2date(x_fit), fit(x_fit), "m--")
                a.annotate("Slope = {}".format(round(trend[0],2)), xy=(dates.num2date(x_num.mean()), fit(x_fit).mean()),
                           xytext=(dates.num2date(x_num.mean()),fit(x_fit).mean() + y.max()*.2 ),
                           arrowprops=dict(arrowstyle="->", color='black'))
            a.plot_date(x_dates,y, 'purple',label='Design')

        if CategoryDict["finance"] == 1:
            # Set the x and y for basic line plot
            x_dates = ChartData['date']
            y = ChartData['finance'].cumsum() / 3600
            # If option is select create a trend line
            if DisplayTrend == 1:

                # Set the x values for trendline (convert to num)
                x_num = dates.date2num(x_dates)

                # Calculate the trend line
                trend = np.polyfit(x_num, y, 1)
                fit = np.poly1d(trend)

                # Create the fit
                x_fit = np.linspace(x_num.min(), x_num.max())
                a.plot(dates.num2date(x_fit), fit(x_fit), "y--")
                a.annotate("Slope = {}".format(round(trend[0],2)), xy=(dates.num2date(x_num.mean()), fit(x_fit).mean()),
                           xytext=(dates.num2date(x_num.mean()), fit(x_fit).mean() + y.max()*.2 ),
                           arrowprops=dict(arrowstyle="->", color='black'))
            a.plot_date(x_dates,y, 'yellow',label='Finance')

        a.set_xlabel("Date")
        a.set_ylabel("Time Logged (h)")
        title = "Data vs Time: {}".format(dataRangeStr)
        a.legend()
        a.xaxis.set_major_locator(mticker.MaxNLocator(30))
        a.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d-%Y"))
        plt.xticks(rotation=45)
        a.set_title(title)

# Add inheritants to the parentheses
class SelfImprovementApp(tk.Tk):
    # Initialize funtion will always run when the class is called
    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self,*args,**kwargs)
        tk.Tk.wm_title(self, "Self Improvment Project")

        container = tk.Frame(self,bg='purple')
        container.grid(row=0,column=0,sticky='nsew')


        # Adding different options to the menu bar
        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar,tearoff=0)
        filemenu.add_separator()
        filemenu.add_command(label="Exit",command=quit)
        menubar.add_cascade(label="File",menu=filemenu)

        # Adding the category change option
        categoryChoice = tk.Menu(menubar,tearoff=0)
        GamingVar = tk.IntVar(self,1)
        categoryChoice.add_checkbutton(label="Gaming", variable = GamingVar, command= lambda: changeCategory("gaming", GamingVar))
        DesignVar = tk.IntVar(self,0)
        categoryChoice.add_checkbutton(label="Design", variable= DesignVar, command=lambda: changeCategory("design", DesignVar))
        ElectronicsVar = tk.IntVar(self,0)
        categoryChoice.add_checkbutton(label="Electronics",  variable= ElectronicsVar, command=lambda: changeCategory("electronics", ElectronicsVar))
        ProgrammingVar = tk.IntVar(self,0)
        categoryChoice.add_checkbutton(label="Programming",variable = ProgrammingVar,command=lambda: changeCategory("programming", ProgrammingVar))
        FinanceVar = tk.IntVar(self,0)
        categoryChoice.add_checkbutton(label="Finance",variable = FinanceVar,command=lambda: changeCategory("finance", FinanceVar))
        menubar.add_cascade(label="Category", menu=categoryChoice)


        # Adding time frame data to the menu bar
        TimeFrame = tk.Menu(menubar,tearoff=0)

        WeekVar = tk.StringVar(self,'week')
        MonthVar = tk.StringVar(self,'month')
        YearVar = tk.StringVar(self,'year')
        AllVar = tk.StringVar(self,'all')

        TimeFrame.add_radiobutton(label="Today",command=lambda: changeTimeFrame('today'))
        TimeFrame.add_radiobutton(label="Week",command=lambda: changeTimeFrame('week'))
        TimeFrame.add_radiobutton(label="Month", command=lambda: changeTimeFrame('month'))
        TimeFrame.add_radiobutton(label="Year", command=lambda: changeTimeFrame('year'))
        TimeFrame.add_radiobutton(label="All Time", command=lambda: changeTimeFrame('all'))
        menubar.add_cascade(label= "Data Time Frame", menu=TimeFrame)

        # Adding the graph type option
        ChartType = tk.Menu(menubar, tearoff=0)
        ChartType.add_radiobutton(label="Bar Chart", command=lambda: changeChartType('bar'))
        ChartType.add_radiobutton(label = "Line Chart", command = lambda: changeChartType('line'))
        ChartType.add_radiobutton(label = "Pie Chart",command = lambda: changeChartType('pie'))
        menubar.add_cascade(label="Chart Type",menu = ChartType)

        ReqMonth = tk.Menu(menubar, tearoff=1)
        ReqMonth.add_radiobutton(label="January", command=lambda: changeReqMonth(1))
        ReqMonth.add_radiobutton(label="February", command=lambda: changeReqMonth(2))
        ReqMonth.add_radiobutton(label="March", command=lambda: changeReqMonth(3))
        ReqMonth.add_radiobutton(label="April", command=lambda: changeReqMonth(4))
        ReqMonth.add_radiobutton(label="May", command=lambda: changeReqMonth(5))
        ReqMonth.add_radiobutton(label="June", command=lambda: changeReqMonth(6))
        ReqMonth.add_radiobutton(label="July", command=lambda: changeReqMonth(7))
        ReqMonth.add_radiobutton(label="August", command=lambda: changeReqMonth(8))
        ReqMonth.add_radiobutton(label="September", command=lambda: changeReqMonth(9))
        ReqMonth.add_radiobutton(label="October", command=lambda: changeReqMonth(10))
        ReqMonth.add_radiobutton(label="November", command=lambda: changeReqMonth(11))
        ReqMonth.add_radiobutton(label="December", command=lambda: changeReqMonth(12))


        menubar.add_cascade(label="Month", menu=ReqMonth)

        # Add options for years
        ReqYear = tk.Menu(menubar, tearoff=0)
        ReqYear.add_radiobutton(label="2021", command=lambda: changeReqYear(2021))
        ReqYear.add_radiobutton(label="2022", command=lambda: changeReqYear(2022))
        ReqYear.add_radiobutton(label="Last 365 days", command=lambda: changeReqYear(365))

        menubar.add_cascade(label="Year", menu=ReqYear)

        # Add menu for graph options
        GraphOptions = tk.Menu(menubar, tearoff=0)
        EnableTrendline = tk.IntVar(self, 0)
        GraphOptions.add_checkbutton(label="Add Trendline", variable=EnableTrendline,command=lambda: enableTrendline(EnableTrendline))
        # GraphOptions.add_command(label="Show Trend Line (TBD)")
        # GraphOptions.add_command(label="TBD")
        # GraphOptions.add_command(label="TBD")

        menubar.add_cascade(label="Graph Options", menu=GraphOptions)

        # Adding top indicators (which will be adjusted for my application)
        tk.Tk.config(self, menu=menubar)

    # Eventually we will have a bunch of frames, they will all exist but one will be on top and can change
        self.frames = {}

        for F in (StartPage, Visaulization_Page,Data_Table_Page,New_Entry_Page):
            frame = F(container,self)
            self.frames[F] = frame
            frame.grid(row=0,column=0,sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self,cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self,parent,controller):
        today = datetime.today().date()
        now = datetime.now()
        tk.Frame.__init__(self,parent)
        self.grid_propagate(1)

        # Set the row and columns configurations


        # Set the row and columns configurations
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)

        self.grid_rowconfigure(5, weight=5)

        top_label = tk.Label(self,text="""Self Improvement Application""", font=XLARGE_FONT,bg="#89CFF0",width=50, height=0).grid(sticky='nsew',row=0,column=0,columnspan=5)

        button01 = tk.Button(self,text="Start Page", command=lambda: controller.show_frame(StartPage),height=5,bg='#C0C0C0').grid(sticky='nsew',row=1,column=0,rowspan=1)
        button02 = tk.Button(self,text="Graph Page", command=lambda: controller.show_frame(Visaulization_Page), height=5).grid(sticky='nsew',row=1,column=1,rowspan=1)
        button03 = tk.Button(self,text="Data Table", command=lambda: controller.show_frame(Data_Table_Page),height=5).grid(sticky='nsew',row=1,column=2,rowspan=1)
        button04 = tk.Button(self,text="New Entry", command=lambda: controller.show_frame(New_Entry_Page),height=5).grid(sticky='nsew',row=1,column=3,rowspan=1)
        button05 = tk.Button(self, text="Exit Application", command=exit, height=5).grid(sticky='nsew',row=1,column=4,rowspan=1)

        label02 = tk.Label(self,text="{}".format(printQuote()),font=LARGE_FONT,wraplength=1000,borderwidth = 5,relief="raised").grid(sticky='n',row=3,column=0,columnspan=5,rowspan=2,pady = 50, ipady=50)
        self.time_label = tk.Label(self, text= "fuck", font=NORM_FONT, width=10, height=5)
        self.time_label.grid(sticky='s', row=2, column=0, columnspan=5)

        ########   Key information section  #########
        i = -1
        CatFrame = tk.Frame(self, height=250, width=0, relief='sunken', borderwidth=10)
        CatFrame.grid(sticky='new', row=5, column=0,columnspan=5, rowspan=1)
        CatFrame.grid_propagate(0)
        for Category in Categories:
            i = i +1
            CatFrame.columnconfigure(i,weight=1)
            KeyInfo = getKeyInfo(Category)
            CatTitle = tk.Label(CatFrame, text="{}".format(Category.capitalize()), font=NORM_FONT)
            CatTitle.grid(column=i, row=0)
            loggedToday = tk.Label(CatFrame, text="Last logged {}".format(KeyInfo['LastDay']), font=100).grid(column=i, row=1)
            maxLogged = tk.Label(CatFrame, text="Max Log of {}h on {}".format(KeyInfo['MaxLogged'],KeyInfo['MaxDay']), font=25).grid(column=i, row=2)
            CurrentAvgLogged = tk.Label(CatFrame, text="Current 30 Day Avg {} min".format(KeyInfo['CurrentAvgLogged']), font=25).grid(column=i, row=3)
            PreviousAvgLogged = tk.Label(CatFrame, text="Prev Avg: {} min".format(KeyInfo['PreviousAvgLogged']),font=25).grid(column=i, row=4)
            AvgChange = tk.Label(CatFrame, text="Change (+/-): {} min".format(KeyInfo['AvgLoggedChange']),font=25).grid(column=i, row=5)

        self.updateClock()

    def updateClock(self):
        date = datetime.today().strftime("%m/%d/%y")
        time = datetime.today().strftime("%I:%M:%S %p")
        self.time_label.configure(text=time + "\n" + date)
        self.time_label.after(1000, self.updateClock)

class Visaulization_Page(tk.Frame):
    def __init__(self, parent,controller):
        tk.Frame.__init__(self,parent, bg='blue')


        # Set the row and columns configurations
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)

        self.grid_rowconfigure(2, weight=1)

        top_label = tk.Label(self,text="Data Charts",bg="#89CFF0",font=XLARGE_FONT, height=0).grid(sticky='nsew',row=0,column=0,columnspan=5)

        button01 = tk.Button(self,text="Start Page", command=lambda: controller.show_frame(StartPage),height=5).grid(sticky='nsew',row=1,column=0,rowspan=1)
        button02 = tk.Button(self,text="Graph Page", command=lambda: controller.show_frame(Visaulization_Page), height=5,bg='#C0C0C0').grid(sticky='nsew',row=1,column=1,rowspan=1)
        button03 = tk.Button(self,text="Data Table", command=lambda: controller.show_frame(Data_Table_Page),height=5).grid(sticky='nsew',row=1,column=2,rowspan=1)
        button04 = tk.Button(self,text="New Entry", command=lambda: controller.show_frame(New_Entry_Page),height=5).grid(sticky='nsew',row=1,column=3,rowspan=1)
        button05 = tk.Button(self, text="Exit Application", command=exit, height=5).grid(sticky='nsew',row=1,column=4,rowspan=1)

        canvas = FigureCanvasTkAgg(f,self)
        canvas.get_tk_widget().grid(sticky='nsew',row=1,column=0,columnspan=5,rowspan=2)
        canvas.draw()

        tooldbar_frame = tk.Frame(self).grid(row=0,column=0,rowspan=6)
        toolbar = NavigationToolbar2Tk(canvas,tooldbar_frame).pack()
        canvas._tkcanvas.grid(row=2,column=0,rowspan=6,columnspan=5)

class Data_Table_Page(tk.Frame):
    def __init__(self, parent,controller):
        tk.Frame.__init__(self,parent)


        # Set the row and columns configurations
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)

        self.grid_rowconfigure(2, weight=1)

        top_label = tk.Label(self,text="Data Table", font=XLARGE_FONT,bg="#89CFF0",width=50, height=0).grid(sticky='nsew',row=0,column=0,columnspan=5)

        button01 = tk.Button(self,text="Start Page", command=lambda: controller.show_frame(StartPage),height=5).grid(sticky='nsew',row=1,column=0,rowspan=1)
        button02 = tk.Button(self,text="Graph Page", command=lambda: controller.show_frame(Visaulization_Page), height=5).grid(sticky='nsew',row=1,column=1,rowspan=1)
        button03 = tk.Button(self,text="Data Table", command=lambda: controller.show_frame(Data_Table_Page),height=5,bg='#C0C0C0').grid(sticky='nsew',row=1,column=2,rowspan=1)
        button04 = tk.Button(self,text="New Entry", command=lambda: controller.show_frame(New_Entry_Page),height=5).grid(sticky='nsew',row=1,column=3,rowspan=1)
        button05 = tk.Button(self, text="Exit Application", command=exit, height=5).grid(sticky='nsew',row=1,column=4,rowspan=1)


        df = pd.read_sql_table('PersonalData', engine, index_col=1)
        df['date'] = pd.to_datetime(df['date']).dt.date
        TableFrame = tk.Frame(self)
        TableFrame.grid(row=2,column=0,rowspan=6,columnspan=5,sticky='nsew')
        pt = Table(TableFrame, dataframe= df, cellsize=500)
        pt.sortTable(0,0)
        config.apply_options(options, pt)
        pt.show()

class New_Entry_Page(tk.Frame):
    def __init__(self, parent,controller):
        tk.Frame.__init__(self,parent)


        # Set the row and columns configurations
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)

        self.grid_rowconfigure(2, weight=1)

        top_label = tk.Label(self,text="Submit New Entry", font=XLARGE_FONT,bg="#89CFF0",width=50, height=0).grid(sticky='nsew',row=0,column=0,columnspan=5)

        button01 = tk.Button(self,text="Start Page", command=lambda: controller.show_frame(StartPage),height=5).grid(sticky='nsew',row=1,column=0,rowspan=1)
        button02 = tk.Button(self,text="Graph Page", command=lambda: controller.show_frame(Visaulization_Page), height=5).grid(sticky='nsew',row=1,column=1,rowspan=1)
        button03 = tk.Button(self,text="Data Table", command=lambda: controller.show_frame(Data_Table_Page),height=5).grid(sticky='nsew',row=1,column=2,rowspan=1)
        button04 = tk.Button(self,text="New Entry", command=lambda: controller.show_frame(New_Entry_Page),height=5,bg='#C0C0C0').grid(sticky='nsew',row=1,column=3,rowspan=1)
        button05 = tk.Button(self, text="Exit Application", command=exit, height=5).grid(sticky='nsew',row=1,column=4,rowspan=1)

        # New Entry Section
        Entry_Frame = tk.Frame(self, relief='sunken', borderwidth=10,width=15)
        Entry_Frame.grid_propagate(0)
        Entry_Frame.grid(row=2,column=1,rowspan=6,columnspan=3,sticky='nsew')

        LabelFrame = tk.Frame(Entry_Frame,width=900, height=50)
        LabelFrame.grid_propagate(False)
        LabelFrame.grid(column=0,row=2, columnspan=3)
        LabelFrame.grid_columnconfigure(0, weight=1)
        LabelFrame.grid_columnconfigure(1, weight=1)
        LabelFrame.grid_columnconfigure(2, weight=1)

        CategoryLabel = tk.Label(LabelFrame, text="Category", font=('Helvetica 25 underline bold')).grid(column = 0,row=1, padx = 5, sticky="W")
        DateLabel = tk.Label(LabelFrame, text="Date", font=('Helvetica 25 underline bold')).grid(column = 1,row=1,padx = 75, sticky="NSEW")
        TimeLabel = tk.Label(LabelFrame, text="Duration", font=('Helvetica 25 underline bold')).grid(column = 2,row=1, padx = 25,sticky="EW")

        RadioButtonFrame = tk.Frame(Entry_Frame, height=500)
        RadioButtonFrame.grid(column = 0,row=3, pady = 5, sticky="W")

        DateFrame = tk.Frame(Entry_Frame)
        DateFrame.grid(column = 1, row=3, pady = 5, sticky="W")

        TimeFrame = tk.Frame(Entry_Frame)
        TimeFrame.grid(column = 2,row=3, pady = 5, stick="W")

        # Create the radio button frame
        self.categoryStr = tk.StringVar(self,value="gaming")

        CategoryEntry01 = tk.Radiobutton(RadioButtonFrame, text = "Gaming", variable = self.categoryStr,value="gaming", font=RADIO_FONT)
        CategoryEntry01.grid(column = 1, padx = 15, pady = 1, sticky="W")
        CategoryEntry02 = tk.Radiobutton(RadioButtonFrame, text = "Programming", variable = self.categoryStr,value="programming", font=RADIO_FONT)
        CategoryEntry02.grid(column = 1, padx = 15, pady = 1, sticky="W")
        CategoryEntry03 = tk.Radiobutton(RadioButtonFrame, text = "Design", variable = self.categoryStr,value="design", font=RADIO_FONT)
        CategoryEntry03.grid(column = 1, padx = 15, pady = 1, sticky="W")
        CategoryEntry04 = tk.Radiobutton(RadioButtonFrame, text = "Electronics", variable = self.categoryStr,value="electronics", font=RADIO_FONT)
        CategoryEntry04.grid(column = 1, padx = 15, pady = 1, sticky="W")
        CategoryEntry05 = tk.Radiobutton(RadioButtonFrame, text = "Finance", variable = self.categoryStr,value="finance", font=RADIO_FONT)
        CategoryEntry05.grid(column = 1, padx = 15, pady = 1, sticky="W")

        # Date entry frame
        self.cal = Calendar(DateFrame, selectmode='day',year=datetime.today().year, month=datetime.today().month,day=datetime.today().day)
        self.cal.grid(column = 2,row=2, padx = 15, pady = 5)

        # Time Entry
        self.TimeEntry = tk.Text(TimeFrame,width=10,height=1, font=LARGE_FONT)
        self.TimeEntry.insert(1.0, "0")
        self.TimeEntry.grid(column = 1,row=2, pady = 25)

        SubmitButton = tk.Button(TimeFrame, text="Submit Entry",width=25,height=5, command= self.updateOutput).grid(column = 1,row=3, pady = 5)

        self.OutputText = tk.Text(Entry_Frame,width=50,height=20, font=LARGE_FONT)
        self.OutputText.grid(column = 0,row=4,columnspan=3, pady = 5)

    def updateOutput(self):
        addEntryToDataframe(self.categoryStr.get(), self.cal.get_date(), self.TimeEntry.get("1.0", 'end-1c'))
        self.OutputText.insert('end', EntryResponse + "\n")


app = SelfImprovementApp()
app.geometry("1500x1200")
ani = animation.FuncAnimation(f, animate, interval=1000)
app.update()
app.mainloop()
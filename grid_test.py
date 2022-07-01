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
import matplotlib.ticker as mticker
import pandastable
import datetime
from pandastable import Table, TableModel,config

matplotlib.use("TkAgg")
style.use("ggplot")
import json
import os

# Import local functions
from GUI_Functions import *

LARGE_FONT = ("Verdana",20)
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

def getKeyInfo(Category):
    df = pd.read_sql_table('PersonalData', engine, index_col=1)
    df = df[['date',Category]]
    KeyInfo = {}

    # Determine last day logged
    LastDate = df.where(df[Category] > 0).dropna().iloc[-1]

    # Determine the maximum time in a day
    MaxSpent = df.max().drop('date') / 3600

    # Determine the day max was made
    MaxDay = df.where(df['gaming'] / 3600 == MaxSpent['gaming']).dropna()['date']
    MaxDay = pd.to_datetime(MaxDay.values[0]).strftime('%m/%d/%y')

    KeyInfo['LastDay'] = LastDate
    KeyInfo['MaxSpent'] = MaxSpent
    KeyInfo['MaxDay'] = MaxDay

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
    RandomQuote = '''Motivational Quote:\n " {} " \nBy {}'''.format(quoteData['quotes'][randomNum]['quote'],quoteData['quotes'][randomNum]['author'])
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
        a.pie(CatPercent, labels=labels, autopct= pieText(CatTotal), colors=['g','r','b','purple'], shadow=True, startangle=90)
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

        top_label = tk.Label(self,text="""Self Improvement Application""", font=NORM_FONT,bg="#89CFF0",width=50, height=5).grid(sticky='nsew',row=0,column=0,columnspan=5)

        button01 = tk.Button(self,text="Start Page", command=lambda: controller.show_frame(StartPage),height=5,bg='#C0C0C0').grid(sticky='nsew',row=1,column=0,rowspan=1)
        button02 = tk.Button(self,text="Graph Page", command=lambda: controller.show_frame(Visaulization_Page), height=5).grid(sticky='nsew',row=1,column=1,rowspan=1)
        button03 = tk.Button(self,text="Data Table", command=lambda: controller.show_frame(Data_Table_Page),height=5).grid(sticky='nsew',row=1,column=2,rowspan=1)
        button04 = tk.Button(self,text="New Entry", command=lambda: controller.show_frame(New_Entry_Page),height=5).grid(sticky='nsew',row=1,column=3,rowspan=1)
        button05 = tk.Button(self, text="Exit Application", command=exit, height=5).grid(sticky='nsew',row=1,column=4,rowspan=1)

        self.time_label = tk.Label(self, text= "fuck", font=NORM_FONT, width=50, height=5)
        self.time_label.grid(sticky='s', row=2, column=0, columnspan=5)
        label02 = tk.Label(self,text="{}".format(printQuote()),font=LARGE_FONT,wraplength=500).grid(sticky='new',row=3,column=0,columnspan=5,rowspan=2)

        ########   Key information section  #########

        # Gaming Information
        gamingKeyInfo = getKeyInfo('gaming')
        gamingFrame = tk.Frame(self,bg='red',height=1000).grid(sticky='new',row=5,column=0, rowspan=1)
        loggedToday = tk.Label(gamingFrame, text="fuck fuck fuck", font=100)
        loggedToday.pack(side='top', expand=True)

        programmingFrame = tk.Frame(self,bg='green',height=1000).grid(sticky='new',row=5,column=1,rowspan=1)
        electronicsFrame = tk.Frame(self,bg='blue',height=1000).grid(sticky='new',row=5,column=2,rowspan=1)
        designFrame = tk.Frame(self,bg='purple',height=1000).grid(sticky='new',row=5,column=3,rowspan=1)
        finacenFrame = tk.Frame(self,bg='yellow',height=1000).grid(sticky='new',row=5,column=4,rowspan=1)

        ###############################################

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

        top_label = tk.Label(self,text="Data Charts",bg="#89CFF0",font=NORM_FONT, height=5).grid(sticky='nsew',row=0,column=0,columnspan=5)

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

        top_label = tk.Label(self,text="Data Table", font=NORM_FONT,bg="#89CFF0",width=50, height=5).grid(sticky='nsew',row=0,column=0,columnspan=5)

        button01 = tk.Button(self,text="Start Page", command=lambda: controller.show_frame(StartPage),height=5).grid(sticky='nsew',row=1,column=0,rowspan=1)
        button02 = tk.Button(self,text="Graph Page", command=lambda: controller.show_frame(Visaulization_Page), height=5).grid(sticky='nsew',row=1,column=1,rowspan=1)
        button03 = tk.Button(self,text="Data Table", command=lambda: controller.show_frame(Data_Table_Page),height=5,bg='#C0C0C0').grid(sticky='nsew',row=1,column=2,rowspan=1)
        button04 = tk.Button(self,text="New Entry", command=lambda: controller.show_frame(New_Entry_Page),height=5).grid(sticky='nsew',row=1,column=3,rowspan=1)
        button05 = tk.Button(self, text="Exit Application", command=exit, height=5).grid(sticky='nsew',row=1,column=4,rowspan=1)


        df = pd.read_sql_table('PersonalData', engine, index_col=1)
        df['date'] = pd.to_datetime(df['date']).dt.date
        entry_frame = tk.Frame(self)
        entry_frame.grid(row=2,column=0,rowspan=6,columnspan=5,sticky='nsew')
        pt = Table(entry_frame, dataframe= df, cellsize=500)
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

        top_label = tk.Label(self,text="Submit New Entry", font=NORM_FONT,bg="#89CFF0",width=50, height=5).grid(sticky='nsew',row=0,column=0,columnspan=5)

        button01 = tk.Button(self,text="Start Page", command=lambda: controller.show_frame(StartPage),height=5).grid(sticky='nsew',row=1,column=0,rowspan=1)
        button02 = tk.Button(self,text="Graph Page", command=lambda: controller.show_frame(Visaulization_Page), height=5).grid(sticky='nsew',row=1,column=1,rowspan=1)
        button03 = tk.Button(self,text="Data Table", command=lambda: controller.show_frame(Data_Table_Page),height=5).grid(sticky='nsew',row=1,column=2,rowspan=1)
        button04 = tk.Button(self,text="New Entry", command=lambda: controller.show_frame(New_Entry_Page),height=5,bg='#C0C0C0').grid(sticky='nsew',row=1,column=3,rowspan=1)
        button05 = tk.Button(self, text="Exit Application", command=exit, height=5).grid(sticky='nsew',row=1,column=4,rowspan=1)


app = SelfImprovementApp()
app.geometry("1500x1200")
ani = animation.FuncAnimation(f, animate, interval=1000)
app.update()
app.mainloop()
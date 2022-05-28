# Import tkinter
import tkinter as tk
# ttk is basically the css for tkinter
from tkinter import ttk

# Import matplotlib libraries
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
matplotlib.use("TkAgg")
style.use("ggplot")
import json

# Import local functions
from GUI_Functions import *

LARGE_FONT = ("Verdana",12)
NORM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)


connection = sqlite3.connect(r'C:\Users\Shanky\Desktop\Python\Main_Projects\Self_Improvement_Project\data\PersonalData.db')
cursor = connection.cursor()
engine = sqlalchemy.create_engine(r'sqlite:///C:\Users\Shanky\Desktop\Python\Main_Projects\Self_Improvement_Project\data\PersonalData.db').connect()

f = Figure()
a = f.add_subplot(111)

Categories = ['programming', 'gaming', 'electronics', 'design']
CategoryDict = {"programming":0,"gaming":1,"electronics":0,"design":0}
Counter = 9000
time = "all"
chart = "line"
month = datetime.now().month
year = 365
NewDateEntry =  None
midIndicator = "none"
botIndicator = "none"

def printQuote():
    # Open the file of quotes, read json, select a random number
    f = open('C:\\Users\\Shanky\\Desktop\\Python\\Main_Projects\\Self_Improvement_Project\\quotes.json', encoding='UTF-8')
    quoteData = json.load(f)
    randomNum = random.randint(1, 25)

    # Print the quote and author based off of the random number
    RandomQuote = '''Motivational Quote:\n " {} " \nBy {}'''.format(quoteData['quotes'][randomNum]['quote'],quoteData['quotes'][randomNum]['author'])
    return RandomQuote

def addNewEntry():
    NewEntry = tk.Tk()
    NewEntry.wm_title("New Data Entry")
    label = ttk.Label(NewEntry, text="Please enter a date")
    label.pack(side="top",fill="x",pady=10)
    DateEntry = ttk.Entry(NewEntry)
    DateEntry.insert(0,14)
    DateEntry.pack()
    DateEntry.focus_set()

    def callback():
        global NewDateEntry
        temp = DateEntry.get()
        NewDateEntry = temp

    button01 = ttk.Button(NewEntry, text = "Submit", width = 10, command=callback).pack()
    tk.mainloop()

def changeChartType(ChartType):
    global chart
    chart = ChartType
    return

def changeCategory(NewCategory, CategoryVal):
    global CategoryDict
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

def popupmsg(msg):
    popup = tk.Tk()

    popup.wm_title("!")
    label = ttk.Label(popup,text=msg,font=NORM_FONT)
    label.pack(side="top",fill="x",pady=10)
    B1 = ttk.Button(popup,text="Okay",command= popup.destroy)
    B1.pack()

def animate(i):
    global category
    global Categories
    global CategoryDict
    global Counter
    global chart
    global time
    global month
    global year


    df = pd.read_sql_table('PersonalData', engine, index_col=1)

    data = None

    if time == "week":
        data = getDataByCurrentWeek(df)
    elif time == "month":
        data = getDataByMonth(df,month)
    elif time == "year":
        print("here!")
        data = getDataByYear(df,year)
    elif time == "all":
        data = df

    a.clear()

# Create a pie chart
    if chart == 'pie':
        explode = [0,0,0,0]

        DateTimeRange = pd.to_datetime(data['date'])
        DataRange = data.drop('date', axis=1)
        CatTotal = DataRange.sum()
        RangeTotal = CatTotal.sum()
        CatPercent = (CatTotal / RangeTotal * 100)
        DateStart = datetime.strftime(DateTimeRange.iloc[0].date(), "%m-%d-%y")
        DateEnd = datetime.strftime(DateTimeRange.iloc[-1].date(), "%m-%d-%y")
        labels = Categories
        a.pie(CatPercent, labels=labels, autopct='%1.1f%%', explode = explode, shadow=True, startangle=90)
        a.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        title = "Percent Time per Category from {} to {}".format(DateStart,DateEnd)

# Create a bar chart
    elif chart == 'bar':
        labels = ['Programming', 'Gaming', 'Electronics', 'Design']
        data = data.drop('date', axis=1).sum()
        data = data / 60

        a.bar(labels, data, color=['green', 'red', 'blue', 'purple'])
        a.set_ylabel('Category Totals (m)')
        a.set_xlabel('Category')
        title = "Gaming data vs Time"

# Display the data table only
    elif chart == 'table':
        a.table(cellText=data)
        title = "Gaming data vs Time"

# Create a line chart
    else:
        ChartData = data
        if CategoryDict["programming"] == 1:
            a.plot_date(ChartData['date'], ChartData['programming'].cumsum(), 'g')
        if CategoryDict["gaming"] == 1:
            a.plot_date(ChartData['date'], ChartData['gaming'].cumsum(), 'r')
        if CategoryDict["electronics"] == 1:
            a.plot_date(ChartData['date'], ChartData['electronics'].cumsum(), 'b')
        if CategoryDict["design"] == 1:
            a.plot_date(ChartData['date'], ChartData['design'].cumsum(), 'orange')

        title = "Data vs Time"


    a.legend()
    a.set_title(title)

# Add inheritants to the parentheses
class SelfImprovementApp(tk.Tk):
    # Initialize funtion will always run when the class is called
    def __init__(self,*args,**kwargs):
    # What is self? Name self is convention, could be named anything
    # What are args/kwarg?
        tk.Tk.__init__(self,*args,**kwargs)

        #tk.Tk.iconbitmap(self,default="images/icon.ico")
        tk.Tk.wm_title(self, "Self Improvment Project")

        container = tk.Frame(self)

        # Pack widget, top of window, ????
        container.pack(side="top",fill="both",expand= True)

        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0, weight=1)


        # Adding different options to the menu bar
        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar,tearoff=0)
        filemenu.add_command(label="Save Settings",command=lambda: popupmsg("Not support just yet!"))
        filemenu.add_separator()
        filemenu.add_command(label="Add Entry", command=lambda: addNewEntry())
        filemenu.add_command(label="Exit",command=quit)
        menubar.add_cascade(label="File",menu=filemenu)

        # Adding the category change option
        categoryChoice = tk.Menu(menubar,tearoff=1)
        GamingVar = tk.IntVar(self,1)
        categoryChoice.add_checkbutton(label="Gaming", variable = GamingVar, onvalue=1,offvalue=0, command= lambda: changeCategory("gaming", GamingVar))
        DesignVar = tk.IntVar()
        categoryChoice.add_checkbutton(label="Design", variable= DesignVar, onvalue=1,offvalue=0, command=lambda: changeCategory("design", DesignVar))
        ElectronicsVar = tk.IntVar()
        categoryChoice.add_checkbutton(label="Electronics",  variable= ElectronicsVar, command=lambda: changeCategory("electronics", ElectronicsVar))
        ProgrammingVar = tk.IntVar()
        categoryChoice.add_checkbutton(label="Programming",variable = ProgrammingVar, onvalue=1,offvalue=0,command=lambda: changeCategory("programming", ProgrammingVar))
        menubar.add_cascade(label="Category", menu=categoryChoice)

        # Adding time frame data to the menu bar
        TimeFrame = tk.Menu(menubar,tearoff=1)
        TimeFrame.add_command(label="Week",command=lambda: changeTimeFrame('week'))
        TimeFrame.add_command(label="Month", command=lambda: changeTimeFrame('month'))
        TimeFrame.add_command(label="Year", command=lambda: changeTimeFrame('year'))
        TimeFrame.add_command(label="All Time", command=lambda: changeTimeFrame('all'))
        menubar.add_cascade(label= "Data Time Frame", menu=TimeFrame)

        # Adding the graph type option
        ChartType = tk.Menu(menubar, tearoff=1)
        ChartType.add_command(label="Bar Chart", command=lambda: changeChartType('bar'))
        ChartType.add_command(label = "Line Chart", command = lambda: changeChartType('line'))
        ChartType.add_command(label = "Pie Chart", command = lambda: changeChartType('pie'))
        ChartType.add_command(label = "Table", command = lambda: changeChartType('table'))
        menubar.add_cascade(label="Chart Type",menu = ChartType)

        # Add month options
        ReqMonth = tk.Menu(menubar, tearoff=1)
        ReqMonth.add_command(label="January", command=lambda: changeReqMonth(1))
        ReqMonth.add_command(label="February", command=lambda: changeReqMonth(2))
        ReqMonth.add_command(label="March", command=lambda: changeReqMonth(3))
        ReqMonth.add_command(label="April", command=lambda: changeReqMonth(4))
        ReqMonth.add_command(label="May", command=lambda: changeReqMonth(5))
        ReqMonth.add_command(label="June", command=lambda: changeReqMonth(6))
        ReqMonth.add_command(label="July", command=lambda: changeReqMonth(7))
        ReqMonth.add_command(label="August", command=lambda: changeReqMonth(8))
        ReqMonth.add_command(label="September", command=lambda: changeReqMonth(9))
        ReqMonth.add_command(label="October", command=lambda: changeReqMonth(10))
        ReqMonth.add_command(label="November", command=lambda: changeReqMonth(11))
        ReqMonth.add_command(label="December", command=lambda: changeReqMonth(12))

        menubar.add_cascade(label="Month", menu=ReqMonth)

        # Add options for years
        ReqYear = tk.Menu(menubar, tearoff=1)
        ReqYear.add_command(label="2021", command=lambda: changeReqYear(2021))
        ReqYear.add_command(label="2022", command=lambda: changeReqYear(2022))
        ReqYear.add_command(label="Last 365 days", command=lambda: changeReqYear(365))

        menubar.add_cascade(label="Year", menu=ReqYear)

        # Adding top indicators (which will be adjusted for my application)
        topIndi = tk.Menu(menubar,tearoff=1)
        topIndi.add_command(label="Add Entry", command = lambda: addNewEntry("test"))
        menubar.add_cascade(label="Add Entry",menu=topIndi)

        # Adding top indicators (which will be adjusted for my application)
        mainIndi = tk.Menu(menubar, tearoff=1)
        mainIndi.add_command(label="None", command=lambda: addNewEntry("test2"))
        menubar.add_cascade(label="Main Indicator", menu=mainIndi)

        # Adding top indicators (which will be adjusted for my application)
        botIndi = tk.Menu(menubar, tearoff=1)
        botIndi.add_command(label="None", command=lambda: addNewEntry("test3"))
        menubar.add_cascade(label="Bottom Indicator", menu=botIndi)

        tk.Tk.config(self, menu=menubar)

    # Eventually we will have a bunch of frames, they will all exist but one will be on top and can change
        self.frames = {}

        for F in (StartPage,PageOne,PageTwo, Visaulization_Page):
            frame = F(container,self)
            self.frames[F] = frame

            frame.grid(row=0,column=0,sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self,cont):
        frame = self.frames[cont]
        frame.tkraise()

def qf(stringtoprint):
    print(stringtoprint)

class StartPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self,text="""Self Improvement Application\nBetter Everyday""", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        # The way that command works is that it runs the function on load, the way around it is using lambda
        # Example:
        label02 = tk.Label(self,text="{}".format(printQuote()),font=LARGE_FONT).pack()
        button1 = ttk.Button(self,text="Enter", command=lambda: controller.show_frame(Visaulization_Page)).pack()
        button3 = ttk.Button(self, text="Exit", command=quit).pack()

class PageOne(tk.Frame):
    def __init__(self, parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self,text="Page 1", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button2 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage)).pack()
        button3 = ttk.Button(self, text="Visit Page 2", command=lambda: controller.show_frame(PageTwo)).pack()

class PageTwo(tk.Frame):
    def __init__(self, parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self,text="Page 2", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button4 = ttk.Button(self, text="Visit Page 1", command=lambda: controller.show_frame(PageOne)).pack()

class Visaulization_Page(tk.Frame):
    def __init__(self, parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self,text="Graph Display", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button7 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage)).pack()

        canvas = FigureCanvasTkAgg(f,self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand=True)
        toolbar = NavigationToolbar2Tk(canvas,self)
        canvas._tkcanvas.pack(side=tk.TOP,fill=tk.BOTH,expand=True)

app = SelfImprovementApp()
app.geometry("1280x720")
ani = animation.FuncAnimation(f, animate, interval=1000)
app.mainloop()
from time import time
from tkinter import *
from datetime import datetime
from datetime import timedelta

root = Tk()
root.title("Stopwatch")
root.geometry('400x200')

Stop = False
Start = False
Clear = False
TotalTime = timedelta(seconds=0)

def updateTime():
    global TotalTime
    global Stop
    global Start

    if(Start == True):
        TotalTime += timedelta(seconds=1)
    TimeLabel.config(text="0" + str(TotalTime))
    print(TotalTime)
    TimeLabel.after(1000, updateTime)

def watchStart():
    global Start
    global Stop
    global TotalTime

    Stop = False
    Start = True

    StartButton.grid_remove()

def watchStop():
    global Start
    global Stop

    Start = False
    Stop = True

    StartButton.grid(row=1, column=1, padx=1, pady=1, ipadx=9, sticky=E)

def watchClear():
    global TotalTime
    TotalTime = timedelta(seconds=0)

def submitTime():
    global TotalTime
    return TotalTime

# Set the current time to 00:00:00
ZeroTime = "00:00:00"

TimeLabel = Label(root, text=ZeroTime, font=('ariel 80', 40), bg='Black', fg='green', relief='groove', borderwidth=5)
TimeLabel.grid(row=0, column=0, columnspan=2, padx=2, pady=2, sticky=EW)

StopButton = Button(root, text='STOP', height=3,width=10, command=watchStop)
StopButton.grid(row=1, column=0, padx=1, pady=1, ipadx=9, sticky=EW)
StartButton = Button(root, text='START',height=3,width=10, command=watchStart)
StartButton.grid(row=1, column=0, padx=2, pady=1, ipadx=9, sticky=EW)
ClearButton = Button(root, text='CLEAR',height=3,width=10, command=watchClear)
ClearButton.grid(row=1, column=1, padx=1, pady=1, ipadx=9, sticky=EW)
SubmitButton = Button(root, text='SUBMIT',height=3,width=10, command=submitTime)
SubmitButton.grid(row=2, column=0, columnspan=2, padx=1, pady=1, ipadx=4,sticky=EW)

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)


root.after(1000,updateTime)
root.mainloop()

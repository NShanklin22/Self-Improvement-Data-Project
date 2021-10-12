from tkinter import *
from tkinter import ttk
from tkinter import messagebox

def create_input_frame(container):
    frame = ttk.Frame(container)

    #Creating the input box
    ttk.Label(frame, text="Category:").grid(column=0, row=0, sticky=W)
    ttk.Label(frame, text="Date:").grid(column=0, row=1, sticky=W)
    ttk.Label(frame, text="Duration:").grid(column=0,row=2,sticky=W)

    #Creating the category entry
    global category
    category = ttk.Entry(frame, width=25)
    category.focus()
    category.grid(column=1, row=0,padx=(5,0),pady=2)

    #Creating date entry
    global date
    date = ttk.Entry(frame, width=25)
    date.focus()
    date.grid(column=1, row=1,padx=(5,0),pady=2)

    #Creating the duration entry
    global entry_subnet
    entry_subnet = ttk.Entry(frame, width=25)
    entry_subnet.focus()
    entry_subnet.grid(column=1, row=2,padx=(5,0),pady=2)

    #Creating the submit button
    Button(frame,text="Submit",anchor="center").grid(column=0,row=4,columnspan=2,padx=15)


    return frame

#Creates the main window for the application
def create_main_window():
    # root window
    root = Tk()
    root.title('Data Entry')
    root.geometry('250x250')
    root.resizable(0, 0)

    #Create the input frame
    input_frame = create_input_frame(root)
    input_frame.grid(row=0,column=0,pady=0,padx=5,sticky=W)

    root.mainloop()

create_main_window()
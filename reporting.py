# This program will be used in the future for process that need to run continuously

import visualization
from user_input import *
from pull_entry import *
from visualization import *
from otherFunctions import *
import pdb
import datetime
from datetime import datetime
import sqlite3
import pandas as pd
import sqlalchemy
from fpdf import FPDF

# Create connection to SQL and an engine for SQLalchemy
connection = sqlite3.connect("D:\\Libraries\\Desktop\\Python\\Projects\\Self_Improvement_Data\\Data\\PersonalData.db")
cursor = connection.cursor()
engine = sqlalchemy.create_engine('sqlite:///D:\Libraries\Desktop\Python\Projects\Self_Improvement_Data\Data/PersonalData.db').connect()

# Create a temporary dataframe to manipulate data from SQL database
df = pd.read_sql_table('PersonalData', engine, index_col=1)

# Get todays date and the week mask, this will be used in future logic
Today = datetime.today()
WeekMask = getWeekMask()

title = "Self-Improvement Weekly Report"

# Standard A4 Page Size
PageWidth = 210
PageHeight = 297

CurrentWeek = getCurrentWeek()
WeekStart = CurrentWeek.iloc[0]['WeekStart']
print(datetime.strftime(WeekStart,'%m/%d/%y'))


class PDF(FPDF):
    def header(self):
        # Logo
        self.image('Images/Icon.png', 10, 8, 33)

        self.set_font('Arial','B',20)
        w = self.get_string_width(title) + 6
        self.set_y(15)
        self.set_x(((210-w)/2)+5)
        self.set_draw_color(0,0,0)
        self.set_fill_color(255,255,255)
        self.set_text_color(0,0,0)
        self.set_line_width(1)
        self.cell(w,20,title,1,1,'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial','I',8)
        self.set_text_color(128)
        self.cell(0,10,'Page ' + str(self.page_no()),0,0,'C')

pdf = PDF()
pdf.add_page()
pdf.multi_cell(0, 10, str(printCurrentWeek()))
pdf.image('D:\Libraries\Desktop\Python\Projects\Self_Improvement_Data\Charts\PieChart_S01-01-22_E01-22-22.png',35,70, 150,150)
pdf.output('Reports/Report{}.pdf'.format("1"), 'F')
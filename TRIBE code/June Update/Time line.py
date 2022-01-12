import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from datetime import datetime
import sqlite3

import time



def get_DOB_and_names():
    names=[]
    DOBs=[]
    conn = sqlite3.connect("Family_1.db")
    cursor = conn.cursor()
    sql = """
      SELECT Firstname,Surname,DOB
      FROM tblFamily
      """
    for row in cursor.execute(sql):
        if len(row[0]) != 0 and len(row[1]) != 0 and len(row[2]) != 0:
            name = row[0] + " " + row[1] + " " + "was born "

            DOB = row[2]

            names.append(str(name))
            DOBs.append(str(DOB))


    return names,DOBs

def get_DOD_and_names():
    names=[]
    DODs=[]
    conn = sqlite3.connect("Family_1.db")
    cursor = conn.cursor()
    sql = """
      SELECT Firstname,Surname,DOD
      FROM tblFamily
      """
    for row in cursor.execute(sql):
        if len(row[0])!= 0 and len(row[1])!=0 and len(row[2])!=0:

            name= row[0] + " " + row[1] + " " + "died on"

            DOD=row[2]

            names.append(str(name))
            DODs.append(str(DOD))

    return names,DODs



def input_time_line_data():

        names=[]

        dates = []

        names_1,DOBs=get_DOB_and_names()

        names_2,DODs=get_DOD_and_names()

        if len(names_1)>0 and len(names_2)>0:
            names=  names_1 + names_2

        elif len(names_1) >0 and len(names_2)==0:
            names=names_1

        else:
            names=names_2


        dates= DOBs + DODs



        dates = [datetime.strptime(d, "%Y-%m-%d") for d in dates]


        # Choose some nice levels
        levels = np.tile([-91,91,-81,81,-71,71,-61,61,-51,51,-41,41,-31,31,-21, 21, -11, 11],
                         int(np.ceil(len(dates)/6)))[:len(dates)]



        # Create figure and plot a stem plot with the date
        fig, ax = plt.subplots(figsize=(100, 4), constrained_layout=True)
        ax.set(title="Important dates")

        markerline, stemline, baseline = ax.stem(dates, levels,
                                                 linefmt="C3-", basefmt="k-",
                                                 use_line_collection=True)

        plt.setp(markerline, mec="k", mfc="w", zorder=3)

        # Shift the markers to the baseline by replacing the y-data by zeros.
        markerline.set_ydata(np.zeros(len(dates)))

        # annotate lines
        vert = np.array(['top', 'bottom'])[(levels > 0).astype(int)]
        for d, l, r, va in zip(dates, levels, names, vert):
            ax.annotate(r, xy=(d, l), xytext=(-3, np.sign(l)*3),
                        textcoords="offset points", va=va, ha="right")

        # format xaxis with 4 month intervals
        ax.get_xaxis().set_major_locator(mdates.MonthLocator(interval=24))
        ax.get_xaxis().set_major_formatter(mdates.DateFormatter("%b %Y"))
        plt.setp(ax.get_xticklabels(), rotation=30, ha="right")

        # remove y axis and spines
        ax.get_yaxis().set_visible(False)
        for spine in ["left", "top", "right"]:
            ax.spines[spine].set_visible(False)

        ax.margins(y=0.1)
        plt.show()



# get_DOB_and_names()


#input_time_line_data()

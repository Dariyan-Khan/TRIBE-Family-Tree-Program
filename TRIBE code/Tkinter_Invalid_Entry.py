from tkinter import *
from datetime import datetime, date

def pop_up_menu():
    menu = Tk()
    menu.wm_title("Invalid Entry")
    label =Label(menu, text="Invalid Entry", font="none 12 bold").grid(row=1,column=0)
    confirm =Button(menu, text="Ok", command=lambda:[menu_close(menu)]).grid(row=2,column=0,sticky=W)
    menu.mainloop()


def check_dob_and_dod(DOB,DOD,AllInfo):
    if DOB=="" and DOD=="":
        return AllInfo
    if DOB==-1 or DOD==-1:
        AllInfo=False
        return AllInfo
    else:
        if DOB!="":
            if DOB > date.today():
                AllInfo=False
        if DOD!="":
            if DOD > date.today():
                AllInfo=False
        if DOB!="" and DOD!="":
            if DOB>DOD:
                AllInfo=False

    return AllInfo

def menu_close(menu):
    menu.destroy()
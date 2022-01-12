import sys
import random
import datetime
import sqlite3
import os.path
from tkinter import *
import time
import re
import DatabaseAndWindowTasks as DatabaseAndWindowTasks


def display_menu():
   window = Tk()
   window.title("MAIN MENU")
   window.configure(background="Light blue")

   # Label for text saying what to do

   Label (window, text="Choose one of the options below:", bg="Light blue", fg="black", font = "none 18 bold") .grid(row=0, column=3)

   #Button for option 1

   Button(window, text="Enter new person", width=16, command=lambda:[close_window(window),option1()]) .grid(row=50, column=0, sticky=W)

   # Button for option 2

   Button(window, text="Edit an entry", width = 13, command=lambda:[close_window(window), option2()]) .grid(row=50, column=2, sticky=W)

   #Button for option 3

   Button(window, text="Delete an entry", width = 15, command=lambda:[close_window(window), option3()]) .grid(row=50, column=4, sticky=W)

   #Button for option 4

   Button(window, text="View all entries", width = 16, command=lambda:[close_window(window), option4()]) .grid(row=50, column=6, sticky=W)

   #Button for option 9

   Button(window, text="Exit", width=4, command=lambda:[close_window(window),option9()]) .grid(row=50, column=10, sticky=W)

   Button(window, text="Draw Tree", width=9, command=lambda:[close_window(window), draw_tree()]) .grid(row=50, column=8, sticky=W)

   window.mainloop()

def close_window(window):
    window.destroy()
   
   
   #return window

def option9():
    sys.exit()


def close_window3(window3):
    window3.destroy()

def change_info(person):
    DatabaseAndWindowTasks.create_and_enter_form("EDIT AN ENTRY","2",person)

def delete_person(person):
    conn = sqlite3.connect("Family_1.db")
    print(person)
    with conn:
        cursor = conn.cursor()
        print(person)
        keyfield = "'" + person + "'"
        cursor.execute("DELETE FROM tblFamily WHERE personID =" + keyfield)
        conn.commit()
        update_after_deletion(person)
        conn.commit()




def update_after_deletion(person):
    with sqlite3.connect("Family_1.db") as conn:
        cursor=conn.cursor()
        keyfield = '"' + person + '"'
        field='"' + "" + '"'
        cursor.execute("UPDATE tblFamily SET MotherID =" + field + "WHERE MotherID =" + keyfield)
        cursor.execute("UPDATE tblFamily SET FatherID=" + field + "WHERE FatherID=" + keyfield)
        conn.commit()






def choose_person(message,option_num):
      with sqlite3.connect("Family_1.db") as conn:
          cursor = conn.cursor()
          window3=Tk()
          window3.title("Amending a record")
          window3.configure(background="Light blue")
          # label for choosing row to edit
          Label(window3, text=message, bg="Light blue", fg="black", font ="none 12 bold") .grid(row=0,column=0, sticky=W)
          tkvar_edit= StringVar(window3)
          choices_edit=[]
          for row in cursor.execute("SELECT * FROM  tblFamily WHERE PersonID NOT LIKE '%Mother%' AND PersonID NOT LIKE '%Father%' AND PersonID NOT LIKE '%_P%' "):
             choices_edit.append(row)
          tkvar_edit.set('-')
          popup_menu_edit=OptionMenu(window3, tkvar_edit, *choices_edit)
          popup_menu_edit.grid(row=0, column=1, sticky=W)
          if option_num=="2":
              person=tkvar_edit.get()[2:8]
              Button(window3, text="Submit", width=6, command=lambda:[close_window3(window3), change_info(tkvar_edit.get()[2:8])]) .grid(row=3, column=0, sticky=W)
          elif option_num=="3":
              person=tkvar_edit.get()[2:8]
              Button(window3, text="Submit", width=6, command=lambda:[close_window3(window3), delete_person(tkvar_edit.get()[2:8]),display_menu()]) .grid(row=3, column=0, sticky=W)
          Button(window3, text="Main menu", width=9, command=lambda:[close_window3(window3), display_menu()]) .grid(row=3, column=1, sticky=W)

def close_window3(window3):
    window3.destroy()

def option1():
    file_exists=DatabaseAndWindowTasks.check_file_exists()
    if file_exists==False:
        DatabaseAndWindowTasks.create_database()
    else:
        DatabaseAndWindowTasks.create_and_enter_form("ADD NEW person","1", "NONE")
        display_menu()
        

def option2():
    file_exists=DatabaseAndWindowTasks.check_file_exists()
    if file_exists==False:
        option1()
    else:
        choose_person("Choose Which person To Amend","2")
        
    


def option3():
    choose_person("Choose Which person To Delete","3")
    

def DrawTree():
    pass
    
        

display_menu()

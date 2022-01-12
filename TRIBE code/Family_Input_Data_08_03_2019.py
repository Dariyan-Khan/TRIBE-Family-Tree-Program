import sys
import random
import datetime
import sqlite3
import os.path
from tkinter import *
import time
import re
import DatabaseAndWindowTasks as DatabaseAndWindowTasks
import Mean_and_Standard_Deviation_of_ages as Stats
import Add_Mother as Add_Mother
import Add_Father as Add_Father
import Finding_Relationships as Relations
import SortingAlgorithm_09_03_2019 as Sort

def display_menu():
   window = Tk()
   window.title("MAIN MENU")
   window.configure(background="Light blue")

   # Label for text saying what to do

   Label (window, text="Choose one of the options below:", bg="Light blue", fg="black", font = "none 18 bold") .grid(row=0, column=3, sticky=W)

   #Button for option 1

   Button(window, text="Enter new person", width=16, command=lambda:[close_window(window),option1()]) .grid(row=50, column=0, sticky=W)

   # Button for option 2

   Button(window, text="Edit an entry", width = 13, command=lambda:[close_window(window), option2()]) .grid(row=50, column=2, sticky=W)

   #Button for option 3

   Button(window, text="Delete an entry", width = 15, command=lambda:[close_window(window), option3()]) .grid(row=50, column=4, sticky=W)

   #Button for option 9

   Button(window, text="Exit", width=4, command=lambda:[close_window(window),option9()]) .grid(row=50, column=14, sticky=W)

   Button(window, text="Draw Tree", width=9, command=lambda:[close_window(window), draw_tree()]) .grid(row=50, column=8, sticky=W)

   Button(window, text="Find Relationship", width=14, command=lambda:[close_window(window), get_relationship()]).grid(row=50, column=10, sticky=W)

   Button(window, text="Display Statistics", width=17, command=lambda:[close_window(window), get_statistics()]).grid(row=50, column=12, sticky=W)

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
          for row in cursor.execute("""SELECT * FROM  tblFamily WHERE PersonID NOT LIKE '%Mother%'
                                    AND PersonID NOT LIKE '%Father%'
                                    AND PersonID NOT LIKE '%_P%' """):
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
    

def draw_tree():
    pass

def get_relationship():
    conn = sqlite3.connect("Family_1.db")
    cursor = conn.cursor()
    #add_mother,add_father=DatabaseAndWindowTasks.check_parents_add()
    #if add_mother==True:
     #   Add_Mother.add_mother_main()
    #if add_father==True:
     #   Add_Father.add_father_main()
    window1=Tk()
    window1.title("Find Relationship")
    window1.configure(background="Light blue")
    Label(window1, text="Choose Two People:", bg="Light blue", fg="black", font="none 18 bold").grid(row=0, column=0,sticky=W)

    choices = []
    selected = StringVar(window1)
    selected2 = StringVar(window1)
    selected.set('-')
    for row in cursor.execute("""SELECT PersonID, Firstname, Surname, DOB, DOD, Gender FROM tblFamily"""):

        choices.append(row)
    pop_up_menu = OptionMenu(window1, selected, *choices)
    pop_up_menu.grid(row=1, column=0, sticky=W)

    pop_up_menu2 = OptionMenu(window1, selected2, *choices)
    pop_up_menu2.grid(row=1, column=1, sticky=W)

    output = Text(window1,width=140, height=1, wrap=WORD, background="white")
    output.grid(row=3, column=0, columnspan=2, sticky=W)

    Button(window1, text="Main Menu", width=9,command=lambda: [DatabaseAndWindowTasks.close_window1(window1), display_menu()]).grid(row=2, column=0,sticky=W)

    Button(window1, text="Submit", width=6,command=lambda: [find_relationship(selected,selected2,output)]).grid(row=2, column=1,sticky=W)


    window1.mainloop()

def find_relationship(selected,selected2,output):
    children_dict=Sort.det_children()
    person= selected.get()
    relative=selected2.get()
    all_person_id=DatabaseAndWindowTasks.get_person_id()
    for x in range(0,len(all_person_id)):
        if all_person_id[x][0] in person:
            person = all_person_id[x][0]

        if all_person_id[x][0] in relative:
            relative = all_person_id[x][0]

    if person==relative:
        output.delete(0.0, END)
        output.insert(END,"You chose the same person")
    person_family_id= DatabaseAndWindowTasks.get_family_id(person)
    relative_family_id=DatabaseAndWindowTasks.get_family_id(relative)
    if person_family_id == relative_family_id:
        output.delete(0.0, END)
        output.insert(END,"The 2 people are siblings")
    elif relative in children_dict[person]:
        output.delete(0.0, END)
        output.insert(END,"The person in the drop-down menu on the right is the child of the person in the drop-down menu on the left")
    elif person in children_dict[relative]:
        output.delete(0.0, END)
        output.insert(END,"The person in the drop-down menu on the left is the child of the person in the drop-down menu on the right")


    else:
        path=Relations.relations_main(person,relative)
        output.delete(0.0,END)
        output.insert(END,path)







def get_statistics():
    window1=Tk()
    window1.title("Statistics For People Who Are Currently Alive")
    window1.configure(background="Light blue")
    mode,median, mean_age,variance,standard_deviation, max_age_people,max_age_people_list,min_age_people,min_age_people_list=Stats.statistics_main()

    max_age_string=""
    for x in range(0,len(max_age_people_list)):
        personF=DatabaseAndWindowTasks.get_firstname(max_age_people_list[x])
        personS=DatabaseAndWindowTasks.get_surname(max_age_people_list[x])
        max_age_string=max_age_string + personF + " " + personS + " "
        if x!= int(len(max_age_people_list)-1):
            max_age_string = max_age_string + ","

    min_age_string = ""
    for x in range(0, len(min_age_people_list)):
        personF = DatabaseAndWindowTasks.get_firstname(min_age_people_list[x])
        personS = DatabaseAndWindowTasks.get_surname(min_age_people_list[x])
        min_age_string = min_age_string + personF + " " + personS + " "
        if x != int(len(min_age_people_list) - 1):
            min_age_string = min_age_string + ","



    Label(window1, text="Most common age is:", bg="Light blue", fg="black", font="none 18 bold").grid(row=0,column=0,sticky=W)
    Label(window1, text=mode, bg="Light blue", fg="black", font="none 18 bold").grid(row=0, column=1,sticky=W)

    Label(window1, text="The median age is:", bg="Light blue", fg="black", font="none 18 bold").grid(row=1, column=0,sticky=W)
    Label(window1, text=median, bg="Light blue", fg="black", font="none 18 bold").grid(row=1, column=1, sticky=W)

    Label(window1, text="The mean of the ages is:", bg="Light blue", fg="black", font="none 18 bold").grid(row=2, column=0,sticky=W)
    Label(window1, text=mean_age, bg="Light blue", fg="black", font="none 18 bold").grid(row=2, column=1, sticky=W)

    Label(window1, text="The variance of the ages is:", bg="Light blue", fg="black", font="none 18 bold").grid(row=3, column=0,sticky=W)
    Label(window1, text=variance, bg="Light blue", fg="black", font="none 18 bold").grid(row=3, column=1, sticky=W)

    Label(window1, text="The standard deviation of the ages is :", bg="Light blue", fg="black", font="none 18 bold").grid(row=4, column=0,sticky=W)
    Label(window1, text=standard_deviation, bg="Light blue", fg="black", font="none 18 bold").grid(row=4, column=1, sticky=W)

    Label(window1, text="The oldest people currently living are ", bg="Light blue", fg="black", font="none 18 bold").grid(row=5, column=0,sticky=W)
    Label(window1, text=max_age_string, bg="Light blue", fg="black", font="none 18 bold").grid(row=5, column=1, sticky=W)
    Label(window1, text="aged", bg="Light blue", fg="black", font="none 18 bold").grid(row=5, column=2,sticky=W)
    Label(window1, text=max_age_people, bg="Light blue", fg="black", font="none 18 bold").grid(row=5, column=3, sticky=W)

    Label(window1, text="The youngest people currently living are ", bg="Light blue", fg="black",font="none 18 bold").grid(row=6, column=0, sticky=W)
    Label(window1, text=min_age_string, bg="Light blue", fg="black", font="none 18 bold").grid(row=6, column=1,sticky=W)
    Label(window1, text="aged", bg="Light blue", fg="black", font="none 18 bold").grid(row=6, column=2, sticky=W)
    Label(window1, text=min_age_people, bg="Light blue", fg="black", font="none 18 bold").grid(row=6, column=3,sticky=W)

    Label(window1, text="The mean age is:", bg="Light blue", fg="black", font="none 18 bold").grid(row=7, column=0, sticky=W)
    Label(window1, text=mean_age, bg="Light blue", fg="black", font="none 18 bold").grid(row=7, column=1, sticky=W)

    Button(window1, text="Main Menu", width=9, command=lambda:[DatabaseAndWindowTasks.close_window1(window1), display_menu()]) .grid(row=10, column=2, sticky=W)

    window1.mainloop()

def

display_menu()

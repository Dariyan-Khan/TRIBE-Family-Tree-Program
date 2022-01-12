import sqlite3
from tkinter import *
from tkinter import Message
import DatabaseAndWindowTasks as DatabaseAndWindowTasks
import Mean_and_Standard_Deviation_of_ages as Stats
import Add_Mother as Add_Mother
import Add_Father as Add_Father
import Finding_Relationships as Relations
import SortingAlgorithm_09_03_2019 as Sort
import KivyFamilyTree as kv
import Get_All_Information as GetAllInfo
import time

def display_menu():
   window = Tk()
   window.title("MAIN MENU")
   window.configure(background="Light blue")
   # Label for text saying what to do

   m=Label (window, text="Choose one of the options below:", bg="Light blue", fg="black", font = "none 18 bold").grid(row=0, column=3, sticky=W)
   m.grid(expand=True, fill='x')
   m.bind("<Configure>", lambda e: m.configure(width=e.width-10))
   # #Label (window, text="Choose one of the options below:", bg="Light blue", fg="black", font = "none 18 bold") .grid(row=0, column=3, sticky=W)
   #
   # #Button for Enter New Person
   #
   # Button(window, text="Enter new person", width=16, command=lambda:[close_window(window),enter_new_person()]) .grid(row=50, column=0, sticky=W)
   #
   # # Button for Edit entry
   #
   # Button(window, text="Edit an entry", width = 13, command=lambda:[close_window(window), edit_person()]) .grid(row=50, column=2, sticky=W)
   #
   # #Button for Delete entry
   #
   # Button(window, text="Delete an entry", width = 15, command=lambda:[close_window(window), choose_person_delete()]) .grid(row=50, column=4, sticky=W)
   #
   # #Button for Exit
   #
   # Button(window, text="Exit", width=4, command=lambda:[close_window(window),option9()]) .grid(row=50, column=14, sticky=W)
   #
   # #Button for draw tree
   #
   # Button(window, text="Draw Tree", width=9, command=lambda:[close_window(window), draw_tree()]) .grid(row=50, column=8, sticky=W)
   #
   # #Button for get relationship
   #
   # Button(window, text="Find Relationship", width=14, command=lambda:[close_window(window), get_relationship()]).grid(row=50, column=10, sticky=W)
   #
   # #Button for statistics
   #
   # Button(window, text="Display Statistics", width=17, command=lambda:[close_window(window), get_statistics()]).grid(row=50, column=12, sticky=W)

   window.mainloop()

def close_window(window):
    window.destroy()
   
   
   #return window

def option9():
    exit()
#=================Enters person into database===================================
def enter_new_person():
    file_exists=DatabaseAndWindowTasks.check_file_exists()
    if file_exists==False:
        DatabaseAndWindowTasks.create_database() ### Checks to see if database exists, beofre trying to enter info into it
    DatabaseAndWindowTasks.create_and_enter_form("ADD NEW person","1", "NONE")
    display_menu()

#=================Edit and delete person options=====================================================================================

def edit_person():
    file_exists = DatabaseAndWindowTasks.check_file_exists()
    if file_exists == False:
        enter_new_person()
    else:
        choose_person("Choose Which person To Amend", "2")



def choose_person_delete():
    file_exists = DatabaseAndWindowTasks.check_file_exists()
    if file_exists == False:
        enter_new_person()
    else:
        choose_person("Choose Which person To Delete", "3")

def close_window3(window3):
    window3.destroy()

def change_info(person):
    DatabaseAndWindowTasks.create_and_enter_form("EDIT AN ENTRY","2",person)
    display_menu()

def delete_person(person):
    conn = sqlite3.connect("Family_1.db")
    with conn:
        cursor = conn.cursor()
        print(person)
        keyfield = "'" + person + "'"
        cursor.execute("DELETE FROM tblFamily WHERE personID =" + keyfield)
        conn.commit()
        update_after_deletion(person)
        conn.commit()




def update_after_deletion(person): # Account for  where person was a mother or a father
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
          choices_edit=[]
          for row in cursor.execute("""SELECT * FROM  tblFamily WHERE PersonID NOT LIKE '%Mother%'
                                    AND PersonID NOT LIKE '%Father%'
                                    AND PersonID NOT LIKE '%_P%' """):         ### Gets everyone in the database apart from a select few for the choices
             choices_edit.append(row)
          if len(choices_edit)==0:
              enter_new_person()
          else:
            window3 = Tk()
            window3.title(message)
            window3.configure(background="Light blue")
            Label(window3, text=message, bg="Light blue", fg="black", font="none 12 bold").grid(row=0, column=0,sticky=W)
            tkvar_edit = StringVar(window3)
            tkvar_edit.set('-')
            popup_menu_edit=OptionMenu(window3, tkvar_edit, *choices_edit)
            popup_menu_edit.grid(row=0, column=1, sticky=W)

          if option_num=="2":    #### Edit person
              Button(window3, text="Submit", width=6, command=lambda:[close_window3(window3), change_info(tkvar_edit.get()[2:8])]) .grid(row=3, column=0, sticky=W)

          elif option_num=="3": # Delete person
              Button(window3, text="Submit", width=6, command=lambda:[close_window3(window3), delete_person(tkvar_edit.get()[2:8]),display_menu()]) .grid(row=3, column=0, sticky=W)
          Button(window3, text="Main menu", width=9, command=lambda:[close_window3(window3), display_menu()]) .grid(row=3, column=1, sticky=W)

def close_window3(window3):
    window3.destroy()
#==========================================================================================================================================================================================

def draw_tree():
    file_exists = DatabaseAndWindowTasks.check_file_exists()
    if file_exists == False:
        enter_new_person()
    else:
        Add_Mother.add_mother_main()
        Add_Father.add_father_main()
        entire_families, family_matrix, children_dict, kivy_matrix=Sort.sorting_main()
        print(family_matrix)
        #time.sleep(10)
        everything_connected_dict=GetAllInfo.get_everything_connected()
        ft = kv.StartFamilyTreeApp()
        ft.fids1 = entire_families
        ft.fids2 = everything_connected_dict
        ft.fids3 = kivy_matrix
        ft.run()
        display_menu()





def get_relationship():
    file_exists = DatabaseAndWindowTasks.check_file_exists()
    if file_exists == False:
        enter_new_person()
    else:
        conn = sqlite3.connect("Family_1.db")
        cursor = conn.cursor()
        #Add_Mother.add_mother_main()
        #Add_Father.add_father_main()
        window1=Tk()
        window1.title("Find Relationship")
        window1.configure(background="Light blue")
        Label(window1, text="Choose Two People:", bg="Light blue", fg="black", font="none 18 bold").grid(row=0, column=0,sticky=W)

        choices = []
        selected = StringVar(window1)
        selected2 = StringVar(window1)
        selected.set('-')
        for row in cursor.execute("""SELECT PersonID, Firstname, Surname, DOB, DOD, Gender FROM tblFamily WHERE PersonID NOT LIKE '%Mother%' and PersonID NOT LIKE '%Father%'
                                  AND PersonID NOT LIKE '%_P%' """): # Gets choices for drop-down menu

            choices.append(row)
        pop_up_menu = OptionMenu(window1, selected, *choices)
        pop_up_menu.grid(row=1, column=0, sticky=W)

        pop_up_menu2 = OptionMenu(window1, selected2, *choices)
        pop_up_menu2.grid(row=1, column=1, sticky=W)

        output = Text(window1,width=140, height=1, wrap=WORD, background="white") # Gets output box
        output.grid(row=3, column=0, columnspan=2, sticky=W)

        Button(window1, text="Main Menu", width=9,command=lambda: [DatabaseAndWindowTasks.close_window1(window1), display_menu()]).grid(row=2, column=0,sticky=W)

        Button(window1, text="Submit", width=6,command=lambda: [find_relationship(selected,selected2,output)]).grid(row=2, column=1,sticky=W)


        window1.mainloop()

def find_relationship(selected,selected2,output):
        entire_families, family_matrix, children_dict, kivy_matrix = Sort.sorting_main()
        person= selected.get()
        relative=selected2.get()
        all_person_id=DatabaseAndWindowTasks.get_person_id()

        for x in range(0,len(all_person_id)):
            if all_person_id[x][0] in person: # Gets personID of person from drop-down menu selection
                person = all_person_id[x][0]

            if all_person_id[x][0] in relative: #Gets personID for relative from drop-down menu selection
                relative = all_person_id[x][0]

        if person==relative:
            output.delete(0.0, END)
            output.insert(END,"You chose the same person")

        try:
            person_family_id= DatabaseAndWindowTasks.get_family_id(person)
            relative_family_id=DatabaseAndWindowTasks.get_family_id(relative)   # Checks to see if user chose the same person
        except Exception:
            output.delete(0.0,END)
            output.insert(END, "There is no connection between the 2 entered people")
        if (person_family_id == relative_family_id) and (person!=relative):
            output.delete(0.0, END)
            output.insert(END,"The two people are siblings")    # Checks if the 2 people are in the same family i.e. siblings.

        ## Checks if one is the parent of the other

        elif relative in children_dict[person]:
            person_firstname=DatabaseAndWindowTasks.get_firstname(person)
            person_surname=DatabaseAndWindowTasks.get_surname(person)

            relative_firstname=DatabaseAndWindowTasks.get_firstname(relative)
            relative_surname=DatabaseAndWindowTasks.get_surname(relative)
            relative_gender=DatabaseAndWindowTasks.get_gender(relative)
            if relative_gender=="Male":
                child="Son"
            else:
                child="Daughter"

            output.delete(0.0, END)
            output.insert(END,relative_firstname + " " + relative_surname + " " + " is the" + " " + child + " " + "of" + " " + person_firstname + " " + person_surname)

        elif person in children_dict[relative]:
            person_firstname=DatabaseAndWindowTasks.get_firstname(person)
            person_surname=DatabaseAndWindowTasks.get_surname(person)

            relative_firstname=DatabaseAndWindowTasks.get_firstname(relative)
            relative_surname=DatabaseAndWindowTasks.get_surname(relative)
            person_gender=DatabaseAndWindowTasks.get_gender(person)
            if person_gender=="Male":
                child="Son"
            else:
                child="Daughter"
            output.delete(0.0, END)
            output.insert(END,person_firstname + " "  + person_surname + " " + "is the" + " " + child + " " + "of" + " " + relative_firstname + " " + relative_surname)


        else:
            try:
                path=Relations.relations_main(person,relative,entire_families,family_matrix)
                output.delete(0.0,END)
                output.insert(END,path)
            except Exception:
                output.delete(0.0,END)
                output.insert(END,"There is no connection between the 2 entered people")


def get_statistics():
    file_exists = DatabaseAndWindowTasks.check_file_exists()
    if file_exists == False:
        enter_new_person()
    else:

        window1=Tk()
        window1.title("Statistics For People Who Are Currently Alive")
        window1.configure(background="Light blue")
        try:
            mode_age,median_age, mean_age,variance,standard_deviation, max_age_people,max_age_people_list,min_age_people,min_age_people_list=Stats.statistics_main()
        except Exception:
            mode_age, median_age, mean_age, variance, standard_deviation, max_age_people, max_age_people_list, min_age_people, min_age_people_list = Stats.statistics_main_1_person()

        max_age_string=""
        for x in range(0,len(max_age_people_list)):
            personF=DatabaseAndWindowTasks.get_firstname(max_age_people_list[x])
            personS=DatabaseAndWindowTasks.get_surname(max_age_people_list[x])
            max_age_string=max_age_string + personF + " " + personS + " "
            if x!= int(len(max_age_people_list)-1):
                max_age_string = max_age_string + ","    # Gets sentence for max_age

        min_age_string = ""
        for x in range(0, len(min_age_people_list)):
            personF = DatabaseAndWindowTasks.get_firstname(min_age_people_list[x])
            personS = DatabaseAndWindowTasks.get_surname(min_age_people_list[x])
            min_age_string = min_age_string + personF + " " + personS + " "
            if x != int(len(min_age_people_list) - 1):
                min_age_string = min_age_string + ","  ### gets sentence for min_age


        #mode_age
        Label(window1, text="Most common age is:", bg="Light blue", fg="black", font="none 18 bold").grid(row=0,column=0,sticky=W)
        Label(window1, text=mode_age, bg="Light blue", fg="black", font="none 18 bold").grid(row=0, column=1,sticky=W)

        #median_age
        Label(window1, text="The median age is:", bg="Light blue", fg="black", font="none 18 bold").grid(row=1, column=0,sticky=W)
        Label(window1, text=median_age, bg="Light blue", fg="black", font="none 18 bold").grid(row=1, column=1, sticky=W)

        #mean
        Label(window1, text="The mean of the ages is:", bg="Light blue", fg="black", font="none 18 bold").grid(row=2, column=0,sticky=W)
        Label(window1, text=mean_age, bg="Light blue", fg="black", font="none 18 bold").grid(row=2, column=1, sticky=W)

        #variance
        Label(window1, text="The variance of the ages is:", bg="Light blue", fg="black", font="none 18 bold").grid(row=3, column=0,sticky=W)
        Label(window1, text=variance, bg="Light blue", fg="black", font="none 18 bold").grid(row=3, column=1, sticky=W)

        #standard deviation
        Label(window1, text="The standard deviation of the ages is :", bg="Light blue", fg="black", font="none 18 bold").grid(row=4, column=0,sticky=W)
        Label(window1, text=standard_deviation, bg="Light blue", fg="black", font="none 18 bold").grid(row=4, column=1, sticky=W)

        #max_age
        Label(window1, text="The oldest people currently living are ", bg="Light blue", fg="black", font="none 18 bold").grid(row=5, column=0,sticky=W)
        Label(window1, text=max_age_string, bg="Light blue", fg="black", font="none 18 bold").grid(row=5, column=1, sticky=W)
        Label(window1, text="aged", bg="Light blue", fg="black", font="none 18 bold").grid(row=5, column=2,sticky=W)
        Label(window1, text=max_age_people, bg="Light blue", fg="black", font="none 18 bold").grid(row=5, column=3, sticky=W)

        #min age
        Label(window1, text="The youngest people currently living are ", bg="Light blue", fg="black",font="none 18 bold").grid(row=6, column=0, sticky=W)
        Label(window1, text=min_age_string, bg="Light blue", fg="black", font="none 18 bold").grid(row=6, column=1,sticky=W)
        Label(window1, text="aged", bg="Light blue", fg="black", font="none 18 bold").grid(row=6, column=2, sticky=W)
        Label(window1, text=min_age_people, bg="Light blue", fg="black", font="none 18 bold").grid(row=6, column=3,sticky=W)


        Button(window1, text="Main Menu", width=9, command=lambda:[DatabaseAndWindowTasks.close_window1(window1), display_menu()]) .grid(row=10, column=2, sticky=W)

        window1.mainloop()

# displays menu
display_menu()

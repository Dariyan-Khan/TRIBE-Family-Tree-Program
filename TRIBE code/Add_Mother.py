from tkinter import *
import sqlite3


def close_window1(window1):
    window1.destroy()

def extract_id(person):
    person=person.strip()
    if "_P" in person:
        new_parent_id=person[2:10]
    elif "Mother" in person:
        return person
    else:
        new_parent_id=person[2:8]
    return new_parent_id

def get_mother_id(new_mother):
    print(new_mother[0])
    count=0
    x=0
    while count!=2:
        letter=new_mother[x]
        if letter=="-":
            count+=1
        x=x+1
    MotherID=new_mother[2:x+2]
    return MotherID











def submit_mother(complete_no_mother):
    conn = sqlite3.connect("Family_1.db")
    cursor = conn.cursor()
    print(complete_no_mother)
    for x in range(0, len(complete_no_mother)):
        new_mother = complete_no_mother[x][2].get()
        if new_mother=="-":
            MotherID=""
        elif "Father" in new_mother or "Mother" in new_mother:
            if new_mother[2]=="":
                new_mother=new_mother[0:1] + new_mother[3:len(new_mother)]
            MotherID=get_mother_id(new_mother)



        else:
            MotherID = extract_id(new_mother)

        current_person_id = complete_no_mother[x][0]
        MotherID= "'" + MotherID + "'"
        current_person_id= "'" + current_person_id + "'"
        cursor.execute("UPDATE tblFamily SET MotherID =" + MotherID + "WHERE PersonID=" + current_person_id)
        conn.commit()
    conn.close()



def get_no_mother():
   complete_no_mother=[]
   no_mother_list=[]
   conn=sqlite3.connect("Family_1.db")
   cursor=conn.cursor()
   for row in cursor.execute("SELECT PersonID,Firstname,Surname FROM tblFamily WHERE (PersonID NOT LIKE '%Mother%' AND PersonID NOT LIKE '%Father%' AND PersonID NOT LIKE '%_P%') AND MotherID = '""' "):
        no_mother_list.append(row)
   if len(no_mother_list)==0:
       return complete_no_mother
   else:
       window1 = Tk()
       window1.configure(background="Light Blue")
       for x in range(0,len(no_mother_list)):
           selected=create_no_mother_dropdown(window1,x)
           no_mother=[no_mother_list[x][0], no_mother_list[x][1] + " " + no_mother_list[x][2], selected]
           complete_no_mother.append(no_mother)
           Label(window1, text="Choose a mother from the database for:", bg="Light blue", fg="black", font="none 18 bold").grid(row=x, column=0,sticky=W)
           Label(window1, text=no_mother_list[x][1] + " " + no_mother_list[x][2], bg="Light blue",fg="black", font="none 18 bold").grid(row=x, column=1,sticky=W)
           Button(window1, text="Submit", width=6, command=lambda:[submit_mother(complete_no_mother),close_window1(window1)]) .grid(row=x+1, column=2, sticky=W)
       window1.mainloop()
   return complete_no_mother



def create_no_mother_dropdown(window1,x):
    conn=sqlite3.connect("Family_1.db")
    cursor=conn.cursor()
    choices=[]
    selected = StringVar(window1)
    selected.set('-')
    for row in cursor.execute("SELECT * FROM tblFamily WHERE Gender= 'Female' AND Firstname <> '""' "):
        choices.append(row)
    for row2 in cursor.execute("SELECT MotherID FROM tblFamily WHERE MotherID LIKE '%Mother%' "):
        choices.append(row2)
    pop_up_menu = OptionMenu(window1, selected, *choices)
    pop_up_menu.grid(row=x, column=2, sticky=W)
    conn.commit()
    conn.close()
    return selected

def add_mother_main():
    complete_no_mother=get_no_mother()








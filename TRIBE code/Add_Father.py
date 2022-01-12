from tkinter import *
import sqlite3


def close_window1(window1):
    window1.destroy()

def extract_id(person):
    person=person.strip()
    if "_P" in person:
        new_parent_id=person[2:10]
    else:
        new_parent_id=person[2:8]
    return new_parent_id

def get_father_id(new_father):
    print(new_father[0])
    count=0
    x=0
    while count!=2:
        letter=new_father[x]
        if letter=="-":
            count+=1
        x=x+1
    FatherID=new_father[2:x+2]
    return FatherID











def submit_father(complete_no_father):
    conn = sqlite3.connect("Family_1.db")
    cursor = conn.cursor()
    print(complete_no_father)
    for x in range(0, len(complete_no_father)):
        new_father = complete_no_father[x][2].get()
        if new_father=="-":
            FatherID=""
        elif "Father" in new_father or "Mother" in new_father:
            if new_father[2]=="":
                new_father=new_father[0:1] + new_father[3:len(new_father)]
            FatherID=get_father_id(new_father)



        else:
            FatherID = extract_id(new_father)

        current_person_id = complete_no_father[x][0]
        FatherID= "'" + FatherID + "'"
        current_person_id= "'" + current_person_id + "'"
        cursor.execute("UPDATE tblFamily SET FatherID =" + FatherID + "WHERE PersonID=" + current_person_id)
        conn.commit()
    conn.close()



def get_no_father():
   no_father_list=[]
   complete_no_father=[]
   conn=sqlite3.connect("Family_1.db")
   cursor=conn.cursor()
   for row in cursor.execute("SELECT PersonID,Firstname,Surname FROM tblFamily WHERE (PersonID NOT LIKE '%Father%' AND PersonID NOT LIKE '%Mother%' AND PersonID NOT LIKE '%_P%') AND FatherID= '""' "):
        no_father_list.append(row)
   if len(no_father_list)==0:
       return complete_no_father
   else:
       window1 = Tk()
       window1.configure(background="Light Blue")
       for x in range(0,len(no_father_list)):
           selected=create_no_father_dropdown(window1,x)
           no_father=[no_father_list[x][0], no_father_list[x][1] + " " + no_father_list[x][2], selected]
           complete_no_father.append(no_father)
           Label(window1, text="Choose a father from the database for:", bg="Light blue", fg="black", font="none 18 bold").grid(row=x, column=0,sticky=W)
           Label(window1, text=no_father_list[x][1] + " " + no_father_list[x][2], bg="Light blue",fg="black", font="none 18 bold").grid(row=x, column=1,sticky=W)
       Button(window1, text="Submit", width=6, command=lambda:[submit_father(complete_no_father),close_window1(window1)]) .grid(row=x+1, column=2, sticky=W)
       window1.mainloop()
   return complete_no_father



def create_no_father_dropdown(window1,x):
    conn=sqlite3.connect("Family_1.db")
    cursor=conn.cursor()
    choices=[]
    selected = StringVar(window1)
    selected.set('-')
    for row in cursor.execute("""SELECT * FROM tblFamily WHERE Gender="Male" """):
        choices.append(row)
    pop_up_menu = OptionMenu(window1, selected, *choices)
    pop_up_menu.grid(row=x, column=2, sticky=W)
    conn.commit()
    conn.close()
    return selected

def add_father_main():
    complete_no_father=get_no_father()







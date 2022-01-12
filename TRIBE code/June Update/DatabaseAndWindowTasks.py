import random
import datetime
import sqlite3
import os.path
from tkinter import *
import re
import Tkinter_Invalid_Entry as CheckInvalid
import copy


   
#========================Database and file operations=============================================================================================================
def check_file_exists():
    file_exists = os.path.exists('Family_1.db')
    return file_exists

def check_parents_add():  #Gets all mothers anf fathers in the database and puts them into separate lists, and determines whether there any parents not added
    add_mother=False
    add_father=False
    all_mother=[]
    all_father=[]
    all_parents=[]
    conn=sqlite3.connect("Family_1.db")
    cursor=conn.cursor()
    for row in cursor.execute("SELECT MotherID, FatherID FROM tblFamily"):
        all_parents.append(row)
    for x in range(0,len(all_parents)):
        if all_parents[x][0]!="":
            all_mother.append(all_parents[x][0])
        if all_parents[x][1]!="":
            all_father.append(all_parents[x][1])
    if len(all_parents)!=len(all_mother):
        add_mother=True
    if len(all_parents)!=len(all_mother):
        add_father=True

    return add_mother, add_father



def create_database():
    file_exists = check_file_exists()
    if file_exists == True:
        pass
    else:
        connection = sqlite3.connect("Family_1.db")
        cursor = connection.cursor()
        sql_command = """

        CREATE TABLE `tblFamily`
        (
            `PersonID`	TEXT,
            `Firstname`	TEXT,
            `Surname`	TEXT,
            `DOB`	DATE,
            `DOD`	DATE,
            `POB`	TEXT,
            'Gender'    TEXT,
            'MotherID'          TEXT,
            'FatherID'          TEXT,
            PRIMARY KEY(`PersonID`)
        )"""

        cursor.execute(sql_command)
        connection.commit()
        connection.close()

def create_bio_table():
    connection = sqlite3.connect("Family_1.db")
    cursor = connection.cursor()
    sql_command = """

            CREATE TABLE `tblBio`
            (
                `PersonID`	TEXT,
                'Bio'       TEXT,
                PRIMARY KEY(`PersonID`)
            )"""

    cursor.execute(sql_command)
    connection.commit()
    connection.close()


#=========================Get information about people==========================================================================================================================

def get_bio(person):
    conn = sqlite3.connect("Family_1.db")
    cursor = conn.cursor()
    sql=("""
    
        SELECT Bio
        FROM tblBio
        WHERE PersonID = ?
      """)
    for row in cursor.execute(sql, (person,)):
        bio = (row[0])

    conn.commit()
    conn.close()
    try:
        return bio
    except Exception:
        return None

def get_all_info_apart_from_unknowns():
    conn = sqlite3.connect("Family_1.db")
    cursor = conn.cursor()
    cursor.execute("""
    
        SELECT *
        FROM tblFamily
        WHERE PersonID NOT LIKE "%Mother of%"
        AND PersonID NOT LIKE "%Father of%"
        AND PersonID NOT LIKE "%_P%"
        """)
    data=cursor.fetchall()
    return data





def get_firstname(person):
    conn = sqlite3.connect("Family_1.db")
    cursor = conn.cursor()
    sql = """
          SELECT Firstname
          FROM tblFamily
          Where PersonID = ?
          """
    for row in cursor.execute(sql, (person,)):
        pre_firstname = (row[0])

    conn.commit()
    conn.close()
    return pre_firstname

def get_surname(person):
    conn = sqlite3.connect("Family_1.db")
    cursor = conn.cursor()
    sql = """
      SELECT Surname
      FROM tblFamily
      Where PersonID = ?
      """
    for row in cursor.execute(sql, (person,)):
        pre_surname = (row[0])

    conn.commit()
    conn.close()
    return pre_surname

def get_dob(person):
    conn = sqlite3.connect("Family_1.db")
    cursor = conn.cursor()
    sql = """
      SELECT DOB
      FROM tblFamily
      Where PersonID = ?
      """
    for row in cursor.execute(sql, (person,)):
        pre_dob = (row[0])
        pre_dob_dd = pre_dob[8:10]
        pre_dob_mm = pre_dob[5:7]
        pre_dob_yyyy = pre_dob[0:4]

    conn.commit()
    conn.close()

    return pre_dob_dd, pre_dob_mm, pre_dob_yyyy

def get_dod(person):
    conn = sqlite3.connect("Family_1.db")
    cursor = conn.cursor()
    sql = """
      SELECT DOD
      FROM tblFamily
      Where PersonID = ?
      """
    for row in cursor.execute(sql, (person,)):
        pre_dod = (row[0])
        pre_dod_dd = pre_dod[8:10]
        pre_dod_mm = pre_dod[5:7]
        pre_dod_yyyy = pre_dod[0:4]

    conn.commit()
    conn.close()
    return pre_dod_dd, pre_dod_mm, pre_dod_yyyy

def get_pob(person):
    conn = sqlite3.connect("Family_1.db")
    cursor = conn.cursor()
    sql = """
      SELECT POB
      FROM tblFamily
      Where PersonID = ?
      """
    for row in cursor.execute(sql, (person,)):
        pre_pob = (row[0])

    conn.commit()
    conn.close()
    return pre_pob

def get_gender(person):
    conn = sqlite3.connect("Family_1.db")
    cursor = conn.cursor()
    sql = """
      SELECT Gender
      FROM tblFamily
      Where PersonID = ?
      """
    for row in cursor.execute(sql, (person,)):
        pre_gender = (row[0])

    conn.commit()
    conn.close()
    return pre_gender

def get_mother(person):
    conn = sqlite3.connect("Family_1.db")
    cursor = conn.cursor()
    sql = """
      SELECT MotherID
      FROM tblFamily
      Where PersonID = ?
      """
    for row in cursor.execute(sql, (person,)):
        need_change_m = False
        pre_mother = (row[0])
        if pre_mother == "":
            is_mother = False
            return is_mother, pre_mother, need_change_m

        else:
            is_mother = True
            sql = """
             SELECT *
             FROM tblFamily
             WHERE PersonID = ?
             """
            for row in cursor.execute(sql, (pre_mother,)):
                pre_mother = row
                print(pre_mother)

            ValidM = re.match("[M]{1}[o]{1}[t]{1}[h]{1}[e]{1}[r]", pre_mother[0])
            if ValidM:
                need_change_m = True
                return is_mother, pre_mother, need_change_m
            else:
                print(pre_mother)
                return is_mother, pre_mother, need_change_m

def get_father(person):
    conn = sqlite3.connect("Family_1.db")
    cursor = conn.cursor()
    sql = """
      SELECT FatherID
      FROM tblFamily
      Where PersonID = ?
      """
    for row in cursor.execute(sql, (person,)):
        pre_father1 = (row[0])
        print(pre_father1)
        need_change_f = False
        if pre_father1 == "":
            is_father = False
            pre_father = ""
            return is_father, pre_father, need_change_f

        else:
            is_father = True
            sql = """
             SELECT *
             FROM tblFamily
             WHERE PersonID = ?
             """
            for row in cursor.execute(sql, (pre_father1,)):
                pre_father = row
            valid_f = re.match("[F]{1}[a]{1}[t]{1}[h]{1}[e]{1}[r]", pre_father[0])
            if valid_f:
                need_change_f = True
                return is_father, pre_father, need_change_f
            else:

                return is_father, pre_father, need_change_f

def get_family_id(person):
    conn=sqlite3.connect("Family_1.db")
    cursor = conn.cursor()
    sql = """
        SELECT FamilyID
        FROM tblChildren
        WHERE PersonID = ?
        """
    for row in cursor.execute(sql, (person,)):
        family_id= row
    return family_id

def get_person_id():
    all_person_id=[]
    conn=sqlite3.connect("Family_1.db")
    cursor=conn.cursor()
    for row in cursor.execute("SELECT PersonID from tblFamily"):
        all_person_id.append(row)
    print(all_person_id)
    return all_person_id

def create_random_id(Firstname, Surname):
    prev_random_digit = []  # NEED TO MAKE SURE ANOTHER RANDOM DIGIT THAT IS SAME IS CREATED
    valid_ran_digit = False
    count = 0
    first_letter = Firstname[0]
    second_letter = Surname[0]
    while valid_ran_digit == False:
        random_digit = str(random.randint(1000, 9999))
        for x in range(0, len(prev_random_digit)):
            if int(prev_random_digit[x]) == int(random_digit):
                count = count + 1
            else:
                pass
        if count == 0:
            valid_ran_digit = True
            prev_random_digit.append(random_digit)
        else:
            valid_ran_digit = False

    PersonID = str(first_letter + second_letter + random_digit)
    return PersonID
#===============================================================================================

def check_unknown_mother(Mother, Firstname, Surname, DOB): #Checks if mother is 'Unknown and if its, reutrns the respective ID.
    if Mother == "UNKNOWN":
        MotherID = "Mother of " + Firstname + " " + Surname + " " + "born on" + " " + " " + str(DOB)
    else:
        ValidM = re.match("[M]{1}[o]{1}[t]{1}[h]{1}[e]{1}[r]{1}", Mother[2:8]) # Regular Expressions (RE) check if Mother in ID. If it is, then formatting is needed
        if ValidM:                                                              # To generate MotherID
            MotherID=copy.deepcopy(Mother[2:len(Mother)-3])
        else:
            MotherID = str((Mother[2:8]))
    return MotherID

def check_unknown_father(Father, Firstname, Surname, DOB): # Same process as above but with Fathers
    if Father == "UNKNOWN":
        FatherID = "Father of " + Firstname + " " + Surname + " " + "born on" + " " + " " + str(DOB)
    else:
        valid_f = re.match("[F]{1}[a]{1}[t]{1}[h]{1}[e]{1}[r]{1}", Father[2:8])
        if valid_f:
            FatherID = copy.deepcopy(Father[2:len(Father) - 3])
        else:
            FatherID = str((Father[2:8]))
    return FatherID

def separate_out_unknown_ID(ID):
    for x in range(0,len(ID)):

        Portion=ID[:x+1]
        try:
            Section=int((ID[x-9:x-5]+ID[x-4:x-2]+ID[x-1:x+1]))
            return Portion
        except Exception:
            Section=-1
        print(Section)


#=======================================================Tkinter GUI Code======================================================================================================

def close_window(window):
    window.destroy()

def close_window1(window1):
    window1.destroy()



def clear_info(textentry_fi,textentry_su,textentry_birth_dd,textentry_birth_mm,textentry_birth_yyyy,textentry_death_dd,textentry_death_mm,textentry_death_yyyy,
               textentry_pob,tkvar,tkvar_m,tkvar_f): #CLears information from text entries
        textentry_fi.delete(0, END)
        textentry_su.delete(0, END)
        textentry_birth_dd.delete(0, END)
        textentry_birth_mm.delete(0, END)
        textentry_birth_yyyy.delete(0, END)
        textentry_death_dd.delete(0, END)
        textentry_death_mm.delete(0, END)
        textentry_death_yyyy.delete(0, END)
        textentry_pob.delete(0, END)
        tkvar.set("Male")
        tkvar_m.set("-")
        tkvar_f.set("-")

def enter_info(person,window1,option_num,textentry_fi,textentry_su,textentry_birth_dd,textentry_birth_mm,textentry_birth_yyyy,textentry_death_dd,textentry_death_mm,
               textentry_death_yyyy,textentry_pob,tkvar,tkvar_m,tkvar_f):

        with sqlite3.connect("Family_1.db") as conn:
            cursor = conn.cursor()
        person_rec = []
        all_info=True
        #try:
        Firstname = textentry_fi.get()
        if Firstname==(None or ""):
            all_info=False

        Surname=textentry_su.get()
        if Surname==(None or ""):                        ########Exception handling, to make sure that information entered is of correect format
            all_info=False

        if all_info==True:
            PersonID = create_random_id(Firstname, Surname)

        if option_num == "2":
            PersonID = person

        if len(textentry_birth_yyyy.get())==0 and len(textentry_birth_mm.get())==0 and len(textentry_birth_dd.get())==0:
            DOB=""
        else:
            try:
                DOB = datetime.date(int(textentry_birth_yyyy.get()), int(textentry_birth_mm.get()), int(textentry_birth_dd.get()))
            except Exception:
                DOB=-1

        if len(textentry_death_yyyy.get())==0 and len(textentry_death_mm.get())==0 and len(textentry_death_dd.get())==0:
            DOD=""
        else:
            try:
                DOD = datetime.date(int(textentry_death_yyyy.get()), int(textentry_death_mm.get()), int(textentry_death_dd.get()))
            except Exception:
                    DOD=-1

        all_info=CheckInvalid.check_dob_and_dod(DOB,DOD,all_info)
        POB=textentry_pob.get()

        if POB==None:
            POB=""

        Gender = tkvar.get()
        Mother = tkvar_m.get()
        MotherID = check_unknown_mother(Mother, Firstname, Surname, DOB)
        if option_num == "2":
            is_mother, pre_mother, need_change_m = get_mother(person)

            if need_change_m == True:
                if type(pre_mother) is tuple:
                    pre_mother = pre_mother[0]

                MotherID=separate_out_unknown_ID(MotherID)
                fieldM = "'" + str(MotherID) + "'"
                #separate_out_unknown_ID(ID)
                keyfieldM = "'" + str(pre_mother) + "'"
                sql=("""UPDATE tblFamily SET MotherID = %s WHERE MotherID = %s""" % (fieldM,keyfieldM,))
                for row in cursor.execute(sql):
                    pass

        Father = tkvar_f.get()
        FatherID = check_unknown_father(Father, Firstname, Surname, DOB)
        if option_num == "2":
            is_father, pre_father, need_change_f = get_father(person)
            if need_change_f == True:
                if type(pre_father) is tuple:
                    pre_father = pre_father[0]
                FatherID = separate_out_unknown_ID(FatherID)
                field_f = "'" + FatherID + "'"
                keyfield_f = "'" + pre_father + "'"
                cursor.execute("UPDATE tblFamily SET FatherID =" + field_f + "WHERE FatherID =" + keyfield_f)

        clear_info(textentry_fi,textentry_su,textentry_birth_dd,textentry_birth_mm,textentry_birth_yyyy,textentry_death_dd,textentry_death_mm,textentry_death_yyyy,
                   textentry_pob,tkvar,tkvar_m,tkvar_f)

        if all_info==False:
            CheckInvalid.pop_up_menu()
        else:
            person_rec.append(PersonID)
            person_rec.append(Firstname)
            person_rec.append(Surname)
            person_rec.append(DOB)
            person_rec.append(DOD)
            person_rec.append(POB)
            person_rec.append(Gender)
            person_rec.append(MotherID)
            person_rec.append(FatherID)
            if option_num == "2":
                keyfield = "'" + PersonID + "'"
                cursor.execute("Delete FROM tblFamily WHERE PersonID =" + keyfield)
            cursor.execute("INSERT INTO tblFamily VALUES (?,?,?,?,?,?,?,?,?)", person_rec) ###Adds records to database
            conn.commit()
            person_rec = []
            Label2 = Label(window1, text="Record has been added", bg="Light blue", fg="black",
                           font="none 12 bold").grid(row=100, column=1)
            window1.update()
            conn.commit()
            conn.close()
            
def create_and_enter_form(title, option_num, person):
    window1 = Tk()
    window1.title(title)
    window1.configure(background="Light blue")
    window1.resizable(width=False, height=False)
    # label & text box for First name

    Label(window1, text="Enter the Firstname of the person you are entering", bg="Light blue", fg="black",
          font="none 12 bold").grid(row=1, column=0, sticky=W)
    textentry_fi = Entry(window1, width=20, bg="white")
    textentry_fi.grid(row=1, column=1, sticky=W)
    if option_num == "2":
        pre_firstname = get_firstname(person)
        textentry_fi.insert(INSERT, pre_firstname)

    # label & text box for Surname

    Label(window1, text="Enter the Surname of the person you are entering", bg="Light blue", fg="black",
          font="none 12 bold").grid(row=2, column=0, sticky=W)
    textentry_su = Entry(window1, width=20, bg="white")
    textentry_su.grid(row=2, column=1, sticky=W)
    if option_num == "2":
        pre_surname = get_surname(person)
        textentry_su.insert(INSERT, pre_surname)

    # label & text box for DOB

    Label(window1, text="DD", bg="Light blue", fg="black", font="none 9 bold").grid(row=4, column=1, sticky=W)
    textentry_birth_dd = Entry(window1, width=2, bg="white")
    textentry_birth_dd.grid(row=5, column=1, sticky=W)

    Label(window1, text="MM", bg="Light blue", fg="black", font="none 9 bold").grid(row=4, column=2, sticky=W)
    textentry_birth_mm = Entry(window1, width=2, bg="white")
    textentry_birth_mm.grid(row=5, column=2, sticky=W)

    Label(window1, text="YYYY", bg="Light blue", fg="black", font="none 9 bold").grid(row=4, column=3, sticky=W)
    textentry_birth_yyyy = Entry(window1, width=4, bg="white")
    textentry_birth_yyyy.grid(row=5, column=3, sticky=W)

    Label(window1, text="Enter the Date Of Birth of the person you are entering", bg="Light blue", fg="black",
          font="none 12 bold").grid(row=5, column=0, sticky=W)

    if option_num == "2":
        pre_dob_dd = get_dob(person)[0]
        pre_dob_mm = get_dob(person)[1]
        pre_dob_yyyy = get_dob(person)[2]
        textentry_birth_dd.insert(INSERT, pre_dob_dd)
        textentry_birth_mm.insert(INSERT, pre_dob_mm)
        textentry_birth_yyyy.insert(INSERT, pre_dob_yyyy)

    # label & text box for date of death

    Label(window1, text="DD", bg="Light blue", fg="black", font="none 9 bold").grid(row=6, column=1, sticky=W)
    textentry_death_dd = Entry(window1, width=2, bg="white")
    textentry_death_dd.grid(row=7, column=1, sticky=W)

    Label(window1, text="MM", bg="Light blue", fg="black", font="none 9 bold").grid(row=6, column=2, sticky=W)
    textentry_death_mm = Entry(window1, width=2, bg="white")
    textentry_death_mm.grid(row=7, column=2, sticky=W)

    Label(window1, text="YYYY", bg="Light blue", fg="black", font="none 9 bold").grid(row=6, column=3, sticky=W)
    textentry_death_yyyy = Entry(window1, width=4, bg="white")
    textentry_death_yyyy.grid(row=7, column=3, sticky=W)

    Label(window1,
          text="Enter the Date Of Death of the person you are entering (if the person you are entering is still alive, leave this blank)",
          bg="Light blue", fg="black", font="none 12 bold").grid(row=7, column=0, sticky=W)
    if option_num == "2":
        pre_dod_dd = get_dod(person)[0]
        pre_dod_mm = get_dod(person)[1]
        pre_dod_yyyy = get_dod(person)[2]
        textentry_death_dd.insert(INSERT, pre_dod_dd)
        textentry_death_mm.insert(INSERT, pre_dod_mm)
        textentry_death_yyyy.insert(INSERT, pre_dod_yyyy)

    # label for place of birth
    Label(window1, text="Place of Birth", bg="Light blue", fg="black", font="none 12 bold").grid(row=8, column=0,
                                                                                                 sticky=W)
    textentry_pob = Entry(window1, width=20, bg="white")
    textentry_pob.grid(row=8, column=1, sticky=W)
    if option_num == "2":
        pre_pob = get_pob(person)
        textentry_pob.insert(INSERT, pre_pob)

    # label for gender
    Label(window1, text="What gender was this person born as?", bg="Light blue", fg="black",
          font="none 12 bold").grid(row=9, column=0, sticky=W)

    tkvar = StringVar(window1)
    choices = ['Male', 'Female']
    tkvar.set('Male')

    if option_num == "2":
        pre_gender = get_gender(person)
        tkvar.set(pre_gender)
    pop_up_menu = OptionMenu(window1, tkvar, *choices)     #####Drop down menu
    pop_up_menu.grid(row=9, column=1, sticky=W)

    # label for Mother
    Label(window1, text="Select this person's mother", bg="Light blue", fg="black", font="none 12 bold").grid(
        row=10, column=0, sticky=W)

    tkvar_m = StringVar(window1)
    choices_m = ['UNKNOWN']
    tkvar_m.set('-')
    with sqlite3.connect("Family_1.db") as conn:
        cursor = conn.cursor()
        for row in cursor.execute("SELECT PersonID,Firstname,Surname,DOB FROM tblFamily WHERE tblFamily.Gender='Female' Order BY Firstname"):
            choices_m.append(row)

        for row in cursor.execute("SELECT MotherID FROM tblFamily WHERE tblFamily.MotherID LIKE '%Mother%'"):
            choices_m.append(row)

    pop_up_menu_m = OptionMenu(window1, tkvar_m, "-", *choices_m)
    pop_up_menu_m.grid(row=10, column=1, sticky=W)

    if option_num == "2":
        is_mother = get_mother(person)[0]
        if is_mother == False:
            tkvar_m.set('-')

        elif is_mother == True:
            pre_mother = get_mother(person)[1]
            tkvar_m.set(pre_mother)

        need_change_m = get_mother(person)[2]

    # label for father
    Label(window1, text="Select this person's father", bg="Light blue", fg="black", font="none 12 bold").grid(
        row=11, column=0, sticky=W)

    tkvar_f = StringVar(window1)
    choices_f = ['UNKNOWN']
    tkvar_f.set('-')

    with sqlite3.connect("Family_1.db") as conn:
        cursor = conn.cursor()

        for row in cursor.execute("SELECT PersonID,Firstname,Surname,DOB FROM tblFamily WHERE tblFamily.Gender='Male' Order BY Firstname"):
            choices_f.append(row)
        for row in cursor.execute("SELECT FatherID FROM tblFamily WHERE tblFamily.FatherID LIKE '%Father%'"):
            choices_f.append(row)

    popup_menu_f = OptionMenu(window1, tkvar_f, "-", *choices_f)
    popup_menu_f.grid(row=11, column=1, sticky=W)  #######Drop down menu

    if option_num == "2":
        is_father = get_father(person)[0]
        if is_father == False:
            tkvar_f.set('-')
        elif is_father == True:
            pre_father = get_father(person)[1]
            tkvar_f.set(pre_father)
            need_change_f = get_father(person)[2]

    # button for submit, clear data and go back to main menu
    Button(window1, text="Submit", width=6, command=lambda: [enter_info(person,window1,option_num,textentry_fi,textentry_su,textentry_birth_dd,textentry_birth_mm,textentry_birth_yyyy,textentry_death_dd,textentry_death_mm,textentry_death_yyyy,textentry_pob,tkvar,tkvar_m,tkvar_f),close_window1(window1),create_and_enter_form("ADD NEW person","1", "NONE")]).grid(row=22, column=0, sticky=W)
    Button(window1, text="Clear", width=5, command=lambda:[clear_info(textentry_fi,textentry_su,textentry_birth_dd,textentry_birth_mm,textentry_birth_yyyy,textentry_death_dd,textentry_death_mm,textentry_death_yyyy,textentry_pob,tkvar,tkvar_m,tkvar_f)]).grid(row=22, column=1, sticky=W)
    Button(window1, text="Main Menu", width=9, command=lambda: [close_window1(window1)]).grid(row=22,column=2,sticky=W)

    window1.mainloop()


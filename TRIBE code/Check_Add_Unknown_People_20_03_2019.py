import sqlite3

def check_add_1_unknown():
    people=[]
    conn=sqlite3.connect("Family_1.db")
    cursor=conn.cursor()
    for row in cursor.execute("SELECT * FROM tblFamily WHERE MotherID = '""' OR FatherID = '""' OR (MotherID LIKE '%Mother%' OR FatherID LIKE '%Father%' AND NOT (MotherID  LIKE '%Mother%' AND FatherID LIKE '%Father%')) AND (MotherID <> FatherID) "):
        people.append(row)
    if people==None or len(people)==0:
        need_add_1_people=False
    else:
        need_add_1_people=True

    return need_add_1_people

def check_add_2_people():
    people=[]
    conn=sqlite3.connect("Family_1.db")
    cursor=conn.cursor()
    for row in cursor.execute("SELECT * FROM tblFamily WHERE MotherID = '""' AND FatherID= '""' OR (MotherID LIKE '%Mother%' AND FatherID LIKE  '%Father%') "):
        people.append(row)
    if people==None or len(people)==0:
        need_add_2_people=False
    else:
        need_add_2_people=True
    return need_add_2_people

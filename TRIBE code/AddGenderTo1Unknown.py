import Getting_all_PersonID_Names_imports as AllPeopleInDatabase
import sqlite3

def get_person_gender(PersonX):
  conn= sqlite3.connect("Family_1.db")
  cursor= conn.cursor()
  print(PersonX)
  sql = """
  SELECT Gender
  FROM tblFamily
  Where PersonID = ?
  """
  for row in cursor.execute(sql,(PersonX,)):
        
        person_gender=(row[0])
        print(row[0])
  conn.commit()
  conn.close()
  return person_gender

def update_gender(person,Gender):
    conn=sqlite3.connect("Family_1.db")
    cursor=conn.cursor()
    keyfield= "'" + person + "'"
    Gender= "'" + Gender + "'"
    cursor.execute("UPDATE tblFamily SET Gender=" + Gender + " WHERE PersonID = " + keyfield)
    conn.commit()
    conn.close()

def add_gender_to_1_unknown():
    all_people=AllPeopleInDatabase.list_all()
    for x in range(0,len(all_people)):
        if "_P" in all_people[x]:
            partner_gender=get_person_gender(all_people[x][0:6])
            if partner_gender=="Male":
                Gender="Female"
            else:
                Gender="Male"
            update_gender(all_people[x],Gender)

#add_gender_to_1_unknown()
    



    

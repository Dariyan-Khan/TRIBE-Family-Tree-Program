import sqlite3
#import SortingAlgorithm_22_02_2019_Desc_num_working as Sort
import DatabaseAndWindowTasks as Family


# Put all person ID's into a list

def list_all():
    all_people=[]
    conn = sqlite3.connect("Family_1.db")
    cursor = conn.cursor()
    for row in cursor.execute('SELECT PersonID FROM tblFamily'):
        all_people.append(row[0])

    conn.commit()
    conn.close()

    return all_people


def an_under_score(person):
    under_score=False
    for x in range(0,len(person)):
        if person[x]=="_":
            under_score=True
            break
        else:
            pass
    return under_score

def person_id_against_name_dict():
    person_id_dict={}
    all_people=list_all()
    for x in range(0,len(all_people)):
               name=[]
               under_score=an_under_score(all_people[x])
               firstname= Family.get_firstname(all_people[x])
               surname = Family.get_surname(all_people[x])
               if (firstname=="" or None) and (surname=="" or None) and under_score==True:
                   PersonID=all_people[x][0:6]
                   print(PersonID)
                   firstname=Family.get_firstname(PersonID)
                   surname=Family.get_surname(PersonID)
                   name= "Partner of" + " " + str(firstname) + " " + str(surname)
               elif (firstname=="" or None) and (surname=="" or None) and under_score==False:
                   name=all_people[x]
               else:
                   name=[firstname,surname]
               person_id_dict[all_people[x]]=name
    return person_id_dict

#person_id_dict=person_id_against_name_dict()
#print(person_id_dict)



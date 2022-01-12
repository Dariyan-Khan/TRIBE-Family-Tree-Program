import sqlite3
from tkinter import *
import Getting_all_PersonID_Names_imports as AllPeopleInDatabase
import DatabaseChanges_23_02_2019 as DatabaseChanges
import copy
import AddGenderTo1Unknown as AddGenderTo1Unknown
import Change_Distance_Dictionary as ChangeDistance
import Check_Add_Unknown_People_20_03_2019 as CheckAddUnknowns





#============================== Determine children of people ===================================================================================

def det_children():
    children_dict={}
    all_people = AllPeopleInDatabase.list_all()
    all_people_length = len(all_people)
    for x in range(0, len(all_people)):
        personX=all_people[x]
        person_gender = get_person_gender(personX)
        children_set = get_children(person_gender,personX)
        children_dict[personX] = children_set

    return children_dict
    
        
#============================================== Retrieving Information From Database =============================================================        


def get_person_gender(personX):
  conn= sqlite3.connect("Family_1.db")
  cursor= conn.cursor()
  sql = """
  SELECT Gender
  FROM tblFamily
  Where PersonID = ?
  """
  for row in cursor.execute(sql,(personX,)):
        person_gender=(row[0])
  conn.commit()
  conn.close()
  return person_gender


def get_children(person_gender,personX):
    children_set=set()
    conn = sqlite3.connect("Family_1.db")
    cursor = conn.cursor()
    if person_gender == "Female":
        sql = """
        SELECT PersonID
        FROM tblFamily
        WHERE MotherID = ?
        """
        for row in cursor.execute(sql,(personX,)):
            child_id = row[0]
            child_id=person_id_format(child_id)
            children_set.add(child_id)
    elif person_gender == "Male":
        sql = """
        SELECT PersonID
        FROM tblFamily
        WHERE FatherID = ?
        """
        for row in cursor.execute(sql,(personX,)):
            child_id = row[0]
            child_id=person_id_format(child_id)
            children_set.add(child_id)
    
    children_set.discard("set()")
    return children_set

#========================================================== Create families ============================================================================================

def add_family(personX, personY, family_id_queue,all_family_id):
        GenderX = get_person_gender(personX)
        GenderY = get_person_gender(personY)
        first_family_id, family_id_queue = dequeue(family_id_queue)
        all_family_id.append(first_family_id)
        family_rec=[first_family_id]
        connection = sqlite3.connect("Family_1.db")
        cursor = connection.cursor()
        if GenderX =="Male":
            family_rec.append(personY)
            family_rec.append(personX)
        else:
            family_rec.append(personX)
            family_rec.append(personY)
        cursor.execute("INSERT INTO tblSingleFamily VALUES (?,?,?)", family_rec)
        connection.commit()
        return family_id_queue, first_family_id, all_family_id

def get_family(current_family): # Gets parents and children of a specific familyID
        connection = sqlite3.connect("Family_1.db")
        persons=[]
        parents=[]
        children=[]
        FamilyID =  "'" + current_family + "'"
        cursor=connection.cursor()
        sql = ("""
        SELECT Mother, Father, PersonID
        FROM tblSingleFamily, tblChildren
        WHERE tblSingleFamily.FamilyID = %s
        AND tblChildren.FamilyID = %s """ %  (FamilyID, FamilyID,))
        for row in cursor.execute(sql):
            Mother, Father, PersonID = row
            persons.append(row)
        parents.append(persons[0][0])
        parents.append(persons[0][1])
        for x in range(0,len(persons)):
            children.append(persons[x][2])

        return parents, children    

def families(children_dict,all_family_id):
    PeopleUsed=set()

    all_people=AllPeopleInDatabase.list_all()
    family_id_queue=initialise_family_id_queue() ########Creates queue

    exists = DatabaseChanges.check_table_exists(str("tblSingleFamily"))
    if exists == True:
        DatabaseChanges.delete_table("tblSingleFamily")       #####Checks if tblSingleFamily and tblChildren and either creates them,, or deletes them and then creates them
        DatabaseChanges.create_tblSingleFamily()
    else:
        DatabaseChanges.create_tblSingleFamily()

    exists=DatabaseChanges.check_table_exists("tblChildren")
    if exists == True:
        DatabaseChanges.delete_table("tblChildren")
        DatabaseChanges.create_tblChildren()
    else:
        DatabaseChanges.create_tblChildren()

    for x in range(0,len(all_people)):
        for y in range(x+1,len(all_people)):

           personX=all_people[x]
           personY=all_people[y]
           first = children_dict[personX] 
           second = children_dict[personY]

           if len(first.intersection(second))!=0 and len(first)!=0 and len(second)!=0:   ##########Checks if the intersection of the sets is empty or not
                family_id_queue, first_family_id, all_family_id= add_family(personX, personY, family_id_queue,all_family_id)
                DatabaseChanges.add_children(first,second,first_family_id)
                PeopleUsed.add(personX)
                PeopleUsed.add(personY)

           elif len(first.intersection(second))==0 or len(first)==0 or len(second)==0 :
                pass

    return all_family_id

#======================================================== Dealing With People in tblFamily that are not of the typical format===================================================================

def add_two_unknowns(children_dict):  ###Adds unknown people to database
        person_id_dict=AllPeopleInDatabase.person_id_against_name_dict()
        connection=sqlite3.connect("Family_1.db")
        cursor=connection.cursor()
        sql="""
        SELECT MotherID
        FROM tblFamily
        WHERE MotherID LIKE "%Mother%"
        """
        unknownm=[]
        usedm=[]
        #for row in cursor.execute(sql):
        for row in cursor.execute(sql):
            unknownm.append(row)
        for z in range(len(unknownm)-1,-1,-1):
            if unknownm[z] in person_id_dict:
                unknownm.pop(z)
        for x in range(0,len(unknownm)):
            new_unknown_m= " " + unknownm[x][0]
            if (unknownm[x] not in usedm) and (unknownm[x][0] not in person_id_dict):
                person_rec=[unknownm[x][0],"","","","","","Female","",""]
                cursor.execute("INSERT INTO tblFamily VALUES (?,?,?,?,?,?,?,?,?)", person_rec)
                person_rec=[]
                usedm.append(unknownm[x])
            
                connection.commit()
            

        sql2="""
        SELECT FatherID
        FROM tblFamily
        WHERE FatherID LIKE "%Father%"
        """
        unknownf=[]
        usedf=[]
        for row in cursor.execute(sql2):
            unknownf.append(row)
            for x in range(len(unknownf)-1,-1,-1): ###############################################################################
                if unknownf[x] in person_id_dict:
                    unknownf.pop(x)
            for y in range(0,len(unknownf)):
                if (unknownf[y] not in usedf) and (unknownf[y][0] not in person_id_dict):
                    person_rec=[unknownf[y][0],"","","","","","Male","",""]
                    cursor.execute("INSERT INTO tblFamily VALUES (?,?,?,?,?,?,?,?,?)", person_rec)
                    person_rec=[]
                    usedf.append(unknownf[y])
                    connection.commit()
        return unknownm, unknownf

def add_2_unknowns_to_children_set(unknownm,unknownf,children_dict): ###Adds unknown people to database
    for x in range(0,len(unknownm)):
                   Mother=str(unknownm[x][0])
                   children_set=get_children("Female",Mother)
                   children_dict[Mother]=children_set
    for y in range(0,len(unknownf)):
                   Father=str(unknownf[y][0])
                   children_set=get_children("Male",Father)
                   children_dict[Father]=children_set
    return children_dict
                   
    
        

def add_unknown_parents_to_children_set(children_dict): # Adds unknown people to children set
    person_id_dict = AllPeopleInDatabase.person_id_against_name_dict()
    connection=sqlite3.connect("Family_1.db")
    cursor=connection.cursor()
    sql = """
    SELECT PersonID,MotherID
    FROM tblFamily
    WHERE MotherID LIKE "%_P"
    ORDER BY MotherID
    """
    for row in cursor.execute(sql):
        if (row[1] not in children_dict) and (row[1] not in person_id_dict):
            parent_rec=[row[1],"","","","","","Female","",""]
            cursor.execute("INSERT INTO tblFamily VALUES (?,?,?,?,?,?,?,?,?)",parent_rec)
            connection.commit()
            parent_rec=[]
            children_dict[row[1]]=set()
        children_dict[row[1]].add(row[0])
    
    connection=sqlite3.connect("Family_1.db")
    cursor=connection.cursor()
    sql = """
    SELECT PersonID,FatherID
    FROM tblFamily
    WHERE FatherID LIKE "%_P"
    ORDER BY FatherID
    """
    for row in cursor.execute(sql):
        if (row[1] not in children_dict) and (row[1] not in person_id_dict):
            parent_rec=[row[1],"","","","","","Male","",""]
            cursor.execute("INSERT INTO tblFamily VALUES (?,?,?,?,?,?,?,?,?)",parent_rec)
            connection.commit()
            parent_rec=[]
            children_dict[row[1]]=set()
        children_dict[row[1]].add(row[0])
    return children_dict

def one_unknown_parent(children_dict):
        connection = sqlite3.connect("Family_1.db")
        cursor=connection.cursor()
        sql= """
        SELECT FatherID
        FROM tblFamily
        WHERE MotherID="" AND FatherID<>""
        """
        for row in cursor.execute(sql):
            if row!="":
                unknown_mother = str(str(row[0] + "_P"))
                unknown_mother = "'" + unknown_mother + "'"
                Father = "'" + str(row[0]) + "'"
                for x in range(0,len(children_dict[row[0]])):
                    person = str(list(children_dict[row[0]])[x])
                    person=person_id_format(person)
                    person= "'" + person + "'"
                    
                
                    cursor.execute("UPDATE tblFamily SET MotherID =" + unknown_mother + "WHERE FatherID =" + Father + "AND PersonID =" + person )
                    connection.commit()
                    add_unknown_parents_to_children_set(children_dict)
                
                    
                   
        sql2 = """
        SELECT MotherID
        FROM tblFamily
        WHERE MotherID<>"" AND FatherID = ""
        """
        for row2 in cursor.execute(sql2):
            if row2!="":
                unknown_father = str(str(person_id_format(row2[0])) + "_P")
                unknown_father = "'" + unknown_father + "'"
                Mother = "'" + str(person_id_format(row2[0])) + "'"
                
                for y in range(0,len(children_dict[person_id_format(row2)])):
                       cursor.execute("UPDATE tblFamily SET FatherID =" + unknown_father + "WHERE MotherID =" + Mother )
                       connection.commit()
                    
        connection.commit()
        connection.close()

#==============================================================ID and String Formatting (makes sure everything is in the same/similar format ============================================================================
def person_id_format(variable):
    if type(variable) is tuple:
        variable=variable[0]

    variable.replace("(","")
    variable.replace(")","")
    variable.replace(",","")
    return variable

def check_format_family_id(variable):
  if type(variable) is list:
      variable = str(variable[0])
  if type(variable) is tuple:
      variable=str(variable[0])
  variable=variable.replace("'","")
  variable=variable.replace("(","")
  variable=variable.replace(")","")
  variable=variable.replace(",","")
  return variable

def list_format(list_variable):
    new_list = []
    for x in range(0, len(list_variable)):
        entry = person_id_format(list_variable[x])
        new_list.append(entry)
    return new_list
    
#========================================================= family Queue =========================================================================================
#Creates Queues

def initialise_family_id_queue():
        family_id_queue=[]
        for x in range(1,101):
            family_id_queue.append(str("FID"+str(x)))
        return family_id_queue

def dequeue(family_id_queue):
        first_family_id=family_id_queue.pop(0)
        return first_family_id,family_id_queue

def get_family_id_queue(family_id_queue):
        return family_id_queue


#========================================================== Subroutines for traverse Algorithm to work ===========================================================

def list_of_family_id():
    connection=sqlite3.connect("Family_1.db")
    family_id_list=[]
    cursor=connection.cursor()
    sql = ("""
    SELECT FamilyID
    FROM tblSingleFamily
    """)
    for row in cursor.execute(sql):
        family_id_list.append(row)
    return family_id_list

def create_adjacency_matrix():
    family_matrix=[]
    family_id_list= list_of_family_id()
    family_id_length = len(family_id_list)

    for x in range(0,family_id_length):
        family_matrix.append([])
    for y in range(0,family_id_length):
        for z in range(0, family_id_length):
            family_matrix[y].append([])

    return family_matrix

def create_visited_family_list():
    visited=[]
    return visited

def add_visited_family_list(family,visited):
    visited.append(family)
    return visited

def check_children(child_id,det_children):
    if len(det_children[child_id])==0:
        pass
    elif len(det_children[child_id])!=0:
    
        connection= sqlite3.connect("Family_1.db")
        cursor = connection.cursor()
        parent_family=[]
        child_id = "'" + child_id + "'"
        sql = ("""
        SELECT FamilyID
        FROM tblSingleFamily, tblFamily
        WHERE (((tblSingleFamily.Mother= %s) AND (tblFamily.PersonID = %s))
        OR ((tblSingleFamily.Father = %s) AND (tblFamily.PersonID = %s)))"""% (child_id, child_id, child_id, child_id,))
        for row in cursor.execute(sql):
            parent_family.append(row)
        return parent_family

def check_parents(parent_id):  #Gets the familyID of a family above another one
    valid_person_id = re.match("[A-Z]{1,2}[0-9]{4}", parent_id)
    if not valid_person_id:
        pass
    else:
        parent_in_db=False
        ParentsList=[]
        connection = sqlite3.connect("Family_1.db")
        cursor = connection.cursor()
        parent_id = "'" + parent_id + "'"
        sql0 = ("""
        SELECT MotherID, FatherID
        FROM tblFamily
        WHERE tblFamily.PersonID = %s
        """% (parent_id,))
        for row in cursor.execute(sql0):
            ParentsList.append(row)
        if len(ParentsList)!=0:
                parent_in_db=True
        else:
                pass
        if parent_in_db == True:
            child_family=[]
            sql = ("""
            SELECT FamilyID
            FROM tblChildren
            WHERE tblChildren.PersonID = %s """ % (parent_id,))
            for row in cursor.execute(sql):
                child_family.append(row)

            return child_family
        elif parent_in_db==False:
            pass
    
    
    
    


def traverse(visited, stack, family_matrix, current_family, all_family_id): # A depth first search
    children_dict=det_children()
    if current_family in visited:
        pass
    else:
        visited.append(current_family)   # Appends to visited each time current_family changes
    current_family=check_format_family_id(current_family)
    parents, children = get_family(str(current_family))
    family_below=False

    for x in range(0,len(children)):
        child_id = children[x]
        parent_family = check_children(child_id,children_dict)
        if parent_family is None:
            pass
        else:
            for y in range(0,len(parent_family)):
                parent_familyY=parent_family[y]
                parent_familyY=check_format_family_id(parent_family)
                if parent_familyY in visited:                              
                    pass
                    
                else:
                    family_below=True
                    next_family = str(parent_familyY)
                    next_family = check_format_family_id(next_family)
                    childIDy=child_id
                    break
        

    if family_below==True:

        current_family = check_format_family_id(current_family)
        family_index=int((str(current_family)[3:int(len(current_family))]))-1
        next_family_index = int((next_family[3:int(len(next_family))]))-1      #####Determine position of where info should be added in matrix

        (family_matrix[family_index])[next_family_index].append(1)
        (family_matrix[next_family_index])[family_index].append(-1)
        (family_matrix[family_index])[next_family_index].append(childIDy)
        (family_matrix[next_family_index])[family_index].append(childIDy)##############Adds info to matrix
        (family_matrix[next_family_index])[family_index].append(next_family)
        (family_matrix[family_index])[next_family_index].append(current_family)
        (family_matrix[next_family_index])[family_index].append(current_family)
        (family_matrix[family_index])[next_family_index].append(next_family)

        stack = push(stack, current_family)
        traverse(visited, stack, family_matrix, next_family,all_family_id)  ##Updates stack after family matrix has been ammended

    elif family_below==False:  # If there is no family below, check if there is a family above
        family_above=False
        for z in range(0,len(parents)):

            parent_id = parents[z]
            child_family = check_parents(parent_id)

            if child_family==None or child_family=="None":
                child_family=[]

            if len(child_family)>0:
                child_family=check_format_family_id(child_family)
            else:
                pass
            if len(child_family) ==0:
                pass
            elif len(child_family)>0 and child_family not in visited:
                family_above = True
                break
            else:
                pass

        if family_above==False and len(stack)>=1:
            stack, top_of_stack = pop(stack)
            traverse(visited, stack, family_matrix, top_of_stack,all_family_id)

        elif family_above==False and len(stack)==0 and len(family_matrix)==len(visited): ##########Base case for recursive algorithm
            return family_matrix, visited
        elif family_above==False and len(stack)==0 and len(all_family_id)!=len(visited): #This elif statement deals with families that are 'unconnected' trees

            found=False
            while found==False:
                for x in range(0,len(all_family_id)):
                    if all_family_id[x] not in visited:
                        found=True
                        current_family=all_family_id[x]
                traverse(visited,stack,family_matrix,current_family,all_family_id)

                
            
        elif family_above == True:

            child_family=check_format_family_id(child_family)
            current_family=check_format_family_id(current_family)
            family_index=int((current_family[3:int(len(current_family))]))-1
            child_family_index=int((child_family[3:int(len(child_family))]))-1

            family_matrix[family_index][child_family_index].append(-1)
            family_matrix[child_family_index][family_index].append(1)
            family_matrix[family_index][child_family_index].append(parent_id)
            family_matrix[child_family_index][family_index].append(parent_id)
            family_matrix[child_family_index][family_index].append(child_family)
            family_matrix[family_index][child_family_index].append(current_family)
            family_matrix[child_family_index][family_index].append(current_family)
            family_matrix[family_index][child_family_index].append(child_family)
            
            parent_id=None
            stack = push(stack, current_family)
            traverse(visited, stack, family_matrix, child_family,all_family_id)
            

    
    family_id_list= list_of_family_id()
    family_id_length = len(family_id_list)
    for x in range(0,family_id_length):
        for y in range(0,family_id_length):
            for z in range(0, family_id_length):
                if len(family_matrix[y][z]) == 0:
                    family_matrix[y][z].append(0)
                    family_matrix[y][z].append(0)
                    family_matrix[y][z].append("FID" + str(y+1))   #### Appends 0's afterwards to empty lists.
                    
                else:
                    pass

    return family_matrix, visited

#=============================================Create Stack for traverse algorithm==================================================================
def create_stack():
    stack=[]
    return stack

def push(stack,Item):
    stack.append(Item)
    return stack

def pop(stack):
    top_of_stack= stack.pop()
    return stack, top_of_stack

def peek(stack):
    return stack[len(stack)]

def is_empty(stack):
    if len(stack)==0:
        return True
    else:
        return False
        
#=================================================================== Subroutines for That return variables for Kivy =================================================================================

def all_families_nested_list(all_family_id, family_matrix,distance_dictionary): ####Gets all families in one list
    entire_families = []
    conn = sqlite3.connect("Family_1.db")
    cursor = conn.cursor()
    for x in range(0, len(all_family_id)):
        FamilyID = all_family_id[x]
        family = []
        if distance_dictionary==None:
            generation_number=None
        else:
            generation_number = distance_dictionary[FamilyID]
        family.append(FamilyID)
        family.append(generation_number)
        FamilyID = "'" + FamilyID + "'"

        sql = ("""
        SELECT Mother,Father
        FROM tblSingleFamily
        WHERE tblSingleFamily.FamilyID = %s
        """ % (FamilyID,))

        for row in cursor.execute(sql):
            
            row1=row[0]
            row2=row[1]
            row1 = person_id_format(row1)
            row2=person_id_format(row2)
            if "Father" in row1:
                family.append(row2)
                family.append(row1)
            else:
                family.append(row1)
                family.append(row2)
        family_children = []
        all_children=[]
        for row in cursor.execute("""
            SELECT PersonID
            FROM tblChildren
            WHERE tblChildren.FamilyID = %s
            """ % (FamilyID,)):
            all_children.append(row)
        all_children = list_format(all_children)
        family.append(all_children)
        entire_families.append(family)
    return entire_families





def descendant_number(family_matrix, all_family_id, entered, current, distance_dictionary):
    entered.append(current)
    if len(distance_dictionary) == len(family_matrix): ###Base case
        return distance_dictionary

    for x in range(0, len(entered)):
        family_index_a = int(entered[x][3:len(entered[x])])-1

        for y in range(0, len(all_family_id)):
            extra_distance = int(((family_matrix[family_index_a][y][0])))
            final_family_id = str("FID" + str(y+1))
            if (extra_distance!=0) and (final_family_id not in entered):

                if family_index_a == 1:
                    distance_dictionary[final_family_id] = extra_distance #Finds distance from previous familyID
                    current = final_family_id
                    descendant_number(family_matrix, all_family_id, entered, current, distance_dictionary)
                    return distance_dictionary

                else:
                    total_weight = distance_dictionary.get(entered[x]) + extra_distance  #Finds distance from FID1
                    distance_dictionary[final_family_id] = total_weight
                    current = final_family_id
                    descendant_number(family_matrix, all_family_id, entered, current, distance_dictionary)
                    return distance_dictionary



def create_kivy_matrix(family_matrix1):   #### Gets rid of -1's and 0's for kivy, making  processing easier  later
    kivy_matrix = []
    for x in range(0,len(family_matrix1)):
        for y in range(0,len(family_matrix1)):
            if family_matrix1[x][y][0]==1 :
                kivy_matrix.append(family_matrix1[x][y])
    return kivy_matrix

#===================================================================== Finds family Matrix, Entire families, kivy_matrix and Distance Dictionary =========================================================



def sorting_main(): #Gets all important information

    all_family_id=[]
    children_dict=det_children()
    need_add_1_people=CheckAddUnknowns.check_add_1_unknown()
    if need_add_1_people==True:
        one_unknown_parent(children_dict)
        children_dict = add_unknown_parents_to_children_set(children_dict)
    need_add_2_people=CheckAddUnknowns.check_add_1_unknown()
    if need_add_2_people== True:
        unknownm, unknownf=add_two_unknowns(children_dict)
        children_dict=add_2_unknowns_to_children_set(unknownm,unknownf,children_dict)
    all_family_id=families(children_dict,all_family_id)
    AddGenderTo1Unknown.add_gender_to_1_unknown()

    #Traverse algorithm
    stack=create_stack()
    family_matrix = create_adjacency_matrix()
    visited = create_visited_family_list()
    family_matrix, visited=traverse(visited, stack, family_matrix, "FID1",all_family_id)

    #Generations and Kivy info
    distance_dictionary={"FID1":0}
    entered=[]
    distance_dictionary=descendant_number(family_matrix,all_family_id,entered,"FID1",distance_dictionary)
    distance_dictionary=ChangeDistance.change_distance_dictionary(distance_dictionary)
    entire_families=all_families_nested_list(all_family_id,family_matrix,distance_dictionary)
    family_matrix1=copy.deepcopy(family_matrix)
    kivy_matrix=create_kivy_matrix(family_matrix1)
    return entire_families, family_matrix,children_dict, kivy_matrix



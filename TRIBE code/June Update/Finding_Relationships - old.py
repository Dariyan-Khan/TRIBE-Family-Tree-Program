import sqlite3
import copy
import SortingAlgorithm_09_03_2019 as Sort

def get_person_id(): #Gets all personID's in database
    conn=sqlite3.connect("Family_1.db")
    cursor=conn.cursor()
    cursor.execute("SELECT PersonID from tblFamily")
    all_person_id=cursor.fetchall()
    print(all_person_id)
    return all_person_id

def find_families(entire_families,person,relative): # Finds families for chosen people
        original_person=copy.deepcopy(person)
        original_relative=copy.deepcopy(relative)
        all_person_id=get_person_id()
        for x in range(0,len(all_person_id)):
            if all_person_id[x][0] in person:
                person=all_person_id[x][0]
                print(person)
            if all_person_id[x][0] in relative:
                relative=all_person_id[x][0]
        if "Mother" in person:
            adjustmentP="Child's"
        elif "Father" in person:
            adjustmentP="Child's"
        elif "_P" in person:
            adjustmentP="Child's"
        else:
            adjustmentP=None
        
        for x in range(0,len(entire_families)):
            person_family=entire_families[x]
            if adjustmentP!=None:
                if (person_family[2]==person) or (person_family[3]==person):
                    person=person_family[4][0]
                    break
            elif adjustmentP==None:
                if (person in person_family[4]):
                    break

        if "Mother" in relative:
            adjustmentR="Mother"
        elif "Father" in relative:
            adjustmentR="Father"
        elif "_P" in relative:
            adjustmentR="Parent"
        else:
            adjustmentR=None
        
        for y in range(0,len(entire_families)):
            relative_family=entire_families[y]
            if adjustmentR!=None:
                if (relative_family[0]==relative) or (relative_family[1]==relative):
                    relative=relative_family[4][0]
                    break
            elif adjustmentR==None:
                if (relative in relative_family[4]):
                    break
        return adjustmentP,adjustmentR,person_family,relative_family, original_person, original_relative,person,relative

        
        
def traverse(visited, stack, family_matrix, current_family,person_family_id,relative_family_id,foundP,foundR,person_stack,relative_stack):

        if (foundP==True and foundR==True): ###Base case
            return person_stack, relative_stack,foundR,foundP
        else:
            children_dict=Sort.det_children()
            if current_family in visited:
                pass
            else:
                visited.append(current_family)
            current_family=Sort.check_format_family_id(current_family)
            parents, children = Sort.get_family(str(current_family))
            family_below=False
            for x in range(0,len(children)):
                child_id = children[x]
                parent_family = Sort.check_children(child_id,children_dict)
                if parent_family is None:
                    pass
                else:
                    for y in range(0,len(parent_family)):
                        parent_familyY=parent_family[y]
                        parent_familyY=Sort.check_format_family_id(parent_family)
                        if parent_familyY in visited:
                            pass

                        else:
                            family_below=True
                            next_family = str(parent_familyY)
                            next_family = Sort.check_format_family_id(next_family)
                            child_idY=child_id
                            break


            if family_below==True:
                current_family = Sort.check_format_family_id(current_family)
                family_index=int((str(current_family)[3:int(len(current_family))]))-1
                next_family_index = int((next_family[3:int(len(next_family))]))-1
                stack = Sort.push(stack, current_family)
                if (next_family== person_family_id) and (foundP==False):
                    person_stack=copy.deepcopy(stack)
                    foundP=True

                if (next_family==relative_family_id) and (foundR==False):
                    relative_stack=copy.deepcopy(stack)
                    foundR=True
                person_stack,relative_stack,foundR,foundP=traverse(visited, stack, family_matrix, next_family,person_family_id,relative_family_id,foundP,
                                                                   foundR,person_stack,relative_stack)
                return person_stack,relative_stack,foundR,foundP

            elif family_below==False:

                family_above=False
                for z in range(0,len(parents)):
                    ParentID = parents[z]
                    child_family = Sort.check_parents(ParentID)

                    if child_family==None or child_family=="None":
                        child_family=[]

                    if len(child_family)>0:
                        child_family=Sort.check_format_family_id(child_family)

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

                    stack, top_of_stack = Sort.pop(stack)
                    if (top_of_stack== person_family_id) and (foundP==False):
                        person_stack=copy.deepcopy(stack)
                        foundP=True

                    if (top_of_stack==relative_family_id) and (foundR==False):
                        relative_stack=copy.deepcopy(stack)
                        foundR=True
                    person_stack,relative_stack,foundR,foundP=traverse(visited, stack, family_matrix, top_of_stack,person_family_id,relative_family_id,
                                                                       foundP,foundR,person_stack,relative_stack)
                    return person_stack,relative_stack,foundP,foundR

                elif family_above==False and len(stack)==0 and len(family_matrix)==len(visited):
                    return family_matrix, visited
                elif family_above==False and len(stack)==0 and len(all_family_id)!=len(visited):
                    found=False
                    while found==False:
                        for x in range(0,len(all_family_id)):
                            if all_family_id[x] not in visited:
                                found=True
                                current_family=all_family_id[x]
                        person_stack,relative_stack,foundR,foundP=traverse(visited,stack,family_matrix,current_family,person_family_id,relative_family_id,foundP,foundR,person_stack,relative_stack)
                        return person_stack,relative_stack,foundR,foundP


                elif family_above == True:
                    child_family=Sort.check_format_family_id(child_family)
                    ParentID=None
                    stack = Sort.push(stack, current_family)
                    if (child_family== person_family_id) and (foundP==False):
                        person_stack=copy.deepcopy(stack)
                        foundP=True

                    if (child_family==relative_family_id) and (foundR==False):
                        relative_stack=copy.deepcopy(stack)
                        foundR=True
                    person_stack,relative_stack,foundR,foundP=traverse(visited, stack, family_matrix, child_family,person_family_id,relative_family_id,foundP,foundR,person_stack,relative_stack)
                    return person_stack,relative_stack,foundR,foundP

def find_route_between_people(person_stack,relative_stack,person_family_id,relative_family_id,family_matrix): #Gets route between families

        no_duplicates=False
        count=0
        route=[]
        if person_family_id not in person_stack:
            person_stack.append(person_family_id)
        person_stack_length = len(person_stack)
        if relative_family_id not in relative_stack:
            relative_stack.append(relative_family_id)
        for x in range(len(person_stack)-1,-1,-1):
            route.append(person_stack.pop(x))
        for y in range(0,len(relative_stack)):
            
            route.append(relative_stack.pop(0))

        while no_duplicates==False:
                try: #Used in case index number goes outside range, in which case, a familyID from the route may not need to be deleted

                    current_fam_num=int(route[person_stack_length-1-count][3:len(route[person_stack_length-count-1])])-1
                    next_fam_num=int(route[person_stack_length-count][3:len(route[person_stack_length-count])])-1

                except:

                    current_fam_num=999
                    next_fam_num=999

                try: #Used in case index number goes outside range, in which case, a familyID from the route may not need to be deleted
                    after_current_fam_num= int(route[person_stack_length-2-count][3:len(route[person_stack_length-count-2])])-1
                    after_next_fam_num=int(route[person_stack_length-count+1][3:len(route[person_stack_length-count+1])])-1

                except:
                    after_current_fam_num=1
                    after_next_fam_num=1

                if (int((family_matrix[after_current_fam_num][after_next_fam_num][0])==0) and after_current_fam_num!=after_next_fam_num) or (current_fam_num!=next_fam_num):
                         delete_both=False
                else:
                         delete_both=True
                if delete_both==True:   #(route[person_stack_length-count]==route[person_stack_length-count+1]) and

                        route.pop(person_stack_length-count-1)
                        route.pop(person_stack_length-count-1)
                        if len(route)<3:
                            no_duplicates=True
                        count+=1
                if current_fam_num!=999:

                    if delete_both==False and (route[person_stack_length-1-count]==route[person_stack_length-count]):
                        route.pop(person_stack_length-count-1)
                        no_duplicates=True
                else:  
                        
                        no_duplicates=True
        if route[0]!=person_family_id:
                route.insert(0,person_family_id)
        if route[len(route)-1]!=relative_family_id:
                route.append(relative_family_id)

        return route



def person_id_format(variable):
    if type(variable) is tuple:
        variable=variable[0]

    variable.replace("(","")
    variable.replace(")","")
    variable.replace(",","")
    return variable


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


def get_family_from_person(person):
    conn = sqlite3.connect("Family_1.db")
    cursor = conn.cursor()
    sql = """
        SELECT FamilyID
        FROM tblChildren
        WHERE PersonID=?
        """
    for row in cursor.execute(sql, (person,)):
        person_family = row[0]

    return person_family

def get_person_gender(personX): # Gets gender of person
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

def people_in_route(route, person, relative,family_matrix,adjustmentP,adjustmentR,original_person,original_relative): #Changes familyID's to respective people
        pen_family_num=int(int((route[len(route)-2][3:len(route[len(route)-2])])) - 1)
        final_family_num = int(int((route[len(route)-1][3:len(route[len(route)-1])]))-1)
        if family_matrix[pen_family_num][final_family_num][0]==1:
            child="Y"
        else: child="N"
        people_route=[]
        if adjustmentP!=None :
                people_route.insert(0,original_person)
        elif adjustmentP==None:
                people_route.append(person)
        for x in range(0,len(route)-1):
                if x==0 and adjustmentP!=None:
                        person_gender=get_person_gender(original_person)
                        person_gender=person_gender[0]
                        people_route.append(person+"_C"+"_"+str(person_gender))
                else:                
                        family_1_num=int(int((route[x][3:len(route[x])]))-1)
                        family_2_num=int(int((route[x+1][3:len(route[x+1])]))-1)
                        next_person=family_matrix[family_1_num][family_2_num][1]
                        next_person_gender=get_person_gender(next_person)
                        next_person_gender=next_person_gender[0]
                        if family_matrix[family_1_num][family_2_num][0]==1:
                        
                                people_route.append(next_person + "_C" + "_"+ str(next_person_gender))
                        
                        elif family_matrix[family_1_num][family_2_num][0]==-1:
                                people_route.append(family_matrix[family_1_num][family_2_num][1] +"_A"+"_"+ str(next_person_gender))
                if adjustmentR!=None:
                        relative_gender=get_person_gender(original_relative)
                        people_route.append(original_relative+"_A"+"_"+str(relative_gender))

        if person in people_route[1]:
            people_route.pop(1)
        return people_route,child



def decide_relationship(current_person,next_person,siblings,x,people_route_length,married):  # Finds preliminary relatinships
        if ("_A" in next_person) and ("_M" in next_person) and siblings==False and married==False:
                relationship="Father's"
        elif ("_A" in next_person) and ("_M" in next_person) and siblings==True and married==False:
                relationship = "Brother's"
        elif ("_A" in next_person) and ("_F" in next_person) and siblings==False and married==False:
                relationship="Mother's"
        elif ("_A" in next_person) and ("_F" in next_person) and siblings==True and married==False:
                relationship="Sister's"
        elif ("_C" in next_person) and ("_M" in next_person) and siblings==False and married==False:
                relationship="Son's"
        elif ("_C" in next_person) and ("_M" in next_person) and siblings==True and married==False:
                relationship= "Brother's"
        elif ("_C" in next_person) and ("_F" in next_person) and siblings==False and married==False:
                relationship="Daughter's"
        elif ("_C" in next_person) and ("_F" in next_person) and siblings==True and married==False:
                relationship="Sister's"

        elif married==True and ("_F" in next_person):
                relationship= "Wife's"
        elif married==True and ("_M" in next_person):
                relationship="Husband's"
        

        return relationship
                
        
        


def route_with_relationships(people_route,person,relative,adjustmentP,adjustmentR,original_person,original_relative,child): # Changes ID's in path to relationships and names
                                                                                                                            # at either end

        if adjustmentP!=None:
                person_firstname=get_firstname(original_person)
                person_surname=get_surname(OringinalPerson)
                person_full_name= person_firstname + " " + person_surname
        else:
                person_firstname= get_firstname(person)
                person_surname = get_surname(person)
                person_full_name= person_firstname + " " + person_surname

        if adjustmentR!=None:
                relative_firstname=get_firstname(original_relative)
                relative_surname=get_surname(original_relative)
                relative_full_name= relative_firstname + " " + relative_surname
        else:
                relative_firstname= get_firstname(relative)
                relative_surname = get_surname(relative)
                relative_full_name= relative_firstname + " " + relative_surname
        
        path=person_full_name + "'s"
        people_route_length=len(people_route)
        for x in range(0,people_route_length-1):
                current_person=people_route[x]
                next_person=people_route[x+1]
                current_family=get_family_from_person(current_person[0:6])
                next_family=get_family_from_person(next_person[0:6])
                if current_family==next_family:
                        siblings=True
                else:
                        siblings=False
                current_person_gender=Sort.get_person_gender(current_person[0:6])
                next_person_gender=Sort.get_person_gender(next_person[0:6])
                current_person_children=Sort.get_children(current_person_gender,current_person[0:6])
                next_person_children=Sort.get_children(next_person_gender,next_person[0:6])
                if len(current_person_children.intersection(next_person_children))!=0 and len(current_person_children)!=0 and len(next_person_children)!=0:
                        married=True
                else:
                        married=False
                relationship=decide_relationship(current_person,next_person,siblings,x,people_route_length,married)
                path= path  + " " + relationship
        if relative not in people_route[len(people_route)-1]:
            gender_relative = get_person_gender(relative)
            if gender_relative=='Male' and child=="Y":
                path=path + " " + "Son's"
            elif gender_relative=='Male' and child=="N" and (get_family_from_person(relative)!= get_family_from_person(people_route[0:6])):
                path = path + " " + "Father's"
            elif gender_relative=='Female' and child=="Y":
                path = path + " " + "Daughter's"
            elif gender_relative=='Female' and child=="N" and (get_family_from_person(relative)!= get_family_from_person(people_route[len(people_route)-1][0:6])):
                path = path + "Mother's"
            elif child=="N" and gender_relative=="Male" and  (get_family_from_person(relative)== get_family_from_person(people_route[len(people_route)-1][0:6])):
                path=path + "Brother's"
            elif child=="N" and gender_relative=="Female" and (get_family_from_person(relative)== get_family_from_person(people_route[len(people_route)-1][0:6])):
                path = path + "Sister's"
        path=path + " " + "is" + " " + relative_full_name
        return path

def path_edit(path):
        for x in range(0,3): # Replaces prelimnary relationships with better ones.

                path=path.replace("Father's Father's","GrandFather's")

                path=path.replace("Father's Mother's","GrandMother's" )

                path=path.replace("Father's Son's","Brother's")

                path=path.replace("Father's Daughter's","Sister's")

                path=path.replace("Father's Sister's","Auntie's")

                path=path.replace("Father's Brother's","Uncle's")

                path=path.replace("Brother's Son's", "Nephew")

                path=path.replace("Uncle's Son's", "Cousin's")

                path=path.replace("Brother's Daughter's","Niece")

                path=path.replace("Uncle's Daughter's","Cousin's")

                path=path.replace("Wife's Brother's","Brother-in-Law's")

                path=path.replace("Wife's Sister's", "Sister-in-Law's")
                
                path = path.replace("GrandFather's Father's","Great GrandFather's")

                path= path.replace("GrandFather's Mother's", "Great GrandMother's")

                path= path.replace("GrandFather's Brother's","Great Uncle's")

                path=path.replace("GrandFather's Sister's", "Great Auntie's")
                

                #Mother
                path=path.replace("Mother's Father's","GrandFather's")

                path=path.replace("Mother's Mother's","GrandMother's")

                path=path.replace("Mother's Son's","Brother's")

                path=path.replace("Mother's Daughter's","Sister's")

                path=path.replace("Mother's Sister's","Auntie's")

                path=path.replace("Mother's Brother's","Uncle's")

                path=path.replace("Mother's Sister's","Auntie's")

                path=path.replace("Mother's Brother's","Uncle's")

                path=path.replace("Sister's Son's", "Nephew")

                path=path.replace("Auntie's Son's", "Cousin's")

                path=path.replace("Sister's Daughter's","Niece")

                path=path.replace("Auntie's Daughter's","Cousin's")

                path=path.replace("Husband's Brother's","Brother-in-Law's")

                path=path.replace("Husbands's Sister's", "Sister-in-Law's")

                path = path.replace("Sister's Husbands's", "Sister-in-Law's")

                path = path.replace("GrandMother's Father's","Great GrandFather's")

                path= path.replace("GrandMother's Mother's", "Great GrandMother's")

                path= path.replace("GrandMother's Brother's","Great Uncle's")

                path=path.replace("GrandMother's Sister's", "Great Auntie's")

                #path.replace("    ", " ")
                #path.replace("   ", " ")
                #path.replace("  ", " ")

        return path


def path_correction(path): # removes last 's
        for x in range(0,len(path)):
                if path[x]=="'" and path[x+1]=="s":
                        y=x

        path=path[:y] + path[y+1:]
        path=path[:y] + path[y+1:]
        return path
                
                
                
        

def relations_main(person,relative):
    entire_families, family_matrix, children_dict, kivy_matrix= Sort.sorting_main()
    visited = Sort.create_visited_family_list()
    stack=Sort.create_stack()
    foundP=False
    foundR=False 
    adjustmentP,adjustmentR,person_family,relative_family,original_person,original_relative,person,relative=find_families(entire_families,person,relative)
    person_family_id=person_family[0]
    relative_family_id=relative_family[0]
    person_stack, relative_stack,foundR,foundP=traverse(visited, stack, family_matrix, person_family_id,person_family_id,relative_family_id,foundP,foundR,[],[])
    route=find_route_between_people(person_stack,relative_stack,person_family_id,relative_family_id,family_matrix)
    people_route,child=people_in_route(route,person,relative,family_matrix,adjustmentP,adjustmentR,person,relative)
    path=route_with_relationships(people_route,person,relative,adjustmentP,adjustmentR,original_person,original_relative,child)
    path=path_edit(path)
    path=path_correction(path)
    return path
                

        

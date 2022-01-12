import sqlite3
from datetime import datetime,date



def calc_current_age(DOB):
    date_today=date.today()
    DOB = DOB[0:4] + " " + DOB[5:7] + " " + DOB[8:10]
    DOB = datetime.strptime(DOB, "%Y %m %d")
    return date_today.year - DOB.year - ((date_today.month, date_today.day) < (DOB.month, DOB.day)) 

def list_all_alive():
    all_people=[]
    conn = sqlite3.connect("Family_1.db")
    cursor = conn.cursor()
    for row in cursor.execute('SELECT PersonID,DOB,DOD FROM tblFamily'):
        if row[1]!="" and row[2]=="":
            all_people.append(row[0])

    conn.commit()
    conn.close()

    return all_people  

def get_ages():
    ages_dict={}
    max_person_age=["",0]
    conn= sqlite3.connect("Family_1.db")
    cursor= conn.cursor()
    sql = """
    SELECT PersonID, DOB,DOD
    FROM tblFamily
    """
    #NEED TO EXCLUDE DEAD PEOPLE LATER
    for row in cursor.execute(sql):
        DOB = row[1]
        if DOB!="" and row[2]=="":
            current_age=calc_current_age(DOB)
            ages_dict[row[0]] = current_age

    return ages_dict

def calc_mean():
    ages_dict = get_ages()
    all_people=list_all_alive()
    total_age=0
    for x in range(0,len(all_people)):
        total_age= total_age + int(ages_dict[all_people[x]])
    mean_age = total_age/len(all_people)

    return mean_age
    
    
def calc_square_root(number):
    interval=10
    start =0
    start=float(start)
    for x in range(0,11):
        found=False
        interval=float(interval/10)
        while found==False:
            if ((start**2) <= float(number) and (start+interval)**2 >= float(number)):
                found = True
                
            else:
                start=start+interval
    return round(start,10)
        
def calc_var():
    ages_dict=get_ages()
    all_people=list_all_alive()
    ages_squared=0
    mean_age=calc_mean()
    for x in range(0,len(all_people)):
        ages_squared=ages_squared + ((ages_dict[all_people[x]])**2)
    variance = (ages_squared/len(all_people)) - (mean_age**2)
    return variance

def calc_sd():
    variance=calc_var()
    standard_deviation = calc_square_root(variance)
    return standard_deviation

def just_ages(ages_dict,all_people):
    just_ages_list=[]
    for x in range(0,len(all_people)):
        if all_people[x] in ages_dict:
            just_ages_list.append(ages_dict[all_people[x]])
        
    return just_ages_list

def median(just_ages_list):
    just_ages_list=sorted(just_ages_list)
    if len(just_ages_list)%2==1:
        median_age = just_ages_list[int((len(just_ages_list)+1)/2)-1]
    else:
        median_age = (just_ages_list[int(len(just_ages_list)/2)-1] + just_ages_list[int((len(just_ages_list)/2))])/2

    return median_age

def mode(just_ages_list):
    return max(set(just_ages_list), key=just_ages_list.count)

def max_age(just_ages_list,ages_dict,all_people):
    max_age_people=[]
    max_age=max(just_ages_list)
    for x in range(0,len(all_people)):
        if ages_dict[all_people[x]]==max_age:
            max_age_people.append(all_people[x])
    return max_age,max_age_people

def min_age(just_ages_list,ages_dict,all_people):
    min_age_people=[]
    min_age = min(just_ages_list)
    for x in range(0, len(all_people)):
        if ages_dict[all_people[x]] == min_age:
            min_age_people.append(all_people[x])
    return min_age, min_age_people




def statistics_main():
    all_people=list_all_alive()
    ages_dict=get_ages()
    just_ages_list=just_ages(ages_dict,all_people)
    mode_age =mode(just_ages_list)
    median_age= median(just_ages_list)
    mean_age=calc_mean()
    variance=calc_var()
    standard_deviation=calc_sd()
    max_age_people,max_age_people_list=max_age(just_ages_list, ages_dict,all_people)
    min_age_people, min_age_people_list = min_age(just_ages_list,ages_dict,all_people)
    return mode_age,median_age, mean_age,variance,standard_deviation, max_age_people,max_age_people_list,min_age_people,min_age_people_list

def statistics_main_1_person():
    all_people = list_all_alive()
    ages_dict = get_ages()
    just_ages_list = just_ages(ages_dict, all_people)
    mode_age=just_ages_list[0]
    median_age=just_ages_list[0]
    mean_age=just_ages_list[0]
    variance=0
    standard_deviation=0
    max_age_people, max_age_people_list = max_age(just_ages_list, ages_dict, all_people)
    min_age_people, min_age_people_list = min_age(just_ages_list, ages_dict, all_people)
    return mode_age, median_age, mean_age, variance, standard_deviation, max_age_people, max_age_people_list, min_age_people, min_age_people_list

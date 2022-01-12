import sqlite3
import time

def check_table_exists(tablename):
        connection = sqlite3.connect('Family_1.db')
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        list_of_tables=(cursor.fetchall())
        if (tablename,) in list_of_tables:
            exists=True
            return exists
        else:
            exists=False
            return exists, list_of_tables

def delete_table(tablename):
        connection= sqlite3.connect('Family_1.db',)
        cursor=connection.cursor()
        sql= ("""DROP TABLE %s """ % tablename)
        cursor.execute(sql)
        connection.commit()
        connection.close()
        
        

    
def create_tblSingleFamily():
        #first_family_id= FamilyIDQueue.Dequeue(FamilyID)
        connection = sqlite3.connect("Family_1.db")
        cursor = connection.cursor()
        sql_command = """
            CREATE TABLE tblSingleFamily
            (
            FamilyID  TEXT,
            Mother    TEXT,
            Father    TEXT,
            primary key (FamilyID)
            )"""
        cursor.execute(sql_command)
        print("tblSingleFamily created")
        connection.commit()
        connection.close()



def create_tblChildren():
        #first_family_id= FamilyIDQueue.Dequeue(FamilyID)
        connection = sqlite3.connect("Family_1.db")
        cursor = connection.cursor()
        sql_command = """
            CREATE TABLE tblChildren
            (
            FamilyID  TEXT,
            PersonID  TEXT,
            primary key (FamilyID, PersonID)
            )"""
        cursor.execute(sql_command)
        print("tblChildren")
        connection.commit()
        connection.close()

def add_children(first, second, first_family_id):
        connection=sqlite3.connect('Family_1.db')
        cursor=connection.cursor()
        children_of_people= first.intersection(second)
        children_rec=[first_family_id]
        for z in range(0,len(children_of_people)):
            children_rec.append(children_of_people.pop())
            cursor.execute("INSERT INTO tblChildren VALUES (?,?)", children_rec)
            connection.commit()
            children_rec=[first_family_id]

        connection.close()

import sqlite3

def get_everything():
    all=[]
    everything_dict={}
    conn=sqlite3.connect("Family_1.db")
    cursor=conn.cursor()
    for row in cursor.execute ('SELECT * FROM tblFamily'):
        all.append(row)
        for y in range(0,len(all)):
            everything_dict[all[y][0]]=all[y]
    return everything_dict



def get_everything_connected():
    all=[]
    everything_connected_dict = {}
    conn = sqlite3.connect("Family_1.db")
    cursor = conn.cursor()
    for row in cursor.execute('SELECT * FROM tblFamily'):
        all.append(row)
        for y in range(0, len(all)):
            all[y]
            everything_connected_dict[all[y][0]] = all[y]
    return everything_connected_dict



#everything_dict=get_everything_connected()
#print(everything_dict)
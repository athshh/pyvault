import sqlite3 as sql
import random
import string

def generatePassword(length, digits, letters, special):
    expPass=[]
    charSet=[]
    if digits:
        charSet+=string.digits
    if letters:
        charSet+=string.ascii_letters
    if special:
        charSet+=string.punctuation
    for i in range(length):
        expPass.append(random.choice(charSet))
    return "".join(expPass)



def createDB(DBName):
    con=sql.connect(f'{DBName}')
    cur=con.cursor()
    con.commit()
    return 1

def accessDB():
    try:
        con=sql.connect(':memory:',check_same_thread=False)
        return con
    except:
        return f"Database not found."

def createGroup(groupName,connection,cursor):
    
    cursor.execute(f"CREATE TABLE {groupName}(ID INTEGER PRIMARY KEY AUTOINCREMENT, service VARCHAR(255), loginID VARCHAR(255), loginPass VARCHAR(255))")
    connection.commit()
    return 1

def viewGroup(groupName,cursor):
    res=cursor.execute(f"SELECT * FROM {groupName}")
    return res.fetchall()

def deleteGroup(groupName, connection,cursor):
    
    try:
        cursor.execute(f"DROP TABLE {groupName}")
        connection.commit()
        return 1
    except:
        return f"Table {groupName} not found."

def createEntry(groupName, service, loginID, loginPass, connection,cursor):
    
    cursor.execute(f"INSERT INTO {groupName} (service, loginID, loginPass) VALUES (?, ?, ?)",(service,loginID,loginPass))
    connection.commit()
    return 1

def viewEntry(groupName, service, connection,cursor):
    
    res=cursor.execute(f"SELECT * FROM {groupName} WHERE service=?",(service,))
    return res.fetchone()

def updateEntry(groupName, service, loginID, loginPass,ID, connection,cursor):
    
    cursor.execute(f"UPDATE {groupName} SET service=?, loginID=?, loginPass=? WHERE ID=?",(service, loginID, loginPass,ID))
    connection.commit()
    return 1

def deleteEntry(ID,groupName, connection,cursor):
    
    cursor.execute(f"DELETE FROM {groupName} WHERE ID=?",(ID,))
    connection.commit()
    return 1

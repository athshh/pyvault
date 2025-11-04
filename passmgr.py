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
    cur.execute("CREATE TABLE main(ID INTEGER PRIMARY KEY AUTOINCREMENT, service VARCHAR(255),loginID VARCHAR(255),loginPass VARCHAR(255))")
    con.commit()
    return 0

def accessDB(DBName):
    try:
        con=sql.connect(f'{DBName}')
        return con
    except:
        return f"Database {DBName} not found."

def createGroup(groupName,connection):
    cursor=connection.cursor()
    cursor.execute(f"CREATE TABLE {groupName}(ID INTEGER PRIMARY KEY AUTOINCREMENT, service VARCHAR(255), loginID VARCHAR(255), loginPass VARCHAR(255))")
    connection.commit()
    return 0

def viewGroup(groupName, connection):
    cursor=connection.cursor()
    res=cursor.execute(f"SELECT * FROM {groupName}")
    return res.fetchall()

def deleteGroup(groupName, connection):
    cursor=connection.cursor()
    try:
        cursor.execute(f"DROP TABLE {groupName}")
        connection.commit()
        return 0
    except:
        return f"Table {groupName} not found."

def createEntry(groupName, service, loginID, loginPass, connection):
    cursor=connection.cursor()
    cursor.execute(f"INSERT INTO {groupName} (service, loginID, loginPass) VALUES (?, ?, ?)",(service,loginID,loginPass))
    connection.commit()
    return 0

def viewEntry(groupName, service, connection):
    cursor=connection.cursor()
    res=cursor.execute(f"SELECT * FROM {groupName} WHERE service=?",(service,))
    return res.fetchone()

def updateEntry(groupName, service, loginID, loginPass,ID, connection):
    cursor=connection.cursor()
    cursor.execute(f"UPDATE {groupName} SET service=?, loginID=?, loginPass=? WHERE ID=?",(service, loginID, loginPass,ID))
    connection.commit()
    return 0

def deleteEntry(ID,groupName, connection):
    cursor=connection.cursor()
    cursor.execute(f"DELETE FROM {groupName} WHERE ID=?",(ID,))
    connection.commit()
    return 0

# Actual management

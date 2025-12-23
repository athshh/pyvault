import encrypt
from cryptography.fernet import Fernet
import passmgr 
import os
import sqlite3 as sql
from flask import Flask, jsonify, request

app = Flask(__name__)
con=0
cur=0
key=0
db=0

# TODO: add password-based keygen and access

@app.route('/generateKey',methods=['GET'])
def generateKey():
    encrypt.generateKey()
    return jsonify({'hello':'world'}),201

@app.route('/accessKey',methods=['GET'])
def accessKey():
    global key
    key=encrypt.readKey()
    return jsonify({'status':'success'}),201

def checkKey():
    return key != 0

@app.route('/pass/createDB', methods=['POST'])
def createDB():
    if not checkKey():
        return jsonify({'error':'no valid key loaded'}),400
    data=request.json
    passmgr.createDB(f"{data['name']}.db")
    with open(f"{data['name']}.db",'rb') as dbFile:
        decData=dbFile.read()
        encData=encrypt.encryptData(key,decData)
        with open(f"{data['name']}.xpdb",'wb+') as tempFile:
            tempFile.write(encData)
    os.remove(f"{data['name']}.db")
    return jsonify({'status':'success'}), 201

@app.route('/pass/accessDB', methods=['POST'])
def accessDB():
    if not checkKey():
        return jsonify({'error':'no valid key loaded'}),400
    data=request.json
    temp_path = f"{data['name']}_temp.db" # Added temp path for bridge
    with open(f"{data['name']}.xpdb",'rb') as encFile:
        encData=encFile.read()
        decData=encrypt.decryptData(key,encData)
    
    with open(temp_path, 'wb') as f: # Write decrypted bytes to temp file
        f.write(decData)
        
    global con,cur
    con = sql.connect(':memory:', check_same_thread=False) # Initialize memory connection
    disk_con = sql.connect(temp_path) # Connect to temp file
    disk_con.backup(con) # Backup temp file into RAM
    disk_con.close()
    
    if os.path.exists(temp_path): # Delete temp file bridge
        os.remove(temp_path)
        
    cur=con.cursor()
    return jsonify({'status':'success'}), 201

@app.route('/pass/closeDB',methods=['POST'])
def closeDB():
    if not checkKey():
        return jsonify({'error':'no valid key loaded'}),400
    data=request.json
    temp_path = f"{data['name']}_save.db" # Added temp path for saving
    global con,cur,db
    if con == 0:
        return jsonify({'status':'error','message':'No DB open'}),400
    
    save_disk_con = sql.connect(temp_path) # Connect to temp save file
    con.backup(save_disk_con) # Backup RAM to temp file
    save_disk_con.close()
    
    with open(temp_path, 'rb') as f: # Read bytes from temp file
        decData = f.read()
        
    with open(f"{data['name']}.xpdb",'wb') as encFile:
        encData = encrypt.encryptData(key, decData) # Encrypt the bytes
        encFile.write(encData)
        db=0
        
    if os.path.exists(temp_path): # Delete temp save file
        os.remove(temp_path)
        
    con.close()
    cur=0
    con=0
    return jsonify({'status':'success'}), 201

@app.route('/pass/createGroup',methods=['POST'])
def createGroup():
    if not checkKey():
        return jsonify({'error':'no valid key loaded'}),400
    data=request.json
    groupName=data['group-name']
    res=passmgr.createGroup(groupName,con,cur)
    if res:
        return jsonify({'status':'success'}),201

@app.route('/pass/viewGroup',methods=['POST'])
def viewGroup():
    if not checkKey():
        return jsonify({'error':'no valid key loaded'}),400
    data=request.json
    groupName=data['group-name']
    res=passmgr.viewGroup(groupName,cur)
    return jsonify({'data':res}),201

@app.route('/pass/deleteGroup',methods=['POST'])
def deleteGroup():
    if not checkKey():
        return jsonify({'error':'no valid key loaded'}),400
    data=request.json
    groupName=data['group-name']
    res=passmgr.deleteGroup(groupName,con,cur)
    return jsonify({'data':res}),201

@app.route('/pass/createEntry',methods=['POST'])
def createEntry():
    if not checkKey():
        return jsonify({'error':'no valid key loaded'}),400
    data=request.json
    groupName=data['group-name']
    serviceName=data['service']
    loginID=data['loginID']
    loginPassword=data['loginPassword']
    res=passmgr.createEntry(groupName,serviceName,loginID,loginPassword,con,cur)
    return jsonify({'data':res}),201

@app.route('/pass/viewEntry',methods=['POST'])
def viewEntry():
    if not checkKey():
        return jsonify({'error':'no valid key loaded'}),400
    data=request.json
    groupName=data['group-name']
    serviceName=data['service']
    res=passmgr.viewEntry(groupName,serviceName,con,cur)
    return jsonify({'data':res}),201

@app.route('/pass/updateEntry',methods=['POST'])
def updateEntry():
    if not checkKey():
        return jsonify({'error':'no valid key loaded'}),400
    data=request.json
    entryID=data['entryID']
    groupName=data['group-name']
    serviceName=data['service']
    loginID=data['loginID']
    loginPassword=data['loginPassword']
    res=passmgr.updateEntry(groupName,serviceName,loginID,loginPassword,entryID,con,cur)
    return jsonify({'data':res}),201

@app.route('/pass/deleteEntry',methods=['POST'])
def deleteEntry():
    if not checkKey():
        return jsonify({'error':'no valid key loaded'}),400
    data=request.json
    groupName=data['group-name']
    entryID=data['entryID']
    res=passmgr.deleteEntry(entryID,groupName,con,cur)
    return jsonify({'data':res}),201

if __name__=='__main__':
    app.run(debug=True)

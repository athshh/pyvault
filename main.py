import encrypt
from cryptography.fernet import Fernet
import passmgr 
import os
from flask import Flask, jsonify, request

app = Flask(__name__)
con=0
key=0

@app.route('/generateKey',methods=['GET'])
def generateKey():
    encrypt.generateKey()
    return jsonify({'hello':'world'}),201

@app.route('/accessKey',methods=['GET'])
def accessKey():
    global key
    key=encrypt.readKey()
    return jsonify({'status':'success'}),201

@app.route('/pass/createDB', methods=['POST'])
def createDB():
    data=request.json
    passmgr.createDB(data['name'])
    with open(f'{data['name']}.db','rb') as dbFile:
        decData=dbFile.read()
        encData=encrypt.encryptData(key,decData)
        with open(f'{data['name']}.xpdb','wb+') as tempFile:
            tempFile.write(encData)
    os.remove(f'{data['name']}.db')
    return jsonify({'status':'success'}), 201

@app.route('/pass/accessDB', methods=['POST'])
def accessDB():
    data=request.json
    with open(f'{data['name']}.xpdb','rb') as encFile:
        encData=encFile.read()
        decData=encrypt.decryptData(key,encData)
        with open(f'{data['name']}.db','wb+') as tempFile:
            tempFile.write(decData)
    os.remove(f'{data['name']}.xpdb')
    global con
    con=passmgr.accessDB(data['name'])
    return jsonify({'status':'success'}), 201

@app.route('/pass/createGroup',methods=['POST'])
def createGroup():
    data=request.json
    groupName=data['group-name']
    res=passmgr.createGroup(groupName,con)
    if res:
        return jsonify({'status':'success'}),201

@app.route('/pass/viewGroup',methods=['POST'])
def viewGroup():
    data=request.json
    groupName=data['group-name']
    res=passmgr.viewGroup(groupName,con)
    return jsonify({'data':res}),201


if __name__=='__main__':
    app.run(debug=True)

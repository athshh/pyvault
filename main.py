import encrypt
import passmgr 
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/pass/createDB', methods=['GET'])
def createDB():
    return jsonify({"password":"xyz"})


if __name__=='__main__':
    app.run(debug=True)

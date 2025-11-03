from cryptography.fernet import Fernet

def generateKey(fileName):
    key = Fernet.generate_key()
    with open(f'{fileName}.key','wb') as f:
        f.write(key)
    return

def readKey(filePath):
    try:
        with open(f'filePath', 'rb') as f:
            return Fernet(f.read())
    except:
        return "No file found. Try again."

def encryptData(key,file):
    return key.encrypt(file)

def decryptData(key,file):
    return key.decrypt(file)

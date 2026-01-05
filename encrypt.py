from cryptography.fernet import Fernet

def generateKey():
    key = Fernet.generate_key()
    with open(f'pyvault.key','wb') as f:
        f.write(key)
        f.close()
    return

def readKey(filepath):
    try:
        with open(filepath, 'rb') as f:
            key=Fernet(f.read())
            return key
    except:
        return "No file found. Try again."

def encryptData(key,file):
    return key.encrypt(file)

def decryptData(key,file):
    return key.decrypt(file)

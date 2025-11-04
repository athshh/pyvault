def readFile(fileName):
    with open(f"{fileName}.xas",'rb') as f:
        content=f.read()
        return content

def writeFile(fileName, content):
    with open(f"{fileName}.xas",'wb') as f:
        f.write(content)
        return 0

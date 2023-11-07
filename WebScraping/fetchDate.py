import requests
import csv
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

count=0
def getSoup(url):
    response = requests.get(url)
    htmlContent = response.content
    soup = BeautifulSoup(htmlContent, 'html.parser')
    return soup
def getParagraph(soup):
    body = ''
    for data in soup.find_all("p"):
       # print(data.get_text())
        body+=data.get_text()+"\n"
    return body
def getPath(urlId):
    return "OutputFiles/"+urlId+".txt"
def writeToFile(body, path):
     with open(path, 'a', encoding="utf-8") as f:
        f.write(body)
     global count
     count+=1
def readCSV(fileName):
    with open(fileName, mode ='r')as file:
        data=[]
        csvFile = csv.reader(file)
        for lines in csvFile:
            data.append(lines)
        data.pop(0)
    return data

def fetchDataAndWriteToFile(elm):
    urlId=elm[0]
    url=elm[1]
    soup=getSoup(url)
    body=getParagraph(soup)
    path = getPath(urlId)
    print(path)
    writeToFile(body,path)
    return {"result":f"{urlId} file created"}
def main():
    data=readCSV('Input.csv')
    executer=ThreadPoolExecutor(12)
    futures=[]
    for elm in data:
            #fetchDataAndWriteToFile(elm)
            future=executer.submit(fetchDataAndWriteToFile,(elm))
            futures.append(future)

    executer.shutdown(wait=True)
    for future in futures:
        print(future.result())

    print("file Count "+str(count))

if __name__=="__main__":
    main()

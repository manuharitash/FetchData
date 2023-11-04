import requests
import os
import time
apiKey=['zFaJQYT9LZsoFR56ovG1pvxP','v6QNmMCtTPRziLxpKGdX98G8']
successCount=0

def checkIfFilePresent(filePath,outputImageFolderPath):
    dir_list = os.listdir(outputImageFolderPath)
    fileName=filePath.split('/').pop()
    fileName=fileName.split('.').pop(0)+'no-bg.png'
    if(dir_list.__contains__(fileName)):
        print('Already Removed Background for '+fileName)
        return True
    else:
        return False


def removeBackground(filePath,fileName,api,apiKeyIndex,outputImageFolderPath):
    print(fileName)
    outputImageFilePath=outputImageFolderPath+fileName+'no-bg'+'.png'
    if(checkIfFilePresent(filePath,outputImageFolderPath)==True):
        return
    response = requests.post(
        api,
        files={'image_file': open(filePath, 'rb')},
        data={'size': 'auto'},
        headers={'X-Api-Key': apiKey[apiKeyIndex]}
    )
    if response.status_code == requests.codes.ok:
        with open(outputImageFilePath, 'wb') as out:
            out.write(response.content)
        successCount+1
    elif response.status_code==429:
        print("Too many calls , sleeping for "+response.headers["Retry-After"])
        time.sleep(int(response.headers["Retry-After"]))

    elif response.status_code==402:
        print("Isufficient Credit left on apikey"+apiKey[apiKeyIndex])
        if(apiKeyIndex<apiKey.__len__()):
            removeBackground(filePath,fileName,api,apiKeyIndex+1,outputImageFolderPath)
        else:
            print("API KEYS EXHAUSHTED")

    else:
        print("Error:", response.status_code, response.text)


def main():
    folderPath= 'C:/Users/dell/PycharmProjects/FetchData/RemoveBg/inputFolder'
    dir_list = os.listdir(folderPath)
    outputImageFolderPath='OutputImageFolder/'
    api='https://api.remove.bg/v1.0/removebg'
    for file in dir_list:
        filePath=folderPath+'/'+file
        fileName=file.split('.').pop(0)
        removeBackground(filePath,fileName,api,0,outputImageFolderPath)

    print("successfully removed background for "+str(successCount)+" files")
if __name__=="__main__":
    main()

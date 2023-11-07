import os

# Get the list of all files and directories

#checking if file already present in folder
outputImageFolderPath= 'C:/Users/dell/PycharmProjects/FetchData/RemoveBg/OutputImageFolder'
outputFilePath='C:/Users/dell/PycharmProjects/FetchData/RemoveBg/OutputImageFolder/20231028_143117no-bg.png'
dir_list = os.listdir(outputImageFolderPath)
fileName=outputFilePath.split('/').pop()

print("fileName="+fileName)
if(dir_list.__contains__(fileName)):
    print( True)
else: print(False)

"""""
dir_list = os.listdir(outputFolderPath)

for file in dir_list:
    filePath= outputFolderPath + file
    fileName=file.split('.').pop(0)

print("Files and directories in '", outputFolderPath, "' :")

# prints all files
print(dir_list)
"""

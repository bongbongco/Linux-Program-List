#-*- coding: utf-8 -*-

import os
import shutil
import re

def search(dirName):
    fileNameDictionary = {}
    num = 0
    
    try:
        fileNames = os.listdir(dirName)
        for fileName in fileNames:
            
            full_fileName = os.path.join(dirName, fileName)
            if os.path.isdir(full_fileName):
                search(full_fileName)
            else:
                fileName = os.path.split(full_fileName)[-1]
                sourceName = fileName.split('_')[0]

                if sourceName in fileNameDictionary:
                    fileNameList = []
                    
                    #filePathStoredType= type(fileNameDictionary[sourceName])
                    if type(fileNameDictionary[sourceName]) == type([]):
                        for searchFileName in fileNameDictionary[sourceName]:
                            fileNameList.append(searchFileName)
                    else:
                        fileNameList.append("C:\\dev\\2016.11\\work\\"+fileName.split('_')[0]+'_'+fileName.split('_')[1]+".txt")
                        fileNameList.append(fileNameDictionary[sourceName])
                    fileNameList.append(full_fileName)
                    fileNameDictionary[sourceName] = fileNameList
                    continue
                fileNameDictionary[sourceName] = full_fileName
                                            
    except PermissionError:
        pass
    
    return fileNameDictionary

def main():
    fileNameDictionary = search(u"C:\\dev\\2016.11\\리눅스")
    fileKeys = fileNameDictionary.keys()
    
    for fileKey in fileKeys:
        filecreater = 0
        writeFile = ''
        deplicateFileList= fileNameDictionary[fileKey]
        
        for filePath in deplicateFileList:
            filecreater = filecreater + 1
            
            if filecreater == 1 :
                writeFile = filePath
                continue
            
            if filecreater == 2 :
                shutil.copy(filePath, writeFile)
                continue
            
            readFile = open(filePath)
            fileAddContent = open(writeFile, 'a')
            '''
            lines = readFile.read()
            
            for commonData in commonDataList:
                lines = commonData.sub('', lines)
                #lines = re.sub ("###   Process List Start(ps -ef)   ###[\s*|\S*]*|[\s*|\S*]*###   Process List END   ###", '', lines)
            
            '''
            lines = readFile.readlines()
            flag = 0
            for line in lines:
                line = line.splitlines()[0]
                if line == '###   RPM List END   ###':
                    flag = 1
                if line == '###   Directory Crawling Start(/tmp)   ###':
                    flag = 0
                    continue
                if flag == 0:
                    continue

                fileAddContent.write(line+'\n')
                
            readFile.close()
            fileAddContent.close()
            
            
if __name__ == '__main__':
    main()
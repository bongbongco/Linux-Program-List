#-*- coding: utf-8 -*-

import os
import shutil
import re
from multiprocessing import Process, Manager


def search(dirName):
    fileNameDictionary = {}
    num = 0
    
    fileNames = os.listdir(dirName)
    for fileName in fileNames:
        
        full_fileName = os.path.join(dirName, fileName)
        if os.path.isdir(full_fileName):
            search(full_fileName)
        else:
            fileName = os.path.split(full_fileName)[-1]
            sourceName = fileName.split('_')[0]
            fileNameDictionary[sourceName] = full_fileName
                  
    return fileNameDictionary

def DuplicateValue(source, lines, writerPath):
    for line in lines:
        line = line.splitlines()[0]
        if line == source:
            return False

    writer = open(writerPath, 'a')
    writer.write(source+'\n')
    writer.close
    

def WritingDirectory(lines, seperator, writer, reader):
    flag = 0
    
    for line in lines:
        line = line.splitlines()[0]
        if line[:30] == seperator['start']:
            flag = 1
            continue
        if line[:28] == seperator['end']:
            flag = 0
            continue
        if flag == 0:
            continue
        if (line[-2:] == ' .'#현재 디렉터리
            or line[-3:] == ' ..'#상위 디렉터리
            or line[:5] == 'total'#총 개수
           ):
            continue
        if line[:1] == '/':
            baseDir = line[:-1]
            continue
            
        objectInfo = re.compile('.+\s+\d+\s+\w+\s+\w+\s+\d+\s+\w+\s+\d+\s+[\d|\d\d:\d\d]+\s') # 파일/디렉터리 명 을 제외한 나머지 정보 제거
        Object = objectInfo.sub('', line)
        
        duplicateCheckLines = reader.readlines()
        
        try:
            source = baseDir+Object
            #mulit_open = Process(target=DuplicateValue, args=(baseDir+Object, duplicateCheckLines ,writerPath))
            #mulit_open.start()
        except:
            source = Object
            #mulit_open = Process(target=DuplicateValue, args=(Object, duplicateCheckLines ,writerPath))
            #mulit_open.start()
    #mulit_open.join()
        #writer = open(writerPath, 'a')
        writer.write(source+'\n')


def WritingContent(lines, seperator, writer, category=None):
    flag = 0
    
    for line in lines:
        line = line.splitlines()[0]
        if line == seperator['start']:
            flag = 1
            continue
    
        if (line[:3] == 'UID'#CentOS
            or line[4:8] == 'Name'#Ubuntu
            or line[:4] == '+++-'#Ubuntu
            or line[:8] == 'Desired='#Ubuntu
            or line[:9] == '| Status='#Ubuntu
            or line[:8] == '|/ Err?='#Ubuntu
            ):
            continue

        if line == seperator['end']:#Ubuntu
            flag = 0
            continue
        if flag == 0:
            continue
            
        if category != None: #프로세스 리스트
            processInfo = re.compile('\w+\s+\d+\s+\d+\s+\d+\s+.+\s+[\w+|\W+]+\s+\d\d:\d\d:\d\d\s+')
            line = processInfo.sub('', line) # 프로세스 커멘드를 제외한 나머지 정보 제거
            if (line == '/sbin/init'#shell
                or re.match('\[.+\]', line)
                ):
                continue
        if line[:2] == 'ii' or line[:2] == 'iF' or line[:2] == 'it' or line[:2] == 'rc': #  Ubuntu Package List 불필요 정보 제거
            processInfo = re.compile('\s+[amd\d+|all]+\s+.+')  
            line = processInfo.sub('', line[4:]) # 프로세스 커멘드를 제외한 나머지 정보 제거
            line = re.sub('\s+', '-', line) #
            
        writer.write(line+'\n')
    
    
def WorkManager(lines, state):
    ProcessList = {'start':'###   Process List Start(ps -ef)   ###'
                   ,'end':'###   Process List END   ###'}
    RPMList = {'start':'###   RPM List Start(rpm -qa)   ###'
                   ,'end':'###   RPM List END   ###'}
    DirectoryList = {'start':'###   Directory Crawling Start'
                   ,'end':'###   Directory Crawling END'}    

    writePath = "C:\\dev\\2016.11\\02\\"
    processListWriter = open(writePath + "ProcessList.txt", 'a')
    rpmListWriter = open(writePath + "RPMList.txt", 'a')
    directoryWriter = open(writePath + "DirectoryList.txt", 'a')
    directoryReader = open(writePath + "DirectoryList.txt", 'r')
    dictionaryListPath = writePath + "DirectoryList.txt"

    WritingContent(lines, ProcessList, processListWriter, 'process')
    WritingContent(lines, RPMList, rpmListWriter)
    WritingDirectory(lines, DirectoryList, directoryWriter, directoryReader)
    
    processListWriter.close()
    rpmListWriter.close()
    directoryWriter.close()
    directoryReader.close()
    
    
def main():
    fileNameDictionary = search(u"C:\\dev\\2016.11\\01")
    
    fileKeys = fileNameDictionary.keys()
    
    for fileKey in fileKeys:
        filePath = fileNameDictionary[fileKey]

        readFile = open(filePath)
        lines = readFile.readlines()
        readFile.close()
        
        mulit_open = Process(target=WorkManager, args=(lines, 'start'))
        mulit_open.start()

    mulit_open.join()

            
if __name__ == '__main__':
    main()
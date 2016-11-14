#-*- coding: utf-8 -*-

import os
import shutil
import re
from multiprocessing import Process


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

def WritingDirectory(lines, seperator, writer):
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
        if line[-2:] == ' .' or line[-3:] == ' ..':
            continue
        if line[:5] == 'total':
            continue
        if line[:1] == '/':
            baseDir = line[:-1]
            continue
            
        objectInfo = re.compile('.+\s+\d+\s+\w+\s+\w+\s+\d+\s+\w+\s+\d+\s+[\d|\d\d:\d\d]+\s') # 파일/디렉터리 명 을 제외한 나머지 정보 제거
        Object = objectInfo.sub('', line)
        #print Object
        try:
            writer.write(baseDir+Object+'\n')
        except:
            writer.write(Object+'\n')
        
        #writer.write(line+'\n')

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
    
def WorkManager():
    
    
def main():
    fileNameDictionary = search(u"C:\\dev\\2016.11\\01")
    ProcessList = {'start':'###   Process List Start(ps -ef)   ###'
                   ,'end':'###   Process List END   ###'}
    RPMList = {'start':'###   RPM List Start(rpm -qa)   ###'
                   ,'end':'###   RPM List END   ###'}
    DirectoryList = {'start':'###   Directory Crawling Start'
                   ,'end':'###   Directory Crawling END'}
    
    fileKeys = fileNameDictionary.keys()
    
    for fileKey in fileKeys:
        filecreater = 0
        writePath = "C:\\dev\\2016.11\\02\\"
        filePath = fileNameDictionary[fileKey]

        readFile = open(filePath)
        processListWriter = open(writePath + "ProcessList.txt", 'a')
        rpmListWriter = open(writePath + "RPMList.txt", 'a')
        directoryListWriter = open(writePath + "DirectoryList.txt", 'a')
        
        lines = readFile.readlines()
        WritingContent(lines, ProcessList, processListWriter, 'process')
        WritingContent(lines, RPMList, rpmListWriter)
        WritingDirectory(lines, DirectoryList, directoryListWriter)
        
        readFile.close()
        processListWriter.close()
        rpmListWriter.close()
        directoryListWriter.close()
            
            
if __name__ == '__main__':
    main()
#!/usr/bin/env python

destinationFileName = "DirectoryList_"
fileIndex = 1
lineNumber = 0
limit = 1000000
sourceReader = open("C:\\dev\\2016.11\\work\\DirectoryList_Everything.txt", 'r')
destinationWriter = open("C:\\dev\\2016.11\\work\\"+destinationFileName+str(fileIndex)+".txt", 'a')

while True:
    line = sourceReader.readline()
    if line == '':
        break
    lineNumber += 1
    destinationWriter.write(line)
    if lineNumber == limit:
        fileIndex += 1
        destinationWriter.close()
        destinationWriter = open("C:\\dev\\2016.11\\work\\"+destinationFileName+str(fileIndex)+".txt", 'a')
        lineNumber = 0

destinationWriter.close()
print 'Complete'
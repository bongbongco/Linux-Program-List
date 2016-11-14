#!/usr/bin/env python
import re


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
    if (line[-6:] == ".html\n"
        or line[-6:] == ".conf\n"
        or line[-6:] == ".json\n"
        or line[-5:] == ".png\n"
        or line[-5:] == ".jpg\n"
        or line[-5:] == ".htm\n"
        or line[-5:] == ".gif\n"
        or line[-5:] == ".xml\n"
        or line[-5:] == ".css\n"
        or line[-5:] == ".txt\n"
        or line[-5:] == ".ico\n"
        or line[-5:] == ".jsp\n"
        or line[-5:] == ".jar\n"
        or line[-5:] == ".bat\n"
        or line[-5:] == ".cpp\n"
        or line[-5:] == ".ttf\n"
        or line[-5:] == ".pyc\n"
        or line[-5:] == ".pyo\n"
        or line[-5:] == ".crt\n"
        or line[-5:] == ".yml\n"
        or line[-5:] == ".xsl\n"
        or line[-5:] == ".log\n"
        or line[-5:] == ".bak\n"
        or line[-5:] == ".cmd\n"
        or line[-4:] == ".js\n"
        or line[-4:] == ".db\n"
        or line[-4:] == ".sh\n"
        or line[-4:] == ".py\n"
        or line[-4:] == ".gz\n"
        or line[-4:] == ".mo\n"
        or line[-4:] == ".so\n"
        or line[-4:] == ".pl\n"
        or line[-4:] == ".md\n"
        or line[-3:] == ".h\n"
        or line[-3:] == ".c\n"
        or line[-3:] == ".o\n"
        or re.match('.*/log/.*', line)
        or re.match('.*/logs/.*', line)
        or re.match('.*/bak/.*', line)
        or re.match('.*/bakup/.*', line)
        or re.match('.*/back/.*', line)
        or re.match('.*/backup/.*', line)
        or re.match('.*/upload/.*', line)
        or re.match('.*/image/.*', line)
        ):
            continue
    
    lineNumber += 1
    
    destinationWriter.write(line)
    if lineNumber == limit:
        fileIndex += 1
        destinationWriter.close()
        destinationWriter = open("C:\\dev\\2016.11\\work\\"+destinationFileName+str(fileIndex)+".txt", 'a')
        lineNumber = 0

destinationWriter.close()
print 'Complete'
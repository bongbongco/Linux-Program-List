#-*- coding: utf-8 -*-
#!/usr/bin/env python

import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


sourceReader = open("error.txt", 'r')
destinationWriter = open("result.txt", 'a')

lines = sourceReader.readlines()

for line in lines:
    objectInfo = re.compile('[\w|-][\w|-][\w|-][\w|-][\w|-][\w|-][\w|-][\w|-][\w|-][\w|-]\.*\s+\d+\s+\w+\s+\w+\s+\d+\s+\d\d\d\d-\d\d-\d\d\s\d\d:\d\d\s') # 파일/디렉터리 명 을 제외한 나머지 정보 제거
    line = objectInfo.sub('/', line)
    
    directoryTotal = re.compile(u'합계\s*\d*')
    resultLine = directoryTotal.sub('', unicode(line))
    
    print resultLine
    destinationWriter.write(resultLine)
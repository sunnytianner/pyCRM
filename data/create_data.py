#! /usr/bin/python

import xlrd
import re
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
import time

pattern1=re.compile('\s+')
pattern2=re.compile('[\\\\{}()<>?~_\',.:\@/$%&"`;]+')
pattern3=re.compile('--[-]*')
pattern4=re.compile('[\\\\{}()<>?~_\'.:\$@%&/"`;]+')
pattern5=re.compile('[\\\\{}<>~_\'\@/$%&`]+')
info = {}

def main():
    TrainingFile = open('TrainingData.xls','w')
    TargetFile = open('TargetData.xls','w')
    TrainingFile.write("title"+"\t"+"description"+"\t"+"annotation"+"\t"+"time"+"\t"+"author"+"\t"+"comment"+"\n")
    TargetFile.write("title"+"\t"+"description"+"\t"+"annotation"+"\t"+"time"+"\t"+"author"+"\t"+"comment"+"\n")
    
    load()
    
    num = -1
    wb = xlrd.open_workbook('a.xls')
    sh = wb.sheet_by_index(0)
    for rownum in range(sh.nrows):
        print rownum
        line = sh.row_values(rownum)
        number = line[0]
        title = line[1]
        annotation = line[3]

        str = ""
        title=title.lower()
        title=title.strip()
        title=pattern5.sub('',title)
        title=pattern3.sub('',title)
        title=pattern1.sub(' ',title)
        
        if(annotation == ''):
            if(number in info.keys()):
                str = title+"\t"+info[number]['description']+"\t"+annotation+"\t"+info[number]['date']+"\t"+info[number]['author']+"\t"+info[number]['comment']
            else:
                str = title+"\t"+""+"\t"+annotation+"\t"+""+"\t"+""+"\t"+""
            TargetFile.write(str+"\n")
            continue
    
        annotation=annotation.lower()
        annotation=annotation.strip()
        annotation_set = set(annotation.split(','))
        if('' in annotation_set):
            annotation_set.remove('')
        annotation_str = ""
        for annotation in annotation_set:
            annotation_str += pattern4.sub('',annotation.strip())+","
        annotation_str = annotation_str[:-1]
        
        if(title.strip()=="" or annotation_set==('')):
            continue
        num += 1
        if(number in info.keys()):
            str = title+"\t"+info[number]['description']+"\t"+annotation_str+"\t"+info[number]['date']+"\t"+info[number]['author']+"\t"+info[number]['comment']
        else:
            str = title+"\t"+""+"\t"+annotation_str+"\t"+""+"\t"+""+"\t"+""
        TrainingFile.write(str+"\n")

    TrainingFile.close()
    TargetFile.close()


def load():
  count = 1
  wb = xlrd.open_workbook('b.xls')
  sh = wb.sheet_by_index(0)
  for rownum in range(sh.nrows):
    print count
    count += 1
    line = sh.row_values(rownum)
    number = line[1]
    author = line[2].strip()
    description = line[3]
    date = line[4][7:].strip()
    if(description == ''):
      continue
    description = description.strip()
    description=pattern5.sub('',description)
    description=pattern3.sub('',description)
    description=pattern1.sub(' ',description)
    if(number not in info.keys()):
        info[number] = {}
        info[number]['author'] = author
        info[number]['description'] = description
        info[number]['date'] = date
        info[number]['comment'] = ""
    else:
        info[number]['comment'] += "[" + description + "];"

if __name__ == '__main__':
  main()


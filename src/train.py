from __future__ import division
import xlrd
import re
import cPickle
import math

def TrainModel(tfile,modelfile):
    pw,pt,linenum = GetPwPtAndLinenumber(tfile)
    idf = GetIdf(tfile)
    pd = GetPd(tfile,idf)
    
    cPickle.dump((pw,pt,idf,pd,linenum-1),open(modelfile,"wb"))


def GetPwPtAndLinenumber(tfile):
    TrainFile = open(tfile,"r")
    pw,pt = {},{}
    linenum = 1
    TrainFile.readline()
    line = TrainFile.readline()
    while line:
        line = line.split("\t")
        title = line[0]
        description = line[1]
        annotations = line[2]
        content = ContentCombine(title,description)
        content_dict,annotation_dict,content_size,annotation_size = GetCount(content,annotations)
        
        #for pw
        for w in content_dict.keys():
            if(pw.has_key(w) == False):
                pw[w]={0:0}
            pw[w][0] += 1
            pw[w][linenum] = content_dict[w]/(content_size+annotation_size)
        
        #for pt
        for t in annotation_dict.keys():
            if(pt.has_key(t) == False):
                pt[t]={0:0}
            pt[t][0] += 1
            pt[t][linenum] = annotation_dict[t]/(content_size+annotation_size)
        
        linenum += 1
    
        line = TrainFile.readline()
    
    #golbal value
    for w in pw.keys():
        pw[w][0] = pw[w][0] / linenum
    for t in pt.keys():
        pt[t][0] = pt[t][0] / linenum

    TrainFile.close()

    return pw,pt,linenum


def GetIdf(tfile):
    TrainFile = open(tfile,"r")
    idf = {}
    linenum = 1
    TrainFile.readline()
    line = TrainFile.readline()
    while line:
        line = line.split("\t")
        #for idf
        title = line[0]
        description = line[1]
        content = ContentCombine(title,description)
        for w in set(content.strip().split(" ")):
            if(idf.has_key(w) == False):
                idf[w]= 0
            idf[w] += 1
            
        linenum += 1
        line = TrainFile.readline()
        
    for word in idf:
        idf[word] = math.log(linenum/idf[word])

    TrainFile.close()

    return idf


def GetPd(tfile,idf):
    TrainFile = open(tfile,"r")
    pd = []
    pd.append(0)
    linenum = 1
    TrainFile.readline()
    line = TrainFile.readline()
    while line:
        line = line.split("\t")
        pd.append({})
        pd[linenum]['w'] = {}
        pd[linenum]['t'] = {}
        title = line[0]
        description = line[1]
        annotations = line[2]
        content = ContentCombine(title,description)
        content_dict,annotation_dict,content_size,annotation_size = GetCount(content,annotations)
        #for pd
        for w in content_dict.keys():
            pd[linenum]['w'][w] = content_dict[w] * idf[w]
            
        for t in annotation_dict.keys():
            pd[linenum]['t'][t] = annotation_dict[t] / annotation_size

        linenum += 1
        line = TrainFile.readline()

    TrainFile.close()

    return pd


def ContentCombine(title,description):
    pattern1 = re.compile('\s+')
    pattern2 = re.compile('[\\\\{}()<>?~_\',.:\@/$%&"`;]+')
    pattern3 = re.compile('--[-]*')
    pattern4 = re.compile('[\\\\{}()<>?~_\'.:\$@%&/"`;]+')

    title = title.lower().strip()
    title = pattern2.sub('',title)
    title = pattern3.sub('',title)

    description = description.lower().strip()
    description = pattern2.sub('',description)
    description = pattern3.sub('',description)

    return title + " " + description


def GetCount(content,annotations):
    content_dict,annotation_dict = {},{}
    content_words = content.strip().split(" ")
    annotation_words = annotations.strip().split(",")
    content_size = len(content_words)
    annotation_size = len(annotation_words)
    for content_word in content_words:
        if(content_dict.has_key(content_word) == False):
            content_dict[content_word] = 1
        else:
            content_dict[content_word] += 1
    for annotation_word in annotation_words:
        if(annotation_dict.has_key(annotation_word) == False):
            annotation_dict[annotation_word] = 1
        else:
            annotation_dict[annotation_word] += 1
    return content_dict,annotation_dict,content_size,annotation_size

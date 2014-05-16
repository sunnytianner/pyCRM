from __future__ import division
import sys
import cPickle
import math
from train import *
from predict import *

def Validate(vfile,modelfile,K,alpha,beta,gamma):
    title_validation,description_validation,annotation_validation,validation_size = ReadvalidationData(vfile)
    content_validation = GetContentList(title_validation,description_validation)
    pw,pt,idf,pd,train_linenum = ReadModel(modelfile)
    new_linenum = train_linenum + validation_size
    idf = GetNewIdf(idf,content_validation,train_linenum,new_linenum)
    print "load ok!"
  
    export_annotations=ExportAnnotations(pw,pt,pd,idf,train_linenum,content_validation,K,alpha,beta,gamma)
    target_annotation = []
    for target in annotation_validation:
        target = target.strip().split(",")
        target_annotation.append(target)
    accurancy,recall,f = Verify(export_annotations,target_annotation)
    print "accurancy = " + str(accurancy*100) + "%" + "\n" + "recall = " + str(recall*100) + "%" + "\n" + "f = " + str(f)


def ReadvalidationData(vfile):
    title_validation,description_validation,annotation_validation = [],[],[]
    validationFile = open(vfile,"r")
    validation_size = 0
    validationFile.readline()
    line = validationFile.readline()
    while line:
        line = line.split("\t")
        title_validation.append(line[0])
        description_validation.append(line[1])
        annotation_validation.append(line[2])
        validation_size += 1
        line = validationFile.readline()

    validationFile.close()
    return title_validation,description_validation,annotation_validation,validation_size


def Verify(result_set,target_set):
    result_total,target_total,acc_total = (0,0,0)
    for result,target in zip(result_set,target_set):
        result = set(result)
        target = set(target)
        result_total += len(result)
        if(len(target)>7):
            target_total += 7
        else:
            target_total += len(target)
        acc_total += len(result & target)
    #print str(result_total) + "\t" + str(target_total) + "\t" + str(acc_total)
    acc = acc_total/result_total
    recall = acc_total/target_total
    return acc , recall , 2*acc*recall/(acc+recall)

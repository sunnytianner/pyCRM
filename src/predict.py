from __future__ import division
import time
import sys
import cPickle
import math
from train import *

def Predict(pfile,modelfile,outfile,K,alpha,beta,gamma):
    title_predict,description_predict,predict_size = ReadPredictData(pfile)
    content_predict = GetContentList(title_predict,description_predict)
    pw,pt,idf,pd,train_linenum = ReadModel(modelfile)
    new_linenum = train_linenum + predict_size
    idf = GetNewIdf(idf,content_predict,train_linenum,new_linenum)
    print "load ok!"
  
    time_start = time.time()
    export_annotations=ExportAnnotations(pw,pt,pd,idf,train_linenum,content_predict,K,alpha,beta,gamma)
    time_end = time.time()

    print "Average time is " + str((time_end-time_start)/predict_size) + "s"
    print "Writing the result file..."

    ResultFile = open(outfile,"w")
    ResultFile.write("title"+"\t"+"description"+"\t"+"annotation"+"\n")

    for i in xrange(len(title_predict)):
        ResultFile.write(title_predict[i]+"\t"+description_predict[i]+"\t"+",".join(export_annotations[i])+"\n")

    ResultFile.close()
    print "The result file ok!"


def ReadPredictData(pfile):
    title_predict,description_predict = [],[]
    PredictFile = open(pfile,"r")
    predict_size = 0
    PredictFile.readline()
    line = PredictFile.readline()
    while line:
        line = line.split("\t")
        title_predict.append(line[0])
        description_predict.append(line[1])
        predict_size += 1
        line = PredictFile.readline()

    PredictFile.close()
    return title_predict,description_predict,predict_size


def GetContentList(title_predict,description_predict):
    content_predict = []
    for title,description in zip(title_predict,description_predict):
        content_predict.append(ContentCombine(title,description))

    return content_predict


def ReadModel(modelfile):
    if modelfile == None:
        modelfile = "model.pkl"

    return cPickle.load(open(modelfile,"r"))


def GetNewIdf(idf,content_predict,train_linenum,new_linenum):
    new_idf = {}
    for w in idf:
        new_idf[w] = train_linenum / (idf[w]*idf[w])

    for content in content_predict:
        for w in set(content.strip().split(" ")):
            if new_idf.has_key(w) == False:
                new_idf[w] = 0
            new_idf[w] += 1

    for word in new_idf:
        new_idf[word] = math.log(new_linenum/new_idf[word])

    return new_idf


def ExportAnnotations(pw,pt,pd,idf,linenum,content_predict,K,alpha,beta,gamma):
    export_annotations=[]
    num=1
    for content in content_predict:
        #print "Predicting the number " + str(num) + " feature request' annotations..."
        num += 1
        words = content.strip().split(" ")
        simi_linenum = GetKnn(words,idf,pd,linenum,gamma)
        annotations_wight = CalulateAnnotationsWeight(words,pw,pt,simi_linenum,alpha,beta)
        annotations = sorted(annotations_wight.keys(),key=lambda e:annotations_wight[e],reverse=True)
        if(K==0):
            export_annotations.append(annotations[0:])
        else:
            if(len(annotations)<K):
                export_annotations.append(annotations[0:])
            else:
                export_annotations.append(annotations[:K])
    return export_annotations


def GetKnn(words,idf,pd,linenum,gamma):
    knn = {}
    word_weight = CalulateWordsWeight(words,idf)
    for line in xrange(1,linenum+1):
        similarity = CosinSimilarity(word_weight,pd[line]['w'])
        knn[line] = similarity
    simi_linenum = list(sorted(knn.keys(),key=lambda e:knn[e],reverse=True))
    return simi_linenum[:gamma]


def CalulateAnnotationsWeight(words,pw,pt,linenum,alpha,beta):
    annotations_weight = {}
    for annotation in pt.keys():
        #print annotation
        annotations_weight[annotation] = 0
        for key in set(linenum) & set(pt[annotation].keys()):
            #print "line:" + str(key)
            if(key==0):
                continue
            if(pt[annotation].has_key(key)):
                product = (1-alpha)*pt[annotation][key] + alpha*pt[annotation][0]
            else:
                product = alpha*pt[annotation][0]
            for word in words:
                if(pw.has_key(word)==False):
                    #product *= beta * (1/knn_k)
                    product *= beta
                    continue
                if(pw[word].has_key(key)==False):
                    product *= beta * (pw[word][0])
                else:
                    product *= ((1-beta)*pw[word][key] + beta*pw[word][0])
            annotations_weight[annotation] += product
    
    return annotations_weight


def CalulateWordsWeight(words,idf):
    annotations_weight = {}
    for word in words:
        if(annotations_weight.has_key(word)==False):
            annotations_weight[word] = 0
        annotations_weight[word] += 1
    for word in annotations_weight.keys():
        annotations_weight[word] *= idf[word]
    return annotations_weight


def CosinSimilarity(word_weight,doucument_word):
    def Lenth(word_dict):
        lenth = 0
        for word in word_dict.keys():
            lenth += word_dict[word] ** 2
        lenth = math.sqrt(lenth)
        return lenth
    
    score = 0
    for word in word_weight:
        if(word in doucument_word):
            score += word_weight[word] * doucument_word[word]
    
    return score / (Lenth(word_weight) * Lenth(doucument_word))

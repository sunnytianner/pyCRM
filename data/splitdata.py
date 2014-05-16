#! /usr/bin/python

import sys
import random
import xlrd

#data is des and tags pair; M is copies of split,and M-1 is train and 1 is test;k is the number of nth exprience(0<=k<=M;seed is the control of expirence,if the seed is same,the exprience is in the same control)

if __name__ == '__main__':
    SourceFile = open(sys.argv[1],'r')
    TrainFile = open('Train.xls','w')
    ValidationFile = open('Validation.xls','w')

    M = 7
    k = 0
    seed = 327
    random.seed(seed)

    number = 1
    SourceFile.readline()
    line = SourceFile.readline()
    while line:
        print number
        if random.randint(0,M) == k:
            ValidationFile.write(line)
        else:
            TrainFile.write(line)

        line = SourceFile.readline()
        number += 1

    TrainFile.close()
    ValidationFile.close()


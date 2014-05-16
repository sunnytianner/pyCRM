#! /usr/bin/python

import sys
from train import *
from predict import *
from validation import *

MODEL_STATUS_UNKOWN = 0
MODEL_STATUS_RUN = 1
MODEL_STATUS_TRAIN = 2
MODEL_STATUS_PREDICT = 3
MODEL_STATUS_VALIDATION = 4

def main():
    model_status = MODEL_STATUS_UNKOWN
    tfile = ""
    pfile = ""
    vfile = ""
    outfile = "../result/result.xls"
    modelfile = "../model/model.pkl"
    K = 4
    alpha = 0.3
    beta = 0.8
    gamma = 50

    argv = sys.argv
    i = 1
    while i < len(argv):
        arg = argv[i]
        
        if arg == "-run":
            model_status = MODEL_STATUS_RUN

        elif arg == "-train":
            model_status = MODEL_STATUS_TRAIN

        elif arg == "-predict":
            model_status = MODEL_STATUS_PREDICT
        
        elif arg == "-validate":
            model_status = MODEL_STATUS_VALIDATION

        elif arg == "-tfile":
            i += 1
            tfile = argv[i]

        elif arg == "-pfile":
            i += 1
            pfile = argv[i]
        
        elif arg == "-vfile":
            i += 1
            vfile = argv[i]

        elif arg == "-outfile":
            i += 1
            outfile = argv[i]
        
        elif arg == "-modelfile":
            i += 1
            modelfile = argv[i]

        elif arg == "-K":
            i += 1
            K = argv[i]

        elif arg == "-alpha":
            i += 1
            alpha = argv[i]

        elif arg == "-beta":
            i += 1
            beta = argv[i]

        elif arg == "-gamma":
            i += 1
            gamma = argv[i]

        i += 1

    if model_status == MODEL_STATUS_UNKOWN:
        print("\nPlease specify the task you would like to perform (-run/-train/-predict/-validate)!")
        help()
        return 1

    elif model_status == MODEL_STATUS_RUN:
        if tfile == "":
            print("\nPlease specify the training data file for model training!")
            help()
            return 1
        elif pfile == "":
            print("\nPlease specify the predict data file for predicting!")
            help()
            return 1
        else:
            print "model_status:" + "RUN" + "\ttfile:" + tfile + "\tpfile:" + pfile + "\toutfile:" + outfile + "\tmodelfile:" + modelfile + "\tK:" + str(K) + "\talpha:" + str(alpha) + "\tbeta:"+ str(beta) + "\tgamma:" + str(gamma)
            print "train....."
            TrainModel(tfile,modelfile)
            print "predict..."
            Predict(pfile,modelfile,outfile,K,alpha,beta,gamma)

    elif model_status == MODEL_STATUS_TRAIN:
        if tfile == "":
            print("\nPlease specify the training data file for model training!")
            help()
            return 1
        else:
            print "model_status:" + "TRAIN" + "\ttfile:" + tfile + "\tpfile:" + pfile + "\toutfile:" + outfile + "\tmodelfile:" + modelfile + "\tK:" + str(K) + "\talpha:" + str(alpha) + "\tbeta:"+ str(beta) + "\tgamma:" + str(gamma)
            print "train....."
            TrainModel(tfile,modelfile)

    elif model_status == MODEL_STATUS_PREDICT:
        if pfile == "":
            print("\nPlease specify the predict data file for predicting!")
            help()
            return 1
        else:
            print "model_status:" + "PREDICT" + "\ttfile:" + tfile + "\tpfile:" + pfile + "\toutfile:" + outfile + "\tmodelfile:" + modelfile + "\tK:" + str(K) + "\talpha:" + str(alpha) + "\tbeta:"+ str(beta) + "\tgamma:" + str(gamma)
            print "predict..."
            Predict(pfile,modelfile,outfile,K,alpha,beta,gamma)

    elif model_status == MODEL_STATUS_VALIDATION:
        if vfile == "":
            print("\nPlease specify the validation data file for validating!")
            help()
            return 1
        else:
            print "model_status:" + "VALIDATION" + "\tvfile:" + vfile +  "\tmodelfile:" + modelfile + "\tK:" + str(K) + "\talpha:" + str(alpha) + "\tbeta:"+ str(beta) + "\tgamma:" + str(gamma)
            print "validating..."
            Validate(vfile,modelfile,K,alpha,beta,gamma)

    return 0

def help():
    print("Command line usage:\n")
    print("\tpython CRM.py -run -tfile <string> -pfile <string> -outfile <string>(default result.xls) -K <int>(default 4) -alpha <double>(default 0.3) -beta <double>(default 0.8) -gamma <int>(default 50)")
    print("\tpython CRM.py -train -tfile <string> -modelfile <string>(default model.pkl)")
    print("\tpython CRM.py -predict -pfile <string> -modelfile <string>(default model.pkl) -outfile <string>(default result.xls) -K <int>(default 4) -alpha <double>(default 0.3) -beta <double>(default 0.8) -gamma <int>(default 50)\n")
    print("\tpython CRM.py -validate -vfile <string> -modelfile <string>(default model.pkl) -K <int>(default 4) -alpha <double>(default 0.3) -beta <double>(default 0.8) -gamma <int>(default 50)\n")

if __name__=="__main__":
    sys.exit(main())

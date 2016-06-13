# -*- coding: utf-8 -*-
import numpy as np
from optparse import OptionParser
import sys
from time import time
import codecs
import os
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.externals import joblib

import stif_classifier_dataset as stif_data
import stif_nexterite_properties as stif



logger = stif.logger
data_dir = stif.data_dir
clf_dir = os.path.join(data_dir,'clf_serial')
clf_filename = 'stif_clf.pkl'
threshold_prob = 0.8

def write_predicted_alerts(file_name_ori, lines):
    return write_alerts(file_name_ori, '_PRED_ALERTS.out', lines)

def write_alerts(file_name_ori, prefix, lines):
    data_dir=stif.data_dir
    filename, file_extension = os.path.splitext(file_name_ori)
    filename_dest = os.path.join(data_dir, filename+ prefix)
    ftt = codecs.open(filename_dest, 'wb',encoding="utf-8")
    for line in lines:
        ftt.write(line)
    ftt.close()
    logger.info("%s %d"%(filename_dest,len(lines)))
    return filename+ prefix


def size_mb(docs):
    return sum(len(s.encode('utf-8')) for s in docs) / 1e6


def train_and_save(data_train,y):
    data_train_size_mb = size_mb(data_train)
    logger.info("%d documents - %0.3fMB (training set)" % (len(data_train), data_train_size_mb))
    logger.info("\n")
    clf = Pipeline([('tfidf', TfidfVectorizer(sublinear_tf=True, max_df=0.5,preprocessor=stif_data.preprocessor)), ('clf', RandomForestClassifier(n_estimators=300, n_jobs=-1))])
    logger.info('_' * 80)
    logger.info("Training: ")
    logger.info(clf)
    t0 = time()
    clf.fit(data_train, y)
    train_time = time() - t0
    logger.info("train time: %0.3fs" % train_time)
    joblib.dump(clf, os.path.join(clf_dir,clf_filename))

def predict(filename_ori,lines):
    clf = joblib.load(os.path.join(clf_dir,clf_filename))
    pred_proba = clf.predict_proba(lines)[:, 1]
    sorted_pred = [tuple((proba,lines[i])) for i,proba in enumerate(pred_proba)]
    sorted_pred = sorted(sorted_pred, key=lambda item: -item[0] )
    to_write = []
    for item in sorted_pred:
        to_write.append(str(item[0])+"\t"+item[1])
    return write_alerts(filename_ori, "PRED_PROBA.out", to_write)

def isAlert(clf, str, proba=threshold_prob):
    #dec_str=codecs.decode(bytes(str),encoding='utf-8')
    # s = bytes(str,"utf-8")
    # dec_str=s.decode('utf-8')
    # lines =[dec_str]
    pred_proba = clf.predict_proba([str])[:, 1]
    if pred_proba >= threshold_prob :
        return True
    return False

    logger.info("predict_proba : %f\t%s"% (pred_proba[0],str))

def select_proba_tweets(source,proba):
    lines = []
    with codecs.open(source, 'r',encoding='utf-8') as f:
        for line in f:
            m = re.match(r"(\d+\.\d+)\t(.*)$", line)
            if m != None:
                l_proba = float(m.group(1))
                text = m.group(2)
                if l_proba >= proba:
                    lines.append(text+'\n')
    return lines



if __name__ == '__main__' :
    # parse commandline arguments
    op = OptionParser()
    op.add_option("-c", "--classify",
                  action="store", dest="file_to_classify", default=None,
                  help="Classify with train classifier.")

    op.add_option("-t","--train",
                  action="store", dest="do_train", default=False,
                  help="Entrainement du classifier")

    (opts, args) = op.parse_args()
    if len(args) > 0:
        op.error("this script takes no arguments.")
        sys.exit(1)

    # print(__doc__)
    # op.print_help()
    # print()

    if opts.do_train :
        logger.info("Loading train tweets")
        stif_dataset = stif_data.StifDataSet(stif.data_labeled_dir,stif.data_not_labeled_dir)
        texts = np.hstack((stif_dataset.neg_texts,stif_dataset.pos_texts))
        y = np.ones(len(texts), dtype=np.int)
        y[:len(stif_dataset.neg_texts)] = 0.
        train_and_save(texts,y)
    elif opts.file_to_classify != None:
        with codecs.open(os.path.join(data_dir,opts.file_to_classify), 'r',encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        filename_dest = predict(opts.file_to_classify,lines)
        lines = select_proba_tweets(os.path.join(data_dir,filename_dest),threshold_prob)
        write_alerts(filename_dest, str(threshold_prob)+".out", lines)
    else:
        clf = joblib.load(os.path.join(clf_dir,clf_filename))
        test1="@franceinfo: #Incendie  #LaCourneuve : la reprise du trafic sur le #RERB entre Aulnay et la Gare du Nord repousse  la fin du service."
        tag="ALERTE"
        if isAlert(clf,test1)==False:
            tag = "NON "+tag
        logger.info("ALERTE %s"%(test1))





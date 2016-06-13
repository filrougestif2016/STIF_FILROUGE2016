# -*- coding: utf-8 -*-
import logging
import numpy as np
from optparse import OptionParser
import sys
from time import time


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
import stif_classifier_dataset
import stif_nexterite_properties
import stif_bench
import bm25_tfidf
import codecs
import os


logger = stif_nexterite_properties.logger

def size_mb(docs):
    return sum(len(s.encode('utf-8')) for s in docs) / 1e6

def transform_data(data):
    vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5,preprocessor=stif_classifier_dataset.preprocessor)
    return vectorizer.fit_transform(data)

def write_predicted_alerts(file_name_ori, lines):
    write_alerts(file_name_ori, '_PRED_ALERTS.out', lines)

def write_alerts(file_name_ori, prefix, lines):
    data_dir=stif_nexterite_properties.data_dir
    filename, file_extension = os.path.splitext(file_name_ori)
    filename_dest = os.path.join(data_dir, filename+ prefix)
    #ftt = codecs.open(filename_dest, 'wb',encoding="iso-8859-1")
    ftt = codecs.open(filename_dest, 'wb',encoding="utf-8")
    for line in lines:
        ftt.write(line)
    ftt.close()
    logger.info("%s %d"%(filename_dest,len(lines)))

def vectorizer_tfidf(data):
    vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5, preprocessor=stif_classifier_dataset.preprocessor)
    X = vectorizer.fit_transform(data)
    return vectorizer,X

def do_classify(data_train,y, data_test):
    vectorizer,X = vectorizer_tfidf(data_train)
    clf = RandomForestClassifier(n_estimators=300, n_jobs=-1)
    clf.fit(X,y)
    X_test = vectorizer.transform(data_test)
    y_pred=clf.predict(X_test)
    y_pred_proba = clf.predict_proba(X_test)[:, 1]

    return clf,y_pred,y_pred_proba

def bm25_vectorizer(data):
    vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5, preprocessor=stif_classifier_dataset.preprocessor)
    vectorizer._tfidf = bm25_tfidf.BM25Transformer(use_idf=True, k1=1.5, b=0.75)
    X = vectorizer.fit_transform(data)
    return vectorizer,X

def do_classify_bm25(data_train,y, data_test):
    t0 = time()
    vectorizer, X = bm25_vectorizer(data_train)
    v_time = time() - t0
    logger.info("bm25 vectorizer: %0.3fs" % v_time)
    clf = RandomForestClassifier(n_estimators=300, n_jobs=-1)
    logger.info('_' * 80)
    logger.info("classifier: ")
    logger.info(clf)
    t0 = time()
    clf.fit(X,y)
    train_time = time() - t0
    logger.info("train: %0.3fs" % train_time)
    t0 = time()

    X_test = vectorizer.transform(data_test)
    t_time = time() - t0
    logger.info("matrix test construction: %0.3fs" % t_time)
    t0 = time()
    y_pred=clf.predict(X_test)
    p_time = time() - t0
    logger.info("predict: %0.3fs" % p_time)
    t0 = time()

    y_pred_proba = clf.predict_proba(X_test)[:, 1]
    p_time = time() - t0
    logger.info("predict proba: %0.3fs" % p_time)

    return clf,y_pred,y_pred_proba

def classify(file_name_ori, data_train,y,data_test, bm25_code=False):
    data_train_size_mb = size_mb(data_train)
    data_test_size_mb = size_mb(data_test)
    logger.info("%d documents - %0.3fMB (training set)" % (len(data_train), data_train_size_mb))
    logger.info("%d documents - %0.3fMB (test set)" % (len(data_test), data_test_size_mb))
    logger.info("\n")
    if bm25_code:
        clf, pred, pred_proba = do_classify_bm25(data_train,y,data_test)
    else:
        #clf = Pipeline([('tfidf', TfidfVectorizer(sublinear_tf=True, max_df=0.5,preprocessor=stif_classifier_dataset.preprocessor)), ('clf', LinearSVC(loss='l2',penalty='l1',dual=False, tol=1e-3))])
        clf = Pipeline([('tfidf', TfidfVectorizer(sublinear_tf=True, max_df=0.5,preprocessor=stif_classifier_dataset.preprocessor)), ('clf', RandomForestClassifier(n_estimators=300, n_jobs=-1))])
        #clf=LinearSVC(loss='l2',penalty='l1',dual=False, tol=1e-3)
        logger.info('_' * 80)
        logger.info("Training: ")
        logger.info(clf)
        t0 = time()
        #X_train = transform_data(data_train)
        clf.fit(data_train, y)
        train_time = time() - t0
        logger.info("train time: %0.3fs" % train_time)

       # X_test = transform_data(data_tests)
        pred = clf.predict(data_test)
        pred_proba = clf.predict_proba(data_test)[:, 1]


    indices = np.argwhere(pred==1)
    logger.info("%d classified as alerts" % (len(indices)))

    result = [data_test[i] for i in indices]
    write_predicted_alerts(file_name_ori, result)

    sorted_pred = [tuple((proba,data_test[i])) for i,proba in enumerate(pred_proba)]
    sorted_pred = sorted(sorted_pred, key=lambda item: -item[0] )
    to_write = []
    for item in sorted_pred:
        to_write.append(str(item[0])+"\t"+item[1])

    #sorted_pred = [item[0]+"\t"+item[1] for item in sorted_pred]
    write_alerts(file_name_ori, "PRED_PROBA.out", to_write)


if __name__ == '__main__' :
    op = OptionParser()
    op.add_option("--report",
                  action="store_true", dest="print_report",
                  help="Print a detailed classification report.")
    op.add_option("--chi2_select",
                  action="store", type="int", dest="select_chi2",
                  help="Select some number of features using a chi-squared test")
    op.add_option("--confusion_matrix",
                  action="store_true", dest="print_cm",
                  help="Print the confusion matrix.")
    op.add_option("--top10",
                  action="store_true", dest="print_top10",
                  help="Print ten most discriminative terms per class"
                       " for every classifier.")
    op.add_option("--use_hashing",
                  action="store_true",
                  help="Use a hashing vectorizer.")
    op.add_option("--n_features",
                  action="store", type=int, default=2 ** 16,
                  help="n_features when using the hashing vectorizer.")
    op.add_option("--filtered",
                  action="store_true",
                  help="Remove newsgroup information that is easily overfit: "
                       "headers, signatures, and quoting.")
    op.add_option("-c", "--classify",
                  action="store", dest="file_to_classify", default=None,
                  help="Classify with linearSVC L1 (best score).")

    op.add_option("--bm25",
                  action="store", dest="bm25_code", default=False,
                  help="Remplacer le tf-idf par codification BM25")

    (opts, args) = op.parse_args()
    if len(args) > 0:
        op.error("this script takes no arguments.")
        sys.exit(1)

    print(__doc__)
    op.print_help()
    print()

    logger.info("Loading tweets")
    stif_dataset = stif_classifier_dataset.StifDataSet(stif_nexterite_properties.data_labeled_dir,stif_nexterite_properties.data_not_labeled_dir)
    texts = np.hstack((stif_dataset.neg_texts,stif_dataset.pos_texts))
    y = np.ones(len(texts), dtype=np.int)
    y[:len(stif_dataset.neg_texts)] = 0.
    if opts.file_to_classify != None:
        data_dir = stif_nexterite_properties.data_dir
        with codecs.open(os.path.join(data_dir,opts.file_to_classify), 'r',encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        if opts.bm25_code:
            classify(opts.file_to_classify,texts,y,lines,True)
        else:
            classify(opts.file_to_classify,texts,y,lines,False)

    else:
        stif_bench.bench(texts,y,opts)

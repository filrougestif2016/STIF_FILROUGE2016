# -*- coding: utf-8 -*-
import os
import codecs
import re
from optparse import OptionParser
from text_to_bag_of_words import transform_line
from glob import glob
import random
import numpy as np
from sklearn.cross_validation import cross_val_score
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier
from sklearn.grid_search import GridSearchCV
from sklearn.cross_validation import train_test_split
from optparse import OptionParser
import stif_nexterite_properties as stif

logger = stif.logger

class StifDataSet(object):
     def __init__(self, dir_pos, dir_neg):
        filenames_pos = sorted(glob(os.path.join(dir_pos, '*.out')))
        logger.debug("%d files labeled"%len(filenames_pos))
        self.pos_texts =[]
        self.neg_texts = []
        for ipos,fpos in enumerate(filenames_pos):
            logger.debug("%d %s file "%(ipos,fpos))
            texts_pos = open(fpos).readlines()
            basename = os.path.basename(fpos)
            date = basename.split('_')[-1].replace('.out','')
            filenames_neg = sorted(glob(os.path.join(dir_neg, '*'+date+'.out')))
            texts_neg = []
            logger.debug("%d files not_labeled"%len(filenames_neg))
            for fneg in filenames_neg:
                texts_neg = np.hstack((texts_neg,open(fneg).readlines()))
            if len(texts_neg) > len(texts_pos):
                random.shuffle(texts_neg)
                texts_neg = texts_neg[:len(texts_pos)]
            self.pos_texts=np.hstack((self.pos_texts,texts_pos))
            self.neg_texts=np.hstack((self.neg_texts,texts_neg))


def compute_score(clf, X,y):
    xval = cross_val_score(clf,X,y,cv=5)
    return np.mean(xval)

def preprocessor(data):
        return " ".join(transform_line(data))

def findOptSVM(texts,y ):
    vect = CountVectorizer(preprocessor=preprocessor)
    tfidf = TfidfTransformer()
    #svc = SGDClassifier()
    svc = LinearSVC()

    vX = vect.fit_transform(texts)
    tfidfX = tfidf.fit_transform(vX)
    X_train,X_test,y_train,y_test = train_test_split(tfidfX,y,test_size=0.33,random_state=42)
    accuracyArr = []
    cRange = np.logspace(-5,5,10)
    for c in cRange:
        #svc.alpha = c
        svc.C = c
        svc.fit(X_train,y_train)
        accuracyArr.append(svc.score(X_test,y_test))

    C_opt = cRange[np.argmax(accuracyArr)]
    return C_opt


def test_classification(texts,y):
    N = len(texts)
    logger.info("%d documents" % N)

    text_clf = Pipeline([('vect', CountVectorizer()),('tfidf', TfidfTransformer()), ('clf', MultinomialNB())])
    text_clf.set_params(vect__preprocessor=preprocessor)
    score = compute_score(text_clf,texts,y)
    logger.info('Naive Bayes, score  : %f' % score)
    text_clf = Pipeline([('vect', CountVectorizer()),('tfidf', TfidfTransformer()), ('clf', LogisticRegression())])
    text_clf.set_params(vect__preprocessor=preprocessor)
    score = compute_score(text_clf,texts,y)
    logger.info('LogisticRegression, score  : %f' % score)
    text_clf = Pipeline([('vect', CountVectorizer()),('tfidf', TfidfTransformer()), ('clf', LinearSVC(C=0.278256))])
    text_clf.set_params(vect__preprocessor=preprocessor)
    score = compute_score(text_clf,texts,y)
    logger.info('SVM, score  : %f' % score)
    text_clf = Pipeline([('vect', CountVectorizer()),('tfidf', TfidfTransformer()), ('clf', SGDClassifier(alpha=0.000129))])
    text_clf.set_params(vect__preprocessor=preprocessor)
    score = compute_score(text_clf,texts,y)
    logger.info('SVM bis, score  : %f' % score)

    logger.info('SVM C_opt=%f' % findOptSVM(texts,y))

    logger.info("STIF CLASSIFIER END")

def size_mb(docs):
    return sum(len(s.encode('utf-8')) for s in docs) / 1e6


if __name__ == '__main__' :
    logger.info("STIF CLASSIFIER START")
    stif_dataset = StifDataSet(stif.data_labeled_dir,stif.data_not_labeled_dir)
    texts = np.hstack((stif_dataset.neg_texts,stif_dataset.pos_texts))
    y = np.ones(len(texts), dtype=np.int)
    y[:len(stif_dataset.neg_texts)] = 0.

    op = OptionParser()
    op.add_option("-c", "--classification",
                  action="store_false", dest="classification",
                  help="Effectuer un test de classification")
    (opts, args) = op.parse_args()
    if  opts.classification:
        test_classification(texts,y)
    else:
        logger.info("Nombre de tweets identifiés comme alertes %d"%len(stif_dataset.pos_texts))
        logger.info("Nombre de tweets non identifiés %d"%len(stif_dataset.neg_texts))
        data_train,data_test,y_train,y_test = train_test_split(texts,y,test_size=0.33,random_state=42)

        data_train_size_mb = size_mb(data_train)
        data_test_size_mb = size_mb(data_test)

        logger.info("%d documents - %0.3fMB (training set)" % (
            len(data_train), data_train_size_mb))
        logger.info("%d documents - %0.3fMB (test set)" % (
            len(data_test), data_test_size_mb))
        logger.info("\n")

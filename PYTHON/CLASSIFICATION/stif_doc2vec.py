# -*- coding: utf-8 -*-
import sys
from optparse import OptionParser
from gensim.models.doc2vec import TaggedDocument
from gensim.models import Doc2Vec
import os.path
import numpy
import codecs
from random import shuffle
from sklearn.linear_model import LogisticRegression
from text_to_bag_of_words import transform_line
import six
import stif_classifier_dataset
import stif_nexterite_properties
import numpy as np
from sklearn.svm import LinearSVC

logger = stif_nexterite_properties.logger


class LabeledLineSentence(object):
    def __init__(self, sources):
        self.sources = sources

        flipped = {}

        # make sure that keys are unique
        for key, value in sources.items():
            if value not in flipped:
                flipped[value] = [key]
            else:
                raise Exception('Non-unique prefix encountered')

    def __iter__(self):
        for source, prefix in self.sources.items():
            with codecs.open(source, 'r',encoding='iso-8859-1') as fin:
#            with utils.smart_open(source) as fin:
                for item_no, line in enumerate(fin):
                    #yield TaggedDocument(utils.to_unicode(line).split(), [prefix + '_%s' % item_no])
                    yield TaggedDocument(self.splitLine(line), [prefix + '_%s' % item_no])

    def to_array(self):
        self.sentences = []
        for source, prefix in self.sources.items():
            with codecs.open(source, 'r',encoding='iso-8859-1') as fin:
#            with utils.smart_open(source) as fin:
                for item_no, line in enumerate(fin):
                    #self.sentences.append(TaggedDocument(utils.to_unicode(line).split(), [prefix + '_%s' % item_no]))
                    self.sentences.append(TaggedDocument(self.splitLine(line), [prefix + '_%s' % item_no]))
        return self.sentences

    def sentences_perm(self):
        shuffle(self.sentences)
        return self.sentences

    def splitLine(self,line):
        return(transform_line(line))



class Doc2Vec_Model(object):
    def __init__(self,sources, model_name):
        self.sources=sources
        if os.path.isfile(model_name) is False:
            sentences = LabeledLineSentence(sources)
            #self.model = Doc2Vec(min_count=1, window=10, size=1000, sample=1e-4, negative=5, workers=4, alpha=0.025, min_alpha=0.025)
            #self.model = Doc2Vec(size=1000, window=2, min_count=1, workers=4,alpha=0.025, min_alpha=0.025, dm=0)
            self.model = Doc2Vec(size=10000, window=2, min_count=1, workers=4, dm=0)
            #self.model = Doc2Vec(size=1000, window=2, min_count=1, workers=4,alpha=0.025, min_alpha=0.025, dm=0, dm_concat=1)
            self.model.build_vocab(sentences.to_array())

            for epoch in range(20):
                self.model.train(sentences.sentences_perm())
                # self.model.alpha -= 0.002  # decrease the learning rate
                # self.model.min_alpha = self.model.alpha  # fix the learning rate, no decay

            self.model.save(model_name)
        self.model = Doc2Vec.load(model_name)

    def get_similarities(self,line):
        line_vec = self.model.infer_vector(transform_line(line))
        return self.model.docvecs.most_similar([line_vec],topn=self.model.docvecs.count)


    def get_line(self,i):
        filename = six.next(six.iterkeys(self.sources))
        return open(filename, "r").readlines()[i]

    def fit_matrix(self, size, posOrNeg, offset=0):
        value = 1
        _offset = 0
        if posOrNeg == 'NEG':
            value = 0
            _offset = offset
        for i in range(size):
            prefix_test_pos = posOrNeg+'_' + str(i)
            #test_arrays[i] = self.model[prefix_test_pos]
            self.X[_offset+i] = self.model.docvecs.doctag_syn0[self.model.docvecs.doctags[prefix_test_pos].offset]
            self.Y[_offset+i] = value

    def set_matrix(self, posLen,negLen):
        len = posLen+negLen
        self.X = numpy.zeros((len, self.model.vector_size))
        self.Y = numpy.zeros(len)
        self.fit_matrix(posLen,'POS',offset=0)
        self.fit_matrix(negLen,'NEG',offset=posLen)

    def infer_matrix(self, lines):
        infered_matrix = numpy.zeros((len(lines), self.model.vector_size))
        for i, line in enumerate(lines):
            preprocessed_line = transform_line(line)
            infered_matrix[i, :] = self.model.infer_vector(preprocessed_line)
        return infered_matrix


def write_lines_file(fileName, lines):
     file_output = codecs.open(fileName, 'w', 'utf-8')
     file_output.writelines(lines)
     file_output.close()


if __name__ == '__main__' :
    op = OptionParser()
    op.add_option("-c", "--classify",
              action="store", dest="file_to_classify", default=None,
              help="Classify .")
    (opts, args) = op.parse_args()
    if len(args) > 0:
        op.error("this script takes no arguments.")
        print(__doc__)
        op.print_help()
        sys.exit(1)
    if opts.file_to_classify != None:
        data_dir = stif_nexterite_properties.data_dir
        with codecs.open(os.path.join(data_dir,opts.file_to_classify), 'r',encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        logger.info("Loading tweets")
        stif_dataset = stif_classifier_dataset.StifDataSet(stif_nexterite_properties.data_labeled_dir,stif_nexterite_properties.data_not_labeled_dir)
        data_dir=stif_nexterite_properties.data_dir
        pos_filename = os.path.join(data_dir, "pos_tweets.out")
        neg_filename = os.path.join(data_dir, "neg_tweets.out")
        write_lines_file(pos_filename,stif_dataset.pos_texts)
        write_lines_file(neg_filename,stif_dataset.neg_texts)

        sources = {pos_filename : 'POS', neg_filename : 'NEG' }
        model_name = os.path.join(data_dir, 'stif.d2v')
        logger.info("Training model")
        model = Doc2Vec_Model(sources, model_name)
        model.set_matrix(len(stif_dataset.pos_texts),len(stif_dataset.neg_texts))

        logger.info("Test logistic Regression")
        #classifier = LinearSVC(loss='l2',penalty='l1',dual=False, tol=1e-3)
        classifier = LogisticRegression()
        classifier.fit(model.X, model.Y)
        # LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,
        #                 intercept_scaling=1, penalty='l2', random_state=None, tol=0.0001)
        LogisticRegression()
        pred = classifier.predict(model.infer_matrix(lines))
        indices = np.argwhere(pred==1)
        logger.info("%d classified as alerts" % (len(indices)))
        result = [lines[i] for i in indices]
        result_filename = os.path.join(data_dir,'stif_doc2vec_pred.txt')
        write_lines_file(result_filename,result)

        # y_pred = classifier.predict_proba(model.infer_matrix(lines))[:, 1]
        # logger.info(result_filename)



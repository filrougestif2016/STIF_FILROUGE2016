# -*- coding: utf-8 -*-
from gensim import corpora
import codecs
import math
from text_to_bag_of_words import transform_line, words_have_stif_hashtag
import stif_nexterite_properties
import os
from optparse import OptionParser


logger = stif_nexterite_properties.logger

class BM25 :
    def __init__(self, fn_docs, encoding='iso-8859-1' ) :
        self.encoding = encoding
        self.dictionary = corpora.Dictionary()
        self.DF = {}
        self.DocTF = []
        self.DocIDF = {}
        self.N = 0
        self.DocAvgLen = 0
        self.fn_docs = fn_docs
        self.DocLen = []
        self.buildDictionary()
        self.TFIDF_Generator()

    def buildDictionary(self) :
        raw_data = []
        with codecs.open(self.fn_docs,encoding=self.encoding) as f:
            for line in f :
                raw_data.append(transform_line(line))
        self.dictionary.add_documents(raw_data)

    def TFIDF_Generator(self, base=math.e) :
        docTotalLen = 0
        with codecs.open(self.fn_docs,encoding=self.encoding) as f:
            for line in f :
                doc = transform_line(line.strip())
                docTotalLen += len(doc)
                self.DocLen.append(len(doc))
                #print self.dictionary.doc2bow(doc)
                bow = dict([(term, freq*1.0/len(doc)) for term, freq in self.dictionary.doc2bow(doc)])
                for term, tf in bow.items() :
                    if term not in self.DF :
                        self.DF[term] = 0
                    self.DF[term] += 1
                self.DocTF.append(bow)
                self.N = self.N + 1
        for term in self.DF:
            self.DocIDF[term] = math.log((self.N - self.DF[term] +0.5) / (self.DF[term] + 0.5), base)
        self.DocAvgLen = docTotalLen / self.N

    def BM25Score(self, Query=[], k1=1.5, b=0.75) :
        query_bow = self.dictionary.doc2bow(Query)
        scores = []
        for idx, doc in enumerate(self.DocTF) :
            commonTerms = set(dict(query_bow).keys()) & set(doc.keys())
            tmp_score = []
            doc_terms_len = self.DocLen[idx]
            for term in commonTerms :
                upper = (doc[term] * (k1+1))
                below = ((doc[term]) + k1*(1 - b + b*doc_terms_len/self.DocAvgLen))
                tmp_score.append(self.DocIDF[term] * upper / below)
            scores.append(sum(tmp_score))
        return scores

    def TFIDF(self) :
        tfidf = []
        for doc in self.DocTF :
            doc_tfidf  = [(term, tf*self.DocIDF[term]) for term, tf in doc.items()]
            doc_tfidf.sort()
            tfidf.append(doc_tfidf)
        return tfidf

    def Text_line(self,i):
        return open(self.fn_docs, "r").readlines()[i]

    def Items(self) :
        # Return a list [(term_idx, term_desc),]
        items = self.dictionary.items()
        #items.sort()
        return items

def do_write_bm25_similarity_files(idate,filename1, filename2):
        data_dir = stif_nexterite_properties.data_dir
        bm25 = BM25(filename1)
        with codecs.open(filename2, 'r',encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        iname = "bm25_alerts_"+idate
        ftt = codecs.open(os.path.join(data_dir,stif_nexterite_properties.label_name, iname+".out"), 'wb','utf-8')
        fnt = codecs.open(os.path.join(data_dir,stif_nexterite_properties.not_label_name, "no_"+iname+".out"), 'wb','utf-8')
        il=0
        inl=0
        for line in lines:
            words = transform_line(line)
            scores = bm25.BM25Score(words)
            best_score = max(scores)
            if best_score > stif_nexterite_properties.bm25_seuil:
                ftt.write(line)
                il += 1
                #ftt.write("****Best match %f\t%s"%(best_score,bm25.Text_line(i_line)))
            else:
                if not words_have_stif_hashtag(words):
                    fnt.write(line)
                    inl += 1
                    #fnt.write("****Best match %f\t%s"%(best_score,bm25.Text_line(i_line)))
        ftt.close()
        fnt.close()
        logger.info("%s %d"%(iname,il))
        logger.info("%s %d"%("no_"+iname,inl))

def write_bm25_similarity_files(idate,data_dir=stif_nexterite_properties.data_dir,data_impact_dir=stif_nexterite_properties.data_impact_dir,label_dir=stif_nexterite_properties.label_name,pre_dir=stif_nexterite_properties.pre_name):
        impact_filename = os.path.join(data_impact_dir, 'IMPACT_'+idate.replace('.','-')+'.csv')
        bm25 = BM25(impact_filename)
        infilename = os.path.join(data_dir, label_dir,pre_dir,'alerts_'+idate+'.out')
        do_write_bm25_similarity_files(idate,impact_filename,infilename)


if __name__ == '__main__' :
    op = OptionParser()
    op.add_option("-d", "--date",
                  action="store", dest="sel_date", default=None,
                  help="Date de sélection")
    op.add_option("--src",
                  action="store", dest="source", default=None,
                  help="Date de sélection")
    op.add_option("--target",
                  action="store", dest="target", default=None,
                  help="Date de sélection")
    (opts, args) = op.parse_args()
    if  opts.sel_date!=None:
        if opts.source == None:
            write_bm25_similarity_files(opts.sel_date)
        elif opts.target != None:
            do_write_bm25_similarity_files(opts.sel_date,os.path.join(stif_nexterite_properties.data_dir,opts.source),os.path.join(stif_nexterite_properties.data_dir,opts.target))



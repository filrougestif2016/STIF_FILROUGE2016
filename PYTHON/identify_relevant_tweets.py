# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch
import re
from gensim.models import Word2Vec
from nltk.corpus import stopwords
import pystache
import json
from datetime import timedelta, datetime
import traceback
from gensim import corpora
import math
import itertools
import numpy as np
import identify_properties
import time

"""
Différences BM25/TF-IDF :
https://www.elastic.co/blog/found-similarity-in-elasticsearch
"""


class BM25:

    def __init__(self, fn_docs, delimiter='|'):
        self.dictionary = corpora.Dictionary()
        self.DF = {}
        self.delimiter = delimiter
        self.DocTF = []
        self.DocIDF = {}
        self.N = 0
        self.DocAvgLen = 0
        self.fn_docs = fn_docs
        self.DocLen = []
        self.buildDictionary()
        self.TFIDF_Generator()

    def buildDictionary(self):
        # raw_data = []
        # for line in file(self.fn_docs):
        #     raw_data.append(line.strip().split(self.delimiter))
        self.dictionary.add_documents(self.fn_docs)

    def TFIDF_Generator(self, base=math.e):
        docTotalLen = 0
        for doc in self.fn_docs:
            # doc = line.strip().split(self.delimiter)
            docTotalLen += len(doc)
            self.DocLen.append(len(doc))
            #print self.dictionary.doc2bow(doc)
            bow = dict([(term, freq*1.0/len(doc)) for term, freq in self.dictionary.doc2bow(doc)])
            for term, tf in bow.items():
                if term not in self.DF:
                    self.DF[term] = 0
                self.DF[term] += 1
            self.DocTF.append(bow)
            self.N = self.N + 1
        for term in self.DF:
            self.DocIDF[term] = math.log((self.N - self.DF[term] +0.5) / (self.DF[term] + 0.5), base)
        self.DocAvgLen = docTotalLen / self.N

    def BM25Score(self, Query=[], k1=1.5, b=0.75):
        query_bow = self.dictionary.doc2bow(Query)
        scores = []
        for idx, doc in enumerate(self.DocTF):
            commonTerms = set(dict(query_bow).keys()) & set(doc.keys())
            tmp_score = []
            doc_terms_len = self.DocLen[idx]
            for term in commonTerms:
                upper = (doc[term] * (k1+1))
                below = ((doc[term]) + k1*(1 - b + b*doc_terms_len/self.DocAvgLen))
                tmp_score.append(self.DocIDF[term] * upper / below)
            scores.append(sum(tmp_score))
        return scores

    def TFIDF(self):
        tfidf = []
        for doc in self.DocTF:
            doc_tfidf = [(term, tf*self.DocIDF[term]) for term, tf in doc.items()]
            doc_tfidf.sort()
            tfidf.append(doc_tfidf)
        return tfidf

    def Items(self):
        # Return a list [(term_idx, term_desc),]
        items = self.dictionary.items()
        items.sort()
        return items


class ESHandler:

    def __init__(self, **kwargs):
        """
        :param kwargs:
         host : elastic search target host (default is localhost)
         port : elastic search target port (default is 9200)
         pg_size : read bloc size for large select queries (default is 1000)
        :return:
         None
        """
        self.host = 'localhost'
        if 'host' in kwargs.keys():
            self.host = kwargs['host']
        self.port = 9200
        if 'port' in kwargs.keys():
            self.port = int(kwargs['port'])
        self.pg_size = 1000
        if 'page_size' in kwargs.keys():
            self.pg_size = int(kwargs['pg_size'])
        # connect
        self.es = Elasticsearch([{'host': self.host, 'port': self.port}])


    def select_all(self, index_name, query):
        """
        Select all data matching with the given query
        :param index_name: index to browse
        :param query: lucene query to apply
        :return: list of hits
        """
        print "select_all - index_name="+index_name
        res = self.es.search(index=index_name, body=query, size=self.pg_size, from_=0, request_timeout=180)
        i = 1
        data = []
        while len(res[u'hits'][u'hits']) == self.pg_size:
            data.extend(res[u'hits'][u'hits'])
            res = self.es.search(index=index_name, body=query, size=self.pg_size, from_=i*self.pg_size, request_timeout=180)
            i += 1
        if len(res[u'hits'][u'hits']) > 0:
            data.extend(res[u'hits'][u'hits'])
        return data


    def select_page(self, index_name, query, pg_number):
        """
        Select a specific page of data matching with the given query
        :param index_name: index to browse
        :param query: lucene query to apply
        :param pg_number: number of page of data to get (should start at 0)
        :return: list of hits
        """
        print "select_page - index_name="+index_name+", page_number="+str(pg_number)
        try:
            data = []
            if self.es.indices.exists(index_name):
                res = self.es.search(index=index_name, body=query, size=self.pg_size, from_=pg_number*self.pg_size, request_timeout=180)
                if len(res[u'hits'][u'hits']) > 0:
                    data.extend(res[u'hits'][u'hits'])
        except:
            traceback.print_exc()
            pass
        return data



class InfoTrafic:

    def preprocessing_stif_tags(self, data):
        data = data.replace("#", '').lower()
        data = data.replace("en ligne", '')
        data = data.replace("hors ligne", '')
        data = data.replace("hors fixe", '')
        data = data.replace(u'ligne téléphonique', '')
        moyens = ['rer', 'ligne', 'ter', u'métro', 'metro', 't', 'tram', 'bus']
        lignes = ['a', 'b', 'c', 'd', 'e', 'h', 'k', 'j', 'p', 'r', 'u',
                  '1', '2', '3', '3bis', '4', '5', '6', '7', '7bis', '8', '9', '10', '11', '12', '13', '14']
        for i in itertools.product(moyens, lignes):
            data = data.replace(i[0]+' '+i[1], i[0]+i[1])
            data = data.replace(' '+i[0]+i[1]+'_', ' '+i[0]+i[1]+' ')
        data = re.findall("\w+", data, re.UNICODE)
        return data

    def clean_info_trafic(self, data):
        """
        To clean info trafic data
        :param data:
        :return:
        """
        TAG_RE = re.compile(r'<[^>]+>')
        data['texte'] = TAG_RE.sub('', data['texte'])
        for f in ['titre', 'texte', 'description']:
            data[f] = unicode(data[f])
            data[f] = data[f].lower()
            data[f] = data[f].replace('\n', ' ')
            data[f] = data[f].replace('\t', ' ')
            data[f] = data[f].replace('[ ]*', ' ')

    def convert_2_date(self, data):
        """
        Convert pub_date field to datetime type
        :param data:
        :return:
        """
        data['pub_date'] = datetime.strptime(data['pub_date'], "%a, %d %b %Y %H:%M:%S")

    def get_last_date(self):
        """
        Read the date of the last message taken into account among messages provided by STIF RSS feed
        :return:
        """
        if identify_properties.last_date is not None:
            return datetime.strptime(identify_properties.last_date, "%a, %d %b %Y %H:%M:%S")
        else:
            return None

    def filter_data_from_last_date(self):
        """
        Build a list with the messages to deal with (date greater than last_date parameter)
        :return:
        """
        if self.last_date is not None:
            return filter(lambda x: x['pub_date'] > self.last_date, self.es_data)
        else:
            return self.es_data

    def record_last_date(self):
        """
        Write the date of the last message taken into account among messages provided by STIF RSS feed
        :return:
        """
        f = open('identify_properties.py', 'w')
        f.write('# -*- coding: utf-8 -*-\n')
        f.write('last_date="')
        f.write(self.max_date.strftime("%a, %d %b %Y %H:%M:%S"))
        f.write('"\n')
        f.close()

    def __init__(self, es_cnx, it_index):
        """
        Constructor : set ElasticSearch connection handler and info_trafic index
        :param es_cnx: ElasticSearch connection handler
        :param it_index: info_trafic index
        :return:
        """
        self.query_all = {
            "query": {
                "match_all": {}
            }
        }
        self.cnx = es_cnx
        self.es_index = it_index
        self.es_data = cnx.select_all("stif_info_trafic", query_all)
        self.es_data = map(lambda x: x['_source'], self.es_data)
        self.max_date = None
        self.last_date = self.get_last_date()
        map(self.clean_info_trafic, self.es_data)
        map(self.convert_2_date, self.es_data)
        if len(self.es_data) > 0:
            self.max_date = max(self.es_data, key=lambda x: x['pub_date'])['pub_date']
        self.last_messages = self.filter_data_from_last_date()
        self.stops = set(stopwords.words("french"))
        self.corpus = None

    def __iter__(self):
        for d in self.es_data:
            for f in ['titre', 'description', 'texte']:
                data = self.preprocessing_stif_tags(d[f])
                yield [w for w in data if not w in self.stops]

    def get_corpus(self):
        if self.corpus is None:
            self.corpus = []
            for d in self.last_messages:
                for f in ['titre', 'description', 'texte']:
                    data = self.preprocessing_stif_tags(d[f])
                    self.corpus.append([w for w in data if not w in self.stops])
        return self.corpus


    def word2vec(self):
        self.model_word2vec = Word2Vec(self)

    def bm25(self):
        self.model_bm25 = BM25(self.get_corpus(), delimiter=' ')

    def similarity_word2vec(self, doc1, doc2):
        doc1 = doc1.lower()
        doc2 = doc2.lower()
        sentence1 = self.preprocessing_stif_tags(doc1)
        sentence2 = self.preprocessing_stif_tags(doc2)
        sentence1 = [w for w in sentence1 if w in self.model_word2vec.index2word]
        sentence2 = [w for w in sentence2 if w in self.model_word2vec.index2word
                     and 'http' not in w and w != 'RT']
        res = 0
        if len(sentence2) > 0:
            res = self.model_word2vec.n_similarity(sentence1, sentence2)
        return res



class TweetBrowser:

    def __init__(self, es):
        """
        Constructor
        :param es: ElasticSearch handler
        :return:
        """
        self.es = es
        self.query_sel_tweets = '{ \
            "fields": ["_source"], \
             "query": { \
                "bool": { \
                  "must": [ \
                    { \
                      "match": { \
                        "user.time_zone": "Paris" \
                      } \
                    }, \
                   { \
                   "range": { \
                         "created_at": { \
                           "gte": "{{dt_min}}", \
                           "lte": "{{dt_max}}", \
                           "format": "yyyyMMddHHmmss" \
                         } \
                       } \
                   } \
                   ] \
                } \
              } \
            }'

        self.index_settings = {
            "settings": {
            "number_of_shards": 5,
            "number_of_replicas": 0,
            }
        }


    def get_bounds_dates(self, date_time, margin):
        """
        Define an interval around a given date
        :param date_time: given date
        :param margin: margin in hours for the interval
        :return:
        """
        index_date1 = date_time
        index_date2 = date_time
        index_date1 += timedelta(hours=-margin)
        index_date2 += timedelta(hours=margin)
        return index_date1, index_date2


    def get_tweet_index_name(self, date_time, day_delta):
        """
        Retrieve tweet indexes +/- day_delta around given date
        :param date_time: given date
        :param day_delta: margin in days
        :return:
        """
        index_date = date_time
        if day_delta > 0:
            index_date += timedelta(days=1)
        elif day_delta < 0:
            index_date += timedelta(days=-1)
        # retrieve index suffix
        index_suffix = index_date.strftime("%Y.%m.%d")
        return "tweets-" + index_suffix


    def lookup_tweets(self, date_time, margin):
        """
        Retrieve potentially relevant tweets around a date of a info trafic event
        :param date_time: date of info trafic event
        :param margin: index date margin
        :return: list of tweets
        """
        data = None
        try:
            dt_min, dt_max = self.get_bounds_dates(date_time, 1)
            index_name = self.get_tweet_index_name(date_time, margin)
            dt_min = datetime.strftime(dt_min, '%Y%m%d%H%M%S')
            dt_max = datetime.strftime(dt_max, '%Y%m%d%H%M%S')
            q = json.loads(pystache.render(self.query_sel_tweets, {'dt_min': dt_min, 'dt_max': dt_max}))
            res = self.es.select_page(index_name, q, 0)
            i = 1
            data = []
            long_data = []
            while len(res) != 0:
                short_res = map(lambda x: [x['_source']['created_at'], x['_source']['text']], res)
                data.extend(short_res)
                long_data.extend(res)
                res = self.es.select_page(index_name, q, i)
                i += 1
        except:
            traceback.print_exc()
            pass
        return data, long_data


    def record_tweet_alert(self, index_alert, tweet_alert):
        # test if index already exists
        if not self.es.es.indices.exists(index_alert):
            self.es.es.indices.create(index=index_alert, ignore=400, body=self.index_settings)
        res = self.es.es.index(index=index_alert, doc_type='tweet_alert', body=tweet_alert, id=tweet_alert["id"])




if __name__ == '__main__':

    query_all = {
        "query": {
            "match_all": {}
        }
    }

    #
    # Lookup for all messages provided from via navigo RSS feed
    #
    cnx = ESHandler(host='lame14.enst.fr', port=50014, pg_size=500)

    #
    # Info trafic handler
    #
    it_h = InfoTrafic(cnx, "stif_info_trafic")
    # it_h.word2vec()
    it_h.bm25()
    # print it_h.model_bm25.Items()

    #
    # Instantiate Tweet Browser
    #
    tweet_browser = TweetBrowser(cnx)

    #
    # For each via navigo entry, lookup for candidates tweets
    #
    for entry in it_h.last_messages:
        # convert pub_date
        # dt = datetime.strptime(entry['pub_date'], "%a, %d %b %Y %H:%M:%S")
        dt = entry['pub_date']
        # retrieve candidate tweets
        res = []
        long_res = []
        for margin in [-1, 0, 1]:
            r1, r2 = tweet_browser.lookup_tweets(dt, margin)
            res.extend(r1)
            long_res.extend(r2)
        # for each candidate tweet, compute similarity with current via navigo message
        print('------------------------------------------------------------------------')
        sentence1 = entry['titre']+" "+entry['description']
        print(u"%s", (sentence1))
        print
        for i, tweet in enumerate(long_res):
            # sim = it_h.similarity_word2vec(sentence1, tweet[1])
            if "#Rennes" in tweet['_source']['text']:
                continue
            sentence = it_h.preprocessing_stif_tags(tweet['_source']['text'])
            scores = it_h.model_bm25.BM25Score(sentence)
            scores = np.array(scores)
            if np.size(np.nonzero(scores)) > 0:
                score = np.mean(scores[np.nonzero(scores)])
            else:
                score = 0.
            max_score = np.max(scores)
            nb_zeros = np.size(np.where(scores == 0.))
            if (max_score > 3.) and (nb_zeros < float(len(scores))*0.9):
                # print scores
                t_class = "Classe_2"
                if nb_zeros < float(len(scores))*0.65:
                    t_class = "Classe_1"
                print t_class, score, max_score, nb_zeros
                print(u"%s", (tweet['_source']['text']))
                tweet['_source']['classe'] = t_class
                tweet['_source']['max_score'] = max_score
                tweet['_source']['score_zeros'] = nb_zeros
                ts = time.time()
                st = datetime.fromtimestamp(ts).strftime('%Y.%m.%d')
                tweet_browser.record_tweet_alert("tweet_alerts_"+st, tweet['_source'])

    # write last date
    print("Writing last date")
    it_h.record_last_date()

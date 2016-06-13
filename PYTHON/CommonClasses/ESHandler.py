# -*- coding: utf-8 -*-

from elasticsearch import Elasticsearch
import traceback

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
        self.query_all = {
            "query": {
                "match_all": {}
            }
        }
        self.index_settings = {
            "settings": {
            "number_of_shards": 5,
            "number_of_replicas": 0,
            }
        }


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

    def copy_index(self, src_index, tgt_index, doc_type, id_field):
        """
        Make a copy of src_index in tgt_index
        :param src_index: source index name
        :param tgt_index: target index name
        :param doc_type: mapping to apply to each record
        :param id_field: name of id field
        :return: None
        """
        if not self.es.indices.exists(src_index):
            raise src_index + " does not exist ==> cannot copy"
        if self.es.indices.exists(tgt_index):
            raise tgt_index + " already exists ==> cannot copy"
        else:
            self.es.indices.create(index=tgt_index, ignore=400, body=self.index_settings)
        # browse source index
        res = self.select_page(src_index, self.query_all, 0)
        pg = 1
        while len(res) > 0:
            for entry in res:
                self.es.index(index=tgt_index, doc_type=doc_type, body=entry, id=entry[id_field])
            res = self.select_page(src_index, self.query_all, pg)
            pg += 1



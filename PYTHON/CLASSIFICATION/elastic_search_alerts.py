# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import os
import codecs
import re
import urlmarker
import stif_nexterite_properties
from optparse import OptionParser
import selectImpact
import bm25_impact_tweet
from text_to_bag_of_words import line_has_stif_hashtag
from elasticsearch.helpers import scan

es = stif_nexterite_properties.es
default_index = "nexterite-2015.04.17"
logger = stif_nexterite_properties.logger

#es_index_label = "nexterite-2015.04.17"
#es_index_no_label= "nexterite-2015.06.02"
#es_index_label = "nexterite-2015.09.01"

class Nexterity_Search(object):
    def __init__(self, search_date=None, index=default_index):
        if search_date!=None:
            self.es_index_label = "nexterite-"+search_date
            self.date = search_date
        else:
            tokens = index.split('-')
            self.es_index_label = index
            self.date = tokens[1]

    boolTweets = ' "bool" :{'\
                '"should": ['\
                    '{'\
                    '"match": {'\
                        '"snippet": {'\
                            '"query": "trafic perturbé",'\
                            '"fuzziness": "AUTO",'\
                            '"operator":  "and"'\
                            '}'\
                        '}'\
                    '}'\
                    ', {"match": {'\
                         '"snippet": "accident"'\
                         '}'\
                    '}'\
                    ', {"match": {'\
                         '"snippet": "ralentissement"'\
                         '}'\
                    '}'\
                    ', {"match": {'\
                        '"snippet": {'\
                            '"query": "rer trafic",'\
                            '"fuzziness": "AUTO",'\
                            '"operator":  "and"'\
                            '}'\
                        '}'\
                    '}'\
                    ', {"match": {'\
                        '"snippet": {'\
                            '"query": "rer coupé",'\
                            '"fuzziness": "AUTO",'\
                            '"operator":  "and"'\
                            '}'\
                        '}'\
                    '}'\
                ']'\
            '}'

    def searchAlerts(self,index=None,from_=0, size=10, all=False):
        queryAlert = '{ "query": {'+self.boolTweets+'}}'
        return  elastic_search(index, queryAlert, from_=from_, size=size, all=all)
        #return es.search(index=self.es_index_label, size=size,from_=from_,body=queryAlert,request_timeout=180)


    def searchNoAlerts(self,index=None,from_=0,size=10, all=False):
        queryNoAlert = '{ "query": {"bool" :{ "must_not": [{'+self.boolTweets+'}]}}}'
        return  elastic_search(index, queryNoAlert, from_=from_, size=size, all=all)
        #return es.search(index=self.es_index_label, size=size,from_=from_,body=queryNoAlert,request_timeout=180)


def elastic_search(index, query, from_=0, size=10, all=False, es=es):
    if not all:
        #result = es.search(index, size=size,from_=from_,body=query,request_timeout=180)
        return es.search(index, size=size,from_=from_,body=query,request_timeout=180)

    #result = scan(client= es, query=query, scroll= "10m", index=index,timeout="10m")
    return scan(client= es, query=query, scroll= "10m", index=index,timeout="10m")

def get_indices_list():
    indices = es.indices.get_aliases().keys()
    indices = [index for index in indices if index.startswith('nexterite')]
    return  sorted(indices)

def concat_fields_result(fields, src):
    tokens = fields.split(',')
    result = ""
    sep = ""
    for token in tokens:
        html = src['_source'][token]
        soup = BeautifulSoup(html,'html.parser')
        result +=  sep +  soup.get_text().strip()
        #result +=  sep + html 
        sep = " "

    return result

#def doSearch(searchFct, index, field='snippet'):
def doSearch(searchFct, **kwargs):
    index = kwargs.get("index",None)
    field = kwargs.get("field",'snippet')
    day = kwargs.get("day",None)
    month = kwargs.get("month",None)
    size = searchFct(index=index,day=day,month=month)['hits']['total']

    logger.info("size=%d"%size)
    es_max=10000
    count = size // es_max

    #data = [doc for doc in searchFct(index=index,size=min([size,10000]))['hits']['hits']]
    if count > 0:
        data = searchFct(index=index,day=day,month=month,size=min([size,es_max]),all=True)
    else:
        data = [doc for doc in searchFct(index=index,day=day,month=month,size=min([size,es_max]),all=False)['hits']['hits']]

    textDic = dict()
    for src in data:
        try:
            text_tweet = concat_fields_result(field, src)
            text_tweet = text_tweet.replace('\n',' ').replace('\r',' ')
            #text_tweet = re.sub(r'[^\x00-\x7f]',r'',text_tweet)
            text_tweet = re.sub(urlmarker.URL_REGEX,r'',text_tweet).strip()
            textDic[text_tweet] = text_tweet
        except:
            pass
    return textDic


#def writeAlertsInFile(fileName, searchFct, index=None, field='snippet'):
def writeAlertsInFile(fileName, searchFct, **kwargs):
    snippetDic= doSearch(searchFct,**kwargs)

    file_output = codecs.open(fileName, 'w', 'utf-8')

    for tweet in sorted(snippetDic.keys()):
        file_output.write(tweet+'\n')

    file_output.close()
    logger.info("%s %d"%(fileName,len(snippetDic.keys())))

#def writeAndFilterAlertsInFile(fileName, searchFct, index=None, field='snippet'):
def writeAndFilterAlertsInFile(fileName, searchFct, **kwargs):
    snippetDic= doSearch(searchFct, **kwargs)

    file_output = codecs.open(fileName, 'w', 'utf-8')

    iLine = 0
    for tweet in sorted(snippetDic.keys()):
        if not line_has_stif_hashtag(tweet):
            file_output.write(tweet+'\n')
            iLine += 1

    file_output.close()
    logger.info("%s %d"%(fileName,iLine))



if __name__ == '__main__' :
    op = OptionParser()
    op.add_option("-d", "--date",
                  action="store", dest="sel_date", default=None,
                  help="Date de sélection")
    op.add_option("-i", "--index",
                  action="store", dest="sel_index", default=None,
                  help="Index elasticsearch de sélection")
    (opts, args) = op.parse_args()
    stif_nexterite_properties.StifContext()
    if opts.sel_date!=None:
        nexterite = Nexterity_Search(opts.sel_date)
        data_dir=stif_nexterite_properties.data_dir
        #writeAlertsInFile('alerts_2015_09-01.out',searchAlerts)
        writeAlertsInFile(os.path.join(data_dir,'alerts_'+opts.sel_date+'.out'),nexterite.searchAlerts)
        writeAndFilterAlertsInFile(os.path.join(data_dir,'noAlerts_'+opts.sel_date+'.out'),nexterite.searchNoAlerts)
    elif opts.sel_index!=None:
        nexterite = Nexterity_Search(index=opts.sel_index)
        data_dir=stif_nexterite_properties.data_dir
        writeAlertsInFile(os.path.join(data_dir,'alerts_'+opts.sel_index+'.out'),nexterite.searchAlerts)
    else:
        """ - sélection des index nexterite
            - sélection sur mots clé : écriture d'un fichier d'alertes potentielles et d'un fichier de tweets non qualifiés
                répertoire labeled/pre et notLabeled/pre
            - écriture d'un fichier d'impacts via navigo correspondant à l'index
                répertoire via_navigo
            - similarité entre alertes potentielles et impacts : écriture d'un fichier d'alertes et d'un fichier de tweets non qualifiés
                répertoire labeled et notLabeled
        """
        logger.info("START")
        indices = get_indices_list()
        for index in indices:
            #index = list(indices)[0]
            logger.info(index)
            nexterite = Nexterity_Search(index=index)
            #Ecriture des impacts
            impact_date = nexterite.date.replace('.','-')
            impacts_count=selectImpact.write_impact(impact_date,dir=stif_nexterite_properties.data_via_navigo_dir)
            if impacts_count > 0:
                #Ecriture des alertes potentielles
                writeAlertsInFile(os.path.join(stif_nexterite_properties.data_pre_labeled_dir,'alerts_'+nexterite.date+'.out'),nexterite.searchAlerts)
                writeAndFilterAlertsInFile(os.path.join(stif_nexterite_properties.data_not_labeled_dir,'noAlerts_'+nexterite.date+'.out'),nexterite.searchNoAlerts)
                #Recherche de similimarite entre alertes potentielles et impacts
                bm25_impact_tweet.write_bm25_similarity_files(nexterite.date,data_dir=stif_nexterite_properties.data_dir,data_impact_dir=stif_nexterite_properties.data_via_navigo_dir)
        logger.info("END")

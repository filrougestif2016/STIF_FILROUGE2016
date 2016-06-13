# -*- coding: utf-8 -*-
import os
import elastic_search_alerts
from optparse import OptionParser
import stif_nexterite_properties

es_tweets = stif_nexterite_properties.es_tweets
extract_field = 'text'

data_dir = stif_nexterite_properties.data_dir

def getTweets(index,size=10000,from_=0,all=False):
    query='{ "query": {"match_all": {}}}'
    #return es.search(index=index, size=size,from_=from_,body='{ "query": {"match_all": {}}}',request_timeout=180)
    return elastic_search_alerts.elastic_search(index, query, from_, size, all, es=es_tweets)

if __name__ == '__main__' :
    op = OptionParser()
    op.add_option("-i", "--index",
                  action="store", dest="sel_index", default=None,
                  help="Index elasticsearch de sélection")
    (opts, args) = op.parse_args()
    if opts.sel_index != None:
        elastic_search_alerts.writeAlertsInFile(os.path.join(data_dir,'tweets_'+opts.sel_index+'.out'),getTweets,opts.sel_index,extract_field)


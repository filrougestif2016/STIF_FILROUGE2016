# -*- coding: utf-8 -*-
import os
import elastic_search_alerts
from optparse import OptionParser
import stif_nexterite_properties

es_tweets = stif_nexterite_properties.es_tweets
extract_field = 'text'

data_dir = stif_nexterite_properties.data_dir

def getTweets(index,size=10000,from_=0,all=False, day="19", month="02"):
    start_date=day+"/"+month+"/2016"
    end_day = str(int(day)+1)
    end_date = end_day.zfill(2)+"/"+month+"/2016"

    query='{ "query": '\
            '{ "bool": {'\
            ' "must":[ '\
            '{"range":{ "created_at": { "gte":"'+start_date+'", "lte":"'+end_date+'", "format": "dd/MM/yyyy" } }},'\
            '{"term":{"user.time_zone": "paris"}}'\
            ']}}}'
    return elastic_search_alerts.elastic_search(index, query, from_, size, all, es=es_tweets)

def get_alert_tweets(index,size=10000,from_=0,all=False):
#           '{"bool": { "should": [ {"match": {"classe" : "Classe_1"}}, {"match": {"classe" : "Classe_2"}} ] } } '\
    query='{ "query": '\
            '{ "bool": {'\
            ' "must":[ '\
            '{"range":{ "created_at": { "gte":"19/02/2016", "lte":"20/02/2016", "format": "dd/MM/yyyy" } }},'\
            '{"match": {"classe" : "Classe_1"}} '\
            ']'\
            '}}}'
    #return es.search(index=index, size=size,from_=from_,body='{ "query": {"match_all": {}}}',request_timeout=180)
    return elastic_search_alerts.elastic_search(index, query, from_, size, all, es=es_tweets)

def get_filtered_tweets(index,size=10000,from_=0,all=False):
    query='{ "query": '\
            '{ "bool": {'\
            ' "must":[ '\
            '{"range":{ "created_at": { "gte":"19/02/2016", "lte":"20/02/2016", "format": "dd/MM/yyyy" } }},'\
            '{"bool": { "should": [ '\
            '{"match": {"text": {"fuzziness": "AUTO","operator":"and","query":"panne rer"}}},'\
            '{"match": {"text": {"fuzziness": "AUTO","operator":"and","query":"problème ligne"}}},'\
            '{"match": {"text": {"fuzziness": "AUTO","operator":"and","query":"problème signalisation"}}},'\
            '{"match": {"text": {"fuzziness": "AUTO","operator":"and","query":"malaise voyageur"}}},'\
            '{"match": {"text": {"fuzziness": "AUTO","operator":"and","query":"individu voie"}}},'\
            '{"match": {"text": {"fuzziness": "AUTO","operator":"and","query":"voyageur voie"}}},'\
            '{"match": {"text": {"fuzziness": "AUTO","operator":"and","query":"colis suspect"}}},'\
            '{"match": {"text": {"fuzziness": "AUTO","operator":"and","query":"trafic perturbé"}}},'\
            '{"match": {"text": {"fuzziness": "AUTO","operator":"and","query":"trafic ralenti"}}},'\
            '{"match": {"text": {"fuzziness": "AUTO","operator":"and","query":"rer trafic"}}},'\
            '{"match": {"text": {"fuzziness": "AUTO","operator":"and","query":"rer coupé"}}},'\
            '{"match": {"text":"accident"}},'\
            '{"match": {"text":"ralentissement"}}'\
            ']}}'\
            ']'\
            '}}}'

    #return es.search(index=index, size=size,from_=from_,body='{ "query": {"match_all": {}}}',request_timeout=180)
    return elastic_search_alerts.elastic_search(index, query, from_, size, all, es=es_tweets)

def build_name(indices):
    
    first = indices[0]
    suffix = first[:first.rfind('.')]
    days = ""
    for i in indices:
        days += "."+i[i.rfind('.')+1:]
    return suffix+days

if __name__ == '__main__' :
    op = OptionParser()
    op.add_option("-i", "--index",
                  action="store", dest="sel_index", default=None,
                  help="Index elasticsearch de sélection")
    op.add_option("-a", "--alert_index",
                  action="store", dest="sel_alert_index", default=None,
                  help="Index elasticsearch de sélection des alertes")
    op.add_option("-f", "--filtered_indices",
                  action="store", dest="sel_filtered_indices", default=None,
                  help="Liste d'index de sélection ")
    op.add_option("-d", "--day",
                  action="store", dest="sel_day", default=None,
                  help="Jour à sélectionner")
    op.add_option("-m", "--month",
                  action="store", dest="sel_month", default=None,
                  help="Mois à sélectionner")
    (opts, args) = op.parse_args()
    if opts.sel_index != None:
        day = "19"
        if opts.sel_day != None:
            day = opts.sel_day
        month = "02"
        if opts.sel_month != None:
            month = opts.sel_month
        name = build_name(opts.sel_index.split(','))
        elastic_search_alerts.writeAlertsInFile(os.path.join(data_dir,name+'.out'),getTweets,index=opts.sel_index,field=extract_field,day=day,month=month)
    elif opts.sel_alert_index != None:
        elastic_search_alerts.writeAlertsInFile(os.path.join(data_dir,opts.sel_alert_index+'.out'),get_alert_tweets,index=opts.sel_alert_index,field=extract_field)
    elif opts.sel_filtered_indices != None:
        name = build_name(opts.sel_filtered_indices.split(','))
        elastic_search_alerts.writeAlertsInFile(os.path.join(data_dir,name+'.out'),get_filtered_tweets,index=opts.sel_filtered_indices,field=extract_field)


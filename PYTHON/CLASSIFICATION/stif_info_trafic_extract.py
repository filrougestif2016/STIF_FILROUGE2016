# -*- coding: utf-8 -*-
import os
import elastic_search_alerts
from optparse import OptionParser
import stif_nexterite_properties

es_tweets = stif_nexterite_properties.es_tweets
extract_field = 'titre,texte'

data_dir = stif_nexterite_properties.data_dir
logger = stif_nexterite_properties.logger


def get_day_info_trafic(index,size=10000,from_=0,all=False,day="29",month="05"):
    logger.info("get_day_info_trafic")
    start_date=day+"/"+month+"/2016"
    end_day = str(int(day)+1)
    end_date = end_day.zfill(2)+"/"+month+"/2016"
    query='{ "query": '\
            '{ "constant_score": {'\
            ' "filter": '\
            '{"range":{ "pub_date": { "gte":"'+start_date+'", "lte":"'+end_date+'", "format": "dd/MM/yyyy" } }}'\
            '}}}'
    logger.info(query)
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
    op.add_option("-d", "--day",
                  action="store", dest="sel_day", default=None,
                  help="Jour à sélectionner")
    op.add_option("-m", "--month",
                  action="store", dest="sel_month", default=None,
                  help="Mois à sélectionner")
    (opts, args) = op.parse_args()
    if opts.sel_index != None:
        name = build_name(opts.sel_index.split(','))
        day = "29"
        if opts.sel_day != None:
            day = opts.sel_day
        month = "05"
        if opts.sel_month != None:
            month = opts.sel_month
        elastic_search_alerts.writeAlertsInFile(os.path.join(data_dir,name+"_"+month+"-"+day+'.out'),get_day_info_trafic,index=opts.sel_index,field=extract_field, day= day, month=month)


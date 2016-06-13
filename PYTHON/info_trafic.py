# -*- coding: utf-8 -*-

"""
Abonnement au flux RSS info-trafic du STIF
Version1 : test
"""
import requests
from xml.dom.minidom import parseString
import codecs
from elasticsearch import Elasticsearch
# from datetime import datetime

INFO_TRAFIC_URL = "http://www.vianavigo.com/fr/actualites-trafic/rss-vianavigo-vos-transports-en-commun-en-ile-de-france-optile-ratp-sncf/?type=102"

# ------------------------------
# Elastic search parameters
# ------------------------------
es_server_settings = {'host': 'lame14.enst.fr', 'port': 50014}

index_settings = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0
    }
}

index_name = "stif_info_trafic"


# -------------------------------
# info trafic STIF (get RSS feed)
# -------------------------------
def get_rss_feed(url):
    response = None
    r = requests.get(url)
    status = r.status_code
    if status == 200:
        response = r.text
    r.close()
    return response, status


# --------------------------------------------
# Transform xml RSS feed to python list
# --------------------------------------------
def rss_2_list(rss_feed):
    result = []
    rss_dom = parseString(codecs.encode(rss_feed, "utf-8"))
    # look for update date
    e_date = rss_dom.getElementsByTagName("lastBuildDate")
    # upd_date_ = datetime.strptime(e_date[0].childNodes[0].nodeValue[:-6], "%a, %d %b %Y %H:%M:%S %u")
    upd_date = e_date[0].childNodes[0].nodeValue[:-6]
    # define id for elasticsearch
    # result['id'] = upd_date
    # look for info_trafic items
    items = rss_dom.getElementsByTagName("item")
    # result['infos'] = []
    for i, it in enumerate(items):
        result.append({})
        result[i]['titre'] = it.getElementsByTagName('title')[0].childNodes[0].nodeValue
        result[i]['titre'] = codecs.encode(result[i]['titre'], 'iso-8859-1')
        result[i]['description'] = it.getElementsByTagName('description')[0].childNodes[0].nodeValue
        result[i]['description'] = codecs.encode(result[i]['description'], 'iso-8859-1')
        result[i]['texte'] = it.getElementsByTagName('content:encoded')[0].childNodes[0].nodeValue
        result[i]['texte'] = codecs.encode(result[i]['texte'], 'iso-8859-1')
        result[i]['pub_date'] = it.getElementsByTagName('pubDate')[0].childNodes[0].nodeValue[:-6]
    return result


def record_info_trafic(url, es, index_name):
    f, status = get_rss_feed(INFO_TRAFIC_URL)
    if status == 200:
        list_info = rss_2_list(f)
        # print dict_info
        # record in database
        for item in list_info:
            res = es.index(index=index_name, doc_type='stif_info_trafic', body=item, id=item["pub_date"])


if __name__ == '__main__':
    # create elastic-search handler
    es = Elasticsearch([es_server_settings])
    es.indices.create(index=index_name, ignore=400, body=index_settings)
    record_info_trafic(INFO_TRAFIC_URL, es, index_name)
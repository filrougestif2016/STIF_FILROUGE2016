from elasticsearch import Elasticsearch
import os
import codecs
#Nexterite
es = Elasticsearch([{'host': 'lame14.enst.fr', 'port': 50012}])
es_tweets = Elasticsearch([{'host': 'lame14.enst.fr', 'port': 50014}])

#Pour loguer des traces
import logging
from logging.handlers import RotatingFileHandler
logLevel = logging.WARNING
logger = logging.getLogger()
logger.setLevel(logLevel)
formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
file_handler = RotatingFileHandler('stif.log', 'a', 1000000, 0)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
steam_handler = logging.StreamHandler()
steam_handler.setLevel(logLevel)
logger.addHandler(steam_handler)

data_dir='/infres/ir430/bd/stif/PYTHON/CLASSIFICATION/data/'
brandpart_dir=data_dir
data_impact_dir=data_dir + 'via_navigo/'
lsi_seuil=0.7
label_name = "labeled"
not_label_name = "notLabeled"
pre_name='pre'
data_labeled_dir=data_dir + label_name+'/'
data_pre_labeled_dir=data_labeled_dir + '/'+pre_name+'/'
data_not_labeled_dir=data_dir + not_label_name + '/'
data_pre_not_labeled_dir=data_not_labeled_dir + '/'+pre_name+'/'
data_via_navigo_dir=data_impact_dir 
impact_file_name = "AT_STIF_IMPACTBROADCAST_DEDUP.csv"
bm25_seuil=0.2

class StifContext(object):
    hashtag_set = set()
    @staticmethod
    def load_hashtags_set():
        if len(StifContext.hashtag_set)==0:
            hashtag_file_name = os.path.join(data_dir, "hashtags_twittos_stif.out")
            StifContext.hashtag_set = set(line.strip() for line in codecs.open(hashtag_file_name,encoding='utf-8'))
            logger.info("Hashtag set loaded")

    def __init__(self):
        StifContext.load_hashtags_set()

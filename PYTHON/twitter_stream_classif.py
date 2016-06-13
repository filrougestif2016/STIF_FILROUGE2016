# -*- coding: utf8 -*-
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from contextlib import contextmanager
import multiprocessing
import json
import re
import sys
from elasticsearch import Elasticsearch
import time
import datetime
import CLASSIFICATION.stif_nexterite_properties as stif
import CLASSIFICATION.stif_online_classification as stif_clf
from sklearn.externals import joblib
import os
import CommonClasses.tweet_geoloc as tg
from CommonClasses.ESHandler import ESHandler
#import threading
import traceback


# Variables that contains the user credentials to access Twitter API
access_token = "4393396527-cK3lOyJu3ENYXY8IOfwYq70LIOERFM6GT8T9X6G"
access_token_secret = "IGBGw7FszdmD6liG0js6cB1IulXRXjW5qECM3TMrdO7mw"
consumer_key = "tHJySdGjX2zmaa80WMwCXPK9j"
consumer_secret = "W2YoaUEcuSFjmS1VUAS744s8Um7i11vnbrfEDIQRK5Jj8EWkwT"

output = "twitter.output"
lexical = "filtres-stif.txt"
logger = stif.logger
es_server_settings = {'host': 'lame14.enst.fr', 'port': 50014}

index_settings = {
    "settings": {
        "number_of_shards": 5,
        "number_of_replicas": 0,
    }
}


@contextmanager
def redirect_stdout(stream):
    old_stdout = sys.stdout
    sys.stdout = stream
    try:
        yield
    finally:
        sys.stdout = old_stdout


def handler(signum, frame):
    print('Signal handler called with signal', signum)
    raise IOError("Twitter streaming stopped")


# This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    def __init__(self, es_handler, es_index_name, output_name, clf, tweet_localizer):
        self.es_handler = es_handler
        self.es_index_name = es_index_name
        self.output_name = output_name
        self.es_handler.indices.create(index=self.es_index_name, ignore=400, body=index_settings)
        self.es_handler.indices.create(index='stif-alertes', ignore=400, body=index_settings)
        self.clf = clf
        self.tweet_localizer = tweet_localizer

    def on_data(self, data):
        with open(self.output_name, 'a+') as f:
            with redirect_stdout(f):
                print(data)
                try:
                    res = self.es_handler.index(index=self.es_index_name, doc_type='tweet2', body=data, request_timeout=180)
                    # data string to dictionary
                    data_dict = json.loads(data)
                    if u'text' in data_dict.keys():
                        # Classifier le tweet
                        if stif_clf.isAlert(self.clf, data_dict['text']):
                            # geolocaliser
                            tweet = self.tweet_localizer.localize_tweet(data_dict)
                            # enregistrer dans index stif-alertes
                            res = self.es_handler.index(index='stif-alertes', doc_type='tweet2', body=tweet, request_timeout=180)
                            logger.info("%s\t%s" % ('ALERTE', tweet['text']))
                except Exception as e:
                    logger.error(e,exc_info=True)
                    traceback.print_exc()
                    pass
                return True

    def on_error(self, status):
        print(status)


def getAuth():
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return auth


def getQueryContent():
    content = []
    with open(lexical) as f:
        content = f.readlines()
    content = [x.rstrip() for x in content]
    return (content)


def twitterTrack(qry, clf, tweet_localizer):
    # create elastic-search handler
    es = Elasticsearch([es_server_settings])
    # This handles Twitter authentication and the connection to Twitter Streaming API
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y.%m.%d')
    index_name = "tweets-" + st
    output_name = st + output
    l = StdOutListener(es, index_name, output_name, clf, tweet_localizer)
    # auth = OAuthHandler(consumer_key, consumer_secret)
    # auth.set_access_token(access_token, access_token_secret)
    auth = getAuth()
    stream = Stream(auth, l)

    # This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=qry, languages=['fr'])


def printTweetsText(df):
    exclude = re.compile(r'^.*#MTVStars.*$')
    for index, row in df.iterrows():
        try:
            text = row['text']
        except:
            continue

        if not re.match(exclude, text):
            print("-------screen_name=", row['user']['screen_name'])
            print(text)

if __name__ == '__main__':

    # Si CLASSIFICATION n'est pas dans le PYTHONPATH, ca deconne
    # pourtant il y a bien un fichier __init__.py dans CLASSIFICATION
    PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.join(PROJECT_DIR, 'CLASSIFICATION'))

    logger = stif.logger
    data_dir = stif.data_dir
    clf_dir = os.path.join(data_dir, 'clf_serial')
    clf_filename = 'stif_clf.pkl'

    # Chargement du classifier entrainé à faire une seule fois
    clf = joblib.load(os.path.join(clf_dir, clf_filename))

    #
    # Connection to elasticsearch server
    #
    cnx = ESHandler(host='lame14.enst.fr', port=50014, pg_size=500)

    tweetLocalizer = tg.TweetLocalizer(cnx)
    tweetLocalizer.load_all_lines()

    words = getQueryContent()

    #p = threading.Thread(target=twitterTrack, name="twitterTrack", args=(words, clf, tweetLocalizer))
    p = multiprocessing.Process(target=twitterTrack, name="twitterTrack", args=(words, clf, tweetLocalizer))
    p.start()
    p.join(3600 * 24 - 60)
    if p.is_alive():
        p.terminate()
        p.join()

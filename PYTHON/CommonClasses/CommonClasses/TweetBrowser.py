# -*- coding: utf-8 -*-
from datetime import timedelta, datetime
import pystache
import json
import traceback

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

        self.query_date_interval = {
           "size": 0,
            "aggs": {
                "min_date": {"min": {"field": "created_at", "format": "yyyyMMddHHmmss"}},
                "max_date": {"max": {"field": "created_at", "format": "yyyyMMddHHmmss"}}
            }
        }

    def get_all_tweet_indices(self):
        """
        list all tweets indices
        :return:
        """
        indices = self.es.es.indices.get('tweets-*')
        return sorted(indices)

    def get_date_interval(self, index_name):
        res = self.es.es.search(index=index_name, body=self.query_date_interval, request_timeout=180)
        dt_min = datetime.strptime(res['aggregations']['min_date']['value_as_string'], "%Y%m%d%H%M%S")
        dt_max = datetime.strptime(res['aggregations']['max_date']['value_as_string'], "%Y%m%d%H%M%S")
        return dt_min, dt_max

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


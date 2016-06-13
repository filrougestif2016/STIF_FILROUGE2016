# -*- coding: utf-8 -*-

import CommonClasses.preprocessing_alerts as pa
import codecs
from CommonClasses.ESHandler import ESHandler
import pystache
import json
import traceback
import re


class LineStops:

    def __init__(self, cnx):
        self.cnx = cnx
        self.query_sel_stops = '{ \
          "query": { \
            "filtered": { \
                "filter": { \
                    "bool": { \
                        "must_not": [ \
                            {"missing": {"field": "fields.route_long_name"}} \
                        ], \
                        "must": [ \
                            {"match": {"fields.route_long_name": "{{line}}"}} \
                        ] \
                    } \
                } \
            } \
          } \
        }'
        self.gares = [u'gare de lyon', u'gare du nord', u'gare st lazare', u"gare de l'est", u"gare d'austerlitz",
                      u"gare de l est", u"gare d austerlitz"]

    def normalize_stops(self, entry):
        entry[1] = re.sub(' rer [abcdehkjpru]', '', entry[1])
        entry[1] = re.sub(' ligne [\d]+(bis)', '', entry[1])
        if entry[1] not in self.gares:
            entry[1] = entry[1].replace(u'gare de ', '')
            entry[1] = entry[1].replace(u"gare d'", '')
            entry[1] = entry[1].replace(u'gare du ', '')
            entry[1] = entry[1].replace(u'gare des ', '')
        return [entry[0], entry[1], entry[2]]

    def get_station_list(self, line, index_name):
        try:
            q = json.loads(pystache.render(self.query_sel_stops, {'line': line}))
            res = self.cnx.select_page(index_name, q, 0)
            i = 1
            data = []
            long_data = []
            while len(res) != 0:
                short_res = map(lambda x: [x['_id'], x['_source']['fields']['stop_name'].lower(), x['_source']['fields']['pointgeo']], res)
                res = short_res
                short_res = map(self.normalize_stops, res)
                data.extend(short_res)
                long_data.extend(res)
                res = self.cnx.select_page(index_name, q, i)
                i += 1
        except:
            traceback.print_exc()
        return data


class TweetLocalizer:

    def __init__(self, es_cnx):
        self.es_cnx = es_cnx
        self.line_stops = LineStops(es_cnx)
        self.dicLines = {}

    def load_all_lines(self):
        for l in pa.lignes_metro:
            self.dicLines[l] = self.line_stops.get_station_list(l.upper(), "stif-metro")
        for l in pa.lignes_rer:
            self.dicLines[l] = self.line_stops.get_station_list(l.upper(), "stif-rer")

    def localize_tweet(self, tweet):
        tweet_text = tweet['text']
        # tranform text and identify all relevant transportation lines for tweet
        t_line, list_lines = pa.lookup_tc_lines(unicode(tweet_text))
        # deal only with deterministic lines
        if len(list_lines) == 1:
            # check if we get metro or RER
            line_id = list_lines[0][1]
            if not line_id in self.dicLines.keys():
                # load stops for line if it is not already in the dictionary
                if not line_id[0].isdigit():
                    self.dicLines[line_id] = self.line_stops.get_station_list(line_id.upper(), "stif-rer")
                else:
                    if list_lines[0][0] != 't':
                        self.dicLines[line_id] = self.line_stops.get_station_list(line_id.upper(), "stif-metro")
        # do nothing if tramway (stops are not available in the database)
        if (len(list_lines) == 1) and (list_lines[0][0] != 't'):
            # get only stop names for line
            list_stp = map(lambda x: (x[1], x[2]), self.dicLines[line_id])
            # get relevant stops regarding message
            relevant_stops = pa.best_distances(tweet_text, list_stp)
            tweet['transport'] = list_lines[0][0]+list_lines[0][1]
            if len(relevant_stops) > 0:
                reduced_msg_list = pa.reduced_msg_list(tweet_text)
                scores_stops, tag_words = pa.score_words_in_sentence(reduced_msg_list, relevant_stops)
                if not all(x == 0 for x in tag_words):
                    analysis = pa.tag_words_analysis(tag_words)
                    for pattern in analysis:
                        if len(pattern) == 1:
                            if not 'localization' in tweet.keys():
                                tweet['localization'] = relevant_stops[pattern[0]-1][0][1]
                                tweet['localization_text'] = relevant_stops[pattern[0]-1][0][0]
                        else:
                             tweet['section'] = []
                             tweet['section_text'] = []
                             for i in pattern:
                                tweet['section'].append(relevant_stops[i-1][0][1])
                                tweet['section_text'].append(relevant_stops[i-1][0][0])
        return tweet


if __name__ == '__main__':
    #
    # Connection to elasticsearch server
    #
    cnx = ESHandler(host='lame14.enst.fr', port=50014, pg_size=500)

    line_stops = LineStops(cnx)

    dicLines = {}

    f = codecs.open('d:/temp/tweets.txt', 'r', encoding='utf-8')
    line_identification = 0
    total_rows = 0
    for line in f:
        total_rows += 1
        line = line[1:-2]
        line = line.replace("\n", ' ').lower()
        t_line0, list_lines0 = pa.lookup_tc_lines(unicode(line))
        if len(list_lines0) == 1:
            line_identification += 1
        if not line.startswith(u'rt '):
            t_line, list_lines = pa.lookup_tc_lines(unicode(line))
            if len(list_lines) == 1:
                line_id = list_lines[0][1]
                if not line_id in dicLines.keys():
                    # load stops for line
                    if not line_id[0].isdigit():
                        dicLines[line_id] = line_stops.get_station_list(line_id.upper(), "stif-rer")
                    else:
                        if list_lines[0][0] != 't':
                            dicLines[line_id] = line_stops.get_station_list(line_id.upper(), "stif-metro")
            # print line
            # print u"ligne(s) identifiée(s) : ", list_lines
            if (len(list_lines) == 1) and (list_lines[0][0] != 't'):
                # print line_id
                # print(dicLines[line_id])
                list_stp = map(lambda x: (x[1], x[2]), dicLines[line_id])
                # print list_stp
                relevant_stops = pa.best_distances(line, list_stp)
                if len(relevant_stops) > 0:
                    print line
                    print u"ligne(s) identifiée(s) : ", list_lines
                    reduced_msg_list = pa.reduced_msg_list(line)
                    reduced_msg = pa.build_msg_from_list_words(reduced_msg_list)
                    # print(pa.best_distances(reduced_msg, list_stp))
                    scores_stops, tag_words = pa.score_words_in_sentence(reduced_msg_list, relevant_stops)
                    if not all(x == 0 for x in tag_words):
                        print reduced_msg
                        print "arrêt(s) identifié(s) : ", relevant_stops
                        # print(scores_stops)
                        print(tag_words)
                        analysis = pa.tag_words_analysis(tag_words)
                        pa.print_analysis(analysis, relevant_stops)
                    print

    print "total alertes:", total_rows
    print u"lignes identifiées", line_identification

    f.close()
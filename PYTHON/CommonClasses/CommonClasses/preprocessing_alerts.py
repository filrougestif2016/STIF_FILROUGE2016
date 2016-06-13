# -*- coding: utf-8 -*-

import itertools
import re

# from os import path
from stop_words import get_stop_words
import unicodedata
# from fuzzywuzzy import fuzz
from snowballstemmer import stemmer
# from metaphone import doublemetaphone
# from Levenshtein import _levenshtein
# from Levenshtein._levenshtein import *

moyens = ['rer', 'ligne', 'ter', u'métro', 'metro', ' t', 'tram', 'bus']
lignes = ['a', 'b', 'c', 'd', 'e', 'h', 'k', 'j', 'p', 'r', 'u',
          '1', '2', '3', '3bis', '4', '5', '6', '7', '7bis', '8', '9', '10', '11', '12', '13', '14']

lignes_metro = ['1', '2', '3', '3bis', '4', '5', '6', '7', '7bis', '8', '9', '10', '11', '12', '13', '14']

lignes_rer = ['a', 'b', 'c', 'd', 'e', 'h', 'k', 'j', 'p', 'r', 'u']

fr_prep = ['entre', 'devant', 'derriere', 'derrière', 'à', 'a', 'de']

dic_synonyms_re = {
    r'(\s+|^)gdl(\s+|$)': u' gare de lyon ',
    r'(\s+|^)gdn(\s+|$)': u' gare du nord ',
    r'(\s+|^)st\s+laz(\s+|$)': u' st lazare ',
    r'(\s+|^)pref(\s+|$)': u' prefecture ',
    r'(\s+|^)mvlc(\s+|$)': u' marne la vallee chessy ',
    r'\&[a-z]+;': u''
}

fr_stop_words = get_stop_words('fr')
fr_stop_words.extend([u'gare', u'vers'])


def preprocessing_stif_tags(data):
    """
    Preprocess an eligible alert text
    :type data: text to transform
    """
    # for moyen in moyens:
    #     if u"#"+moyen in data:
    #        data += " "+moyen
    data = data.replace("#", '').lower()
    data = data.replace("@", '').lower()
    data = data.replace('\n', ' ').lower()
    data = data.replace('\t', ' ').lower()
    data = data.replace("en ligne", '')
    data = data.replace("hors ligne", '')
    data = data.replace("hors fixe", '')
    data = data.replace(u'ligne téléphonique', '')
    for syn in dic_synonyms_re.keys():
        data = re.sub(syn, dic_synonyms_re[syn], data).strip()
    for i in itertools.product(moyens, lignes):
        data = data.replace(i[0]+' '+i[1], i[0]+i[1])
        # data = data.replace(' '+i[0]+i[1]+'_', ' '+i[0]+i[1]+' ')
        data = data.replace(i[0]+i[1]+'_', i[0]+i[1]+' ')
    data = re.findall("\w+", data, re.UNICODE)
    return data


def lookup_tc_lines(tweet_text):
    """
    Identify all transportation lines present in tweet_text
    :param tweet_text:
    :return: preprocessed text and list of relevant transportation lines
    """
    txt = preprocessing_stif_tags(tweet_text)
    result = []
    for i in itertools.product(moyens, lignes):
        line = i[0]+i[1]
        # lookup for line occurences in txt
        if line in txt:
            result.append((i[0], i[1]))
    return txt, result


def remove_stop_words(preproc_sentence):
    """
    remove french stop words from a sentence splitted in words
    :param preproc_sentence:
    :return:
    """
    result = []
    for w in preproc_sentence:
        if not w in fr_stop_words:
            result.append(w)
    return result


# def metaphone_intersect(set1, set2):
#     result = set()
#     for e1 in set1:
#         for e2 in set2:
#             if distance(e1, e2) <= 1:
#             # if doublemetaphone(e1) == doublemetaphone(e2):
#                 result.add(e2)
#     return result


def distance_stop(txt, stop_name):
    """
    Define a distance (metrics) to determine how relevan is a station
    stop name fro a given text
    Algorithm is simple : returns the number of common words found
    :param txt: tweet text
    :param stop_name: station name
    :return: distance as integer. Higher is the distance, higher is the
             stop name relevant
    """
    data = preprocessing_stif_tags(txt)
    stp = preprocessing_stif_tags(stop_name)
    # number of common words between txt and stop_name
    set1 = set(data).difference(set(fr_stop_words))
    data_reduced = list(set1)
    set2 = set(stp).difference(set(fr_stop_words))
    commons = list(set1 & set2)
    if len(commons) == 1 and commons[0].isdigit():
        nb_commons = 0
    else:
        nb_commons = len(list(set1 & set2))
    # nb_commons = len(list(metaphone_intersect(set1,set2)))
    result = nb_commons
    for common in commons:
        pos = data_reduced.index(common)
        if (pos > 0) and (data_reduced[pos-1] in [u'a', u'à']):
            result += 2
    return result


def best_distances(txt, stop_list):
    """
    Given a tweet text and a station stop names list, returns
    the distances (using the distance_stop function) between
    text and each stop name, sorted by relevance
    :param txt: tweet text
    :param stop_list: list of stops related to a given transportation line
    :return: list of stops with related score distance to text sorted
             by relevance (keep only non zero distances)
    """
    result = []
    # remove french specific characters which are not kept in the
    # stop names dataset
    txt = unicodedata.normalize('NFD', txt).encode('ascii', 'ignore')
    for stp in stop_list:
        stp_name = unicodedata.normalize('NFD', stp[0]).encode('ascii', 'ignore')
        d = distance_stop(txt, stp_name)
        if d > 0:
            result.append([stp, d])
    result = sorted(result, key=getKey, reverse=True)
    return result


def distances(txt, stop_list):
    """
    Given a tweet text and a station stop names list, returns
    the distances (using the distance_stop function) between
    text and each stop name
    :param txt: tweet text
    :param stop_list: list of stops related to a given transportation line
    :return: list of stops with related score distance
    """
    result = []
    txt = unicodedata.normalize('NFD', txt).encode('ascii', 'ignore')
    for stp in stop_list:
        stp_name = unicodedata.normalize('NFD', stp[0]).encode('ascii', 'ignore')
        d = distance_stop(txt, stp_name)
        result.append([stp, d])
    return result


def score_words_in_sentence(l_sentence, best_stops):
    """
    Define a score of relevance for each word in tweet
    We consider only non stop words, stemmed words either for tweet and stop name
    :param l_sentence: tweet split in list of words
    :param best_stops: list of more relevant stops
    :return: 1. list of kept/stemmed words found in tweet
             2. list of scores for each of these words
    """
    sb_stemmer = stemmer('french')
    stemmed_sentence = [sb_stemmer.stemWords([x])[0] for x in l_sentence]
    scores_stops = []
    tag_words = [0 for _ in l_sentence]
    relevant_stops = map(lambda x: unicodedata.normalize('NFD', x[0][0]).encode('ascii', 'ignore'), best_stops)
    rg_stop = 1
    for stop in relevant_stops:
        stop_w_index = []
        stop_lw = re.findall("\w+", stop, re.UNICODE)
        for w_stop in stop_lw:
            if not w_stop in fr_stop_words:
                stemmed_w = sb_stemmer.stemWords([w_stop])[0]
                if stemmed_w in stemmed_sentence:
                    stop_w_index.append(stemmed_sentence.index(stemmed_w))
        score_w = 0
        for i in range(len(stop_w_index)):
            if (i > 0) and (stop_w_index[i] <= stop_w_index[i-1]):
                score_w = 0
                break
            else:
                score_w += 1
        scores_stops.append(score_w)
        if score_w != 0:
            for idx in stop_w_index:
                if tag_words[idx] == 0:
                    tag_words[idx] = rg_stop
        rg_stop += 1
    return scores_stops, tag_words


def build_msg_from_list_words(l):
    """
    rebuilt a message as string from a list of words
    (add a space character between each word)
    :param l: list of words
    :return: a string as message
    """
    result = ''
    for w in l:
        if result == '':
            result += w
        else:
            result += ' '+w
    return result


def getKey(item):
    """
    function used to sort stops
    :param item: a list with 2 elements (stop_name and score)
    :return: score (second element)
    """
    return item[1]


# def best_fuzzy_distances(txt, stop_list):
#     """
#     Compute a fuzzy distance between stop names and tweet using a fuzzy matcher
#     (levenshtein distance)
#     :param txt: tweet text
#     :param stop_list: list of stop names
#     :return: list of stops with related distances sorted by relevance
#              (from higher to smaller)
#     """
#     result = []
#     txt = unicodedata.normalize('NFD', txt).encode('ascii', 'ignore')
#     for stp in stop_list:
#         d = fuzz.partial_ratio(txt, stp)
#         if d > 0:
#             result.append([stp, d])
#     result = sorted(result, key=getKey, reverse=True)[0:10]
#     return result


def reduced_msg_list(msg):
    """
    Reduce a message list : remove stop words / remove special french characters
    :param msg: message to reduce as string
    :return: a list with normalized and non stop words words found in message
    """
    msg_no_accents = unicodedata.normalize('NFD', msg).encode('ascii', 'ignore')
    return remove_stop_words(preprocessing_stif_tags(msg_no_accents))


def tag_words_analysis(tag_words):
    """
    identify patterns in a message tagged word list
    a pattern with a sequence of the same station id is interpreted as a specific localization
    a pattern with a sequence of several station ids is interpreted as a localization set
    :param tag_words: list of words with related tags (station id)
    :return: list of patterns (each pattern is or a single station id or a list of station ids)
    """
    patterns = []
    next_pattern = []
    nb_patterns = 0
    all_pattern_size_is_1 = True
    for val in tag_words:
        if val != 0:
            if (len(next_pattern) == 0) or (val not in next_pattern):
                next_pattern.append(val)
        else:
            if len(next_pattern) != 0:
                patterns.append(next_pattern)
                if len(next_pattern) > 1:
                    all_pattern_size_is_1 = False
                nb_patterns += 1
                next_pattern = []
    if len(next_pattern) != 0:
        patterns.append(next_pattern)
        if len(next_pattern) > 1:
            all_pattern_size_is_1 = False
    if (nb_patterns == 2) and (all_pattern_size_is_1):
        patterns[0].extend(patterns[1])
        del patterns[-1]
    return patterns


def print_analysis(patterns, relevant_stops):
    """
    Display information from identified patterns and relevant stops list
    :param patterns:
    :param relevant_stops:
    :return:
    """
    for pattern in patterns:
        if len(pattern) == 1:
            print(u"lieu identifié : "+relevant_stops[pattern[0]-1][0][0])
        else:
            locations = ""
            for i in pattern:
                if locations == "":
                    locations += relevant_stops[i-1][0][0]
                else:
                    locations += ", "+relevant_stops[i-1][0][0]
            print(u"suite de lieux identifiée : ("+locations+u")")
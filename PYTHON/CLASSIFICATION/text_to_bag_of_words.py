# -*- coding: utf-8 -*-
from nltk.corpus import stopwords
import re
from nltk.tokenize import TweetTokenizer
from nltk.tokenize import RegexpTokenizer
from itertools import chain
from stif_nexterite_properties import StifContext,logger

tweet_tokenizer = TweetTokenizer()
regexp_tokenizer = RegexpTokenizer('[^\']+')


stop_word_list = stopwords.words('french')
stop_word_list.append("les")
stop_word_list.append("rt")

def emoji_remove(word):
    try:
        # Wide UCS-4 build
        myre = re.compile(u'['
            u'\U0001F300-\U0001F64F'
            u'\U0001F680-\U0001F6FF'
            u'\u2600-\u26FF\u2700-\u27BF]+',
            re.UNICODE)
    except re.error:
        # Narrow UCS-2 build
        myre = re.compile(u'('
            u'\ud83c[\udf00-\udfff]|'
            u'\ud83d[\udc00-\ude4f\ude80-\udeff]|'
            u'[\u2600-\u26FF\u2700-\u27BF])+',
            re.UNICODE)
    return(myre.sub('', word))


def transform_line(line):
    tokens = [word for word in [emoji_remove(re.sub(r'[\\".,?!:;()\[\]\{\}/]' , "", word) )
                            for word in chain.from_iterable([regexp_tokenizer.tokenize(word)
                                                             for word in tweet_tokenizer.tokenize(line.lower().strip())])
                            if word not in stop_word_list]
          if len(word)>0]
    return tokens

def line_has_stif_hashtag(line):
    return words_have_stif_hashtag(transform_line(line))

def words_have_stif_hashtag(words):
    for word in words:
        if re.match('^[#|@]\w',word):
            if word[1:] in StifContext.hashtag_set:
                return True
    return False


# -*- coding: utf-8 -*-

import itertools
import re

def preprocessing_stif_tags(data):
    """
    Preprocess an eligible alert text
    :type data: text to transform
    """
    data = data.replace("#", '').lower()
    data = data.replace("en ligne", '')
    data = data.replace("hors ligne", '')
    data = data.replace("hors fixe", '')
    data = data.replace(u'ligne téléphonique', '')
    moyens = ['rer', 'ligne', 'ter', u'métro', 'metro', 't', 'tram', 'bus']
    lignes = ['a', 'b', 'c', 'd', 'e', 'h', 'k', 'j', 'p', 'r', 'u',
              '1', '2', '3', '3bis', '4', '5', '6', '7', '7bis', '8', '9', '10', '11', '12', '13', '14']
    for i in itertools.product(moyens, lignes):
        data = data.replace(i[0]+' '+i[1], i[0]+i[1])
        data = data.replace(' '+i[0]+i[1]+'_', ' '+i[0]+i[1]+' ')
    data = re.findall("\w+", data, re.UNICODE)
    return data


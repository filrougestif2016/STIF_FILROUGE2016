# -*- coding: utf-8 -*-
import os
import numpy as np
import codecs
import stif_nexterite_properties
from text_to_bag_of_words import transform_line
from optparse import OptionParser
import re

data_dir=stif_nexterite_properties.data_dir
logger = stif_nexterite_properties.logger

def unique_line(source):
    dico = {}
    with codecs.open(os.path.join(data_dir,source), 'r',encoding='iso-8859-1') as f:
        for item_no, line in enumerate(f):
            dico[line] =1

    return dico,item_no

def write_file(fileName,dico):
    file_output = codecs.open(fileName, 'w', 'utf-8')

    for tweet in sorted(dico.keys()):
        file_output.write(tweet+'\n')

    file_output.close()
    logger.info("%s %d"%(fileName,len(dico.keys())))

def write_lines_file(fileName, lines):
     file_output = codecs.open(fileName, 'w', 'utf-8')
     file_output.writelines(lines)
     file_output.close()

def load_file_in_dict(source):
    dico = {}
#    with codecs.open(source, 'r',encoding='iso-8859-1') as f:
    with codecs.open(source, 'r',encoding='utf-8') as f:
        for item_no, line in enumerate(f):
            dico[line] =1

    return dico,item_no

def write_bow(source,cible):
    lines = []
    with codecs.open(source, 'r',encoding='utf-8') as f:
        for item_no, line in enumerate(f):
            words = transform_line(line)            
            new_line="%d ====> %s\n" % (item_no,", ".join(words))
            lines.append(new_line)

    write_lines_file(cible,lines)

def diff_files(f1, f2):
    (d1,c1) = load_file_in_dict(f1)
    (d2,c2) = load_file_in_dict(f2)
    logger.info ("fichier %s %d lignes"%(f1,c1))
    logger.info ("fichier %s %d lignes"%(f2,c2))
    missing=0
    less_lines =[]
    for k in d1.keys():
        if k not in d2:
            less_lines.append(k)
            missing += 1
    write_lines_file(os.path.join(stif_nexterite_properties.data_dir,"en_moins.out"), less_lines)
    happy_correct_answers = (c1 - missing)
    # logger.info ("lignes en communs %d %f"% ((c1 - missing),(100 * (c1 - missing))/c1))
    # logger.info ("lignes manquantes %d %f"% (missing, (100 * missing)/c1))
    logger.info ("lignes en communs %d"% (c1 - missing))
    logger.info ("lignes manquantes %d"% missing)
    logger.info("precision % f"% (float(happy_correct_answers)/float(c2)))
    logger.info("rappel % f"% (float(happy_correct_answers)/float(c1)))
    more=0
    more_lines =[]
    for k in d2.keys():
        if k not in d1:
            more_lines.append(k)
            more += 1
    write_lines_file(os.path.join(stif_nexterite_properties.data_dir,"en_plus.out"),more_lines)
    logger.info ("lignes en sus %d %f"% (more,(100 * more)/c1))

def test_unique():
    filename='alertes_identifees.out'
    (d,c) = unique_line(os.path.join(stif_nexterite_properties.data_dir,filename))
    logger.info("%d lines in %s"%(c,filename))
    write_file(os.path.join(stif_nexterite_properties.data_dir,"new_"+filename),d)

def select_proba_tweets(source,proba):
    lines = []
    with codecs.open(source, 'r',encoding='utf-8') as f:
        for line in f:
            m = re.match(r"(\d+\.\d+)\t(.*)$", line)
            if m != None:
                l_proba = float(m.group(1))
                text = m.group(2)
                if l_proba >= proba:
                    lines.append(text+'\n')
    return lines



def diff_classification():
    f2_name = 'tweets-2016.02.18.19.20_PRED_ALERTS.out'
    f1_name = 'tweet_alerts_.out'
    diff_files(os.path.join(data_dir, f1_name),os.path.join(data_dir, f2_name))
    

if __name__ == '__main__' :
    op = OptionParser()
    op.add_option("-d", "--diff",
                  action="store", dest="dif_file", default=None,
                  help="Comparaison avec alertes témoins")
    op.add_option("-p", "--proba",
                  action="store", dest="proba", default=None,
                  help="Proba de selection des tweets")
    (opts, args) = op.parse_args()

    if opts.dif_file != None:
        classif_dir=stif_nexterite_properties.data_dir

        f1_name = 'tweet_alerts_.out'
        if opts.proba != None:
            proba = float(opts.proba)
            lines = select_proba_tweets(os.path.join(classif_dir,opts.dif_file),proba)
            suffix =opts.dif_file[:opts.dif_file.rfind('.')]
            f2_name =  suffix+"_"+opts.proba+".out"
            write_lines_file(os.path.join(classif_dir,f2_name),lines)
        else:
            f2_name = opts.dif_file

        #f2_name = 'alerts_impact_2015-04-17.out'
        #classif_dir=os.path.join(stif_nexterite_properties.home,'pycharmProjects/stif/lame14/DATA/classif/')
        #f1_name = 'tweet_alerts_2016.02.19.out'
        #f2_name = 'tweets-2016.02.18.19.20.out'
        #f2_name = 'bm25_alerts_impact_2015-04-17.out'
        diff_files(os.path.join(classif_dir, f1_name),os.path.join(classif_dir, f2_name))
#    source = os.path.join(data_dir, "pos_tweets.out")
#    cible = os.path.join(data_dir, "words_pos_tweets.out")
#    write_bow(source,cible)

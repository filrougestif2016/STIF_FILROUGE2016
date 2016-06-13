# -*- coding: utf-8 -*-
import CLASSIFICATION.stif_nexterite_properties as stif
import CLASSIFICATION.stif_online_classification as stif_clf
from sklearn.externals import joblib
import os
import sys

# Si CLASSIFICATION n'est pas dans le PYTHONPATH, ça déconne
# pourtant il y a bien un fichier __init__.py dans CLASSIFICATION
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(PROJECT_DIR,'CLASSIFICATION'))

logger = stif.logger
data_dir = stif.data_dir
clf_dir = os.path.join(data_dir,'clf_serial')
clf_filename = 'stif_clf.pkl'

#Chargement du classifier entrainé à faire une seule fois
clf = joblib.load(os.path.join(clf_dir,clf_filename))
test1="@franceinfo: #Incendie  #LaCourneuve : la reprise du trafic sur le #RERB entre Aulnay et la Gare du Nord repousse  la fin du service."
tag="ALERTE"

#Pour tester
if stif_clf.isAlert(clf,test1)==False:
    tag = "NON "+tag
logger.info("%s\t%s"%(tag,test1))

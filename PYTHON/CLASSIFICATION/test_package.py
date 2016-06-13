# -*- coding: utf-8 -*-
import stif_nexterite_properties as stif
import stif_online_classification as stif_clf
from sklearn.externals import joblib
import os

logger = stif.logger
data_dir = stif.data_dir
clf_dir = os.path.join(data_dir,'clf_serial')
clf_filename = 'stif_clf.pkl'

clf = joblib.load(os.path.join(clf_dir,clf_filename))
test1="@franceinfo: #Incendie  #LaCourneuve : la reprise du trafic sur le #RERB entre Aulnay et la Gare du Nord repousse  la fin du service."
tag="ALERTE"
if stif_clf.isAlert(clf,test1)==False:
    tag = "NON "+tag
logger.info("ALERTE %s"%(test1))


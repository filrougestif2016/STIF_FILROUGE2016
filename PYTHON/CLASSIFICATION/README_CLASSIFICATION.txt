#Creation des fichiers pour l entrainement du classifier a paritr des donnees de Nexterite
#Le dataset est equilibre par le programme
python elastic_search_alerts.py

#Creation d un fichier contenant les tweets filtres du 19/02/2016
python stif_extract_lame14.py -f tweets-2016.02.18,tweets-2016.02.19,tweets-2016.02.20

#Creation d un fichier contenant les tweets non filtres du 19/02/2016
#Solution choisie
python stif_extract_lame14.py -i tweets-2016.02.18,tweets-2016.02.19,tweets-2016.02.20

#Creation d un fichier contenant les tweets classes 1
python stif_extract_lame14.py -a tweet_alerts_

#Classification des tweets du 19/02/2016 avec un classifieur RandomForest entraine sur les tweets de Nexterite
python stif_classification.py -c tweets-2016.02.18.19.20.out

#Classification des tweets du 19/02/2016 avec un classifieur RandomForest entraine sur les tweets de Nexterite
#le tfidf de sklearn est remplacé par du bm25
python stif_classification.py -c tweets-2016.02.18.19.20.out --bm25 True

#Classification des tweets du 19/02/2016 doc2vec + logisticRegression entraine sur les tweets de Nexterite
python stif_doc2vec.py -c tweets-2016.02.18.19.20.out

#Entrainement du classifier
python stif_online_classification.py -t True

#Classification essai sur un tweet
python stif_online_classification.py

#Comparaison du résultat avec fichier témoin (tweets classes 1)
python utils.py -d tweets-2016.02.18.19.20_PRED_ALERTS.out


#Comparaison du résultat avec fichier témoin (tweets classes 1)avec seuil de proba en paramètre
python utils.py -d tweets-2016.02.18.19.20PRED_PROBA.out -p 0.8

#EXtraction des données info trafic sur une journée
python stif_info_trafic_extract.py -i stif_info_trafic


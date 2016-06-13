# ETAPE1 - Extraction de 5 journees info trafic
python stif_info_trafic_extract.py -i stif_info_trafic -d 29 -m 05
python stif_info_trafic_extract.py -i stif_info_trafic -d 15 -m 05
python stif_info_trafic_extract.py -i stif_info_trafic -d 24 -m 04
python stif_info_trafic_extract.py -i stif_info_trafic -d 22 -m 03
python stif_info_trafic_extract.py -i stif_info_trafic -d 13 -m 03

#ETAPE2 - Extraction de 5 journees tweets
python stif_extract_lame14.py -i tweets-2016.05.28,tweets-2016.05.29,tweets-2016.05.30 -d 29 -m 05
python stif_extract_lame14.py -i tweets-2016.05.14,tweets-2016.05.15,tweets-2016.05.16 -d 15 -m 05
python stif_extract_lame14.py -i tweets-2016.04.23,tweets-2016.04.24,tweets-2016.04.25 -d 24 -m 04
python stif_extract_lame14.py -i tweets-2016.03.21,tweets-2016.03.22,tweets-2016.03.23 -d 22 -m 03
python stif_extract_lame14.py -i tweets-2016.03.12,tweets-2016.03.13,tweets-2016.03.14 -d 13 -m 03

#ETAPE3 - Similarité BM25 entre journées info trafic et journées tweets
python bm25_impact_tweet.py -d 2016.05.29 --src stif_info_trafi.stif_info_trafic_05-29.out --target tweets-2016.05.28.29.30.out
python bm25_impact_tweet.py -d 2016.05.15 --src stif_info_trafi.stif_info_trafic_05-15.out --target tweets-2016.05.14.15.16.out
python bm25_impact_tweet.py -d 2016.04.24 --src stif_info_trafi.stif_info_trafic_04-24.out --target tweets-2016.04.23.24.25.out
python bm25_impact_tweet.py -d 2016.03.22 --src stif_info_trafi.stif_info_trafic_03-22.out --target tweets-2016.03.21.22.23.out
python bm25_impact_tweet.py -d 2016.03.13 --src stif_info_trafi.stif_info_trafic_03-13.out --target tweets-2016.03.12.13.14.out

#ETAPE4 - Classification (random forest entrainé sur données nexterité) sur les 5 journées tweets
python stif_online_classification.py -c tweets-2016.05.28.29.30.out
python stif_online_classification.py -c tweets-2016.05.14.15.16.out
python stif_online_classification.py -c tweets-2016.04.23.24.25.out
python stif_online_classification.py -c tweets-2016.03.21.22.23.out
python stif_online_classification.py -c tweets-2016.03.12.13.14.out

#ETAPE5 - Similarité BM25 entre journée info trafic et alertes classifiées ( par la tache precedente)
python bm25_impact_tweet.py -d 2016.05.29 --src stif_info_trafi.stif_info_trafic_05-29.out --target tweets-2016.05.28.29.30PRED_PROBA0.8.out
python bm25_impact_tweet.py -d 2016.05.15 --src stif_info_trafi.stif_info_trafic_05-15.out --target tweets-2016.05.14.15.16PRED_PROBA0.8.out
python bm25_impact_tweet.py -d 2016.04.24 --src stif_info_trafi.stif_info_trafic_04-24.out --target tweets-2016.04.23.24.25PRED_PROBA0.8.out
python bm25_impact_tweet.py -d 2016.03.22 --src stif_info_trafi.stif_info_trafic_03-22.out --target tweets-2016.03.21.22.23PRED_PROBA0.8.out
python bm25_impact_tweet.py -d 2016.03.13 --src stif_info_trafi.stif_info_trafic_03-13.out --target tweets-2016.03.12.13.14PRED_PROBA0.8.out


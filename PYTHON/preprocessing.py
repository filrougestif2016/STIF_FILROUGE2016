# -*- coding: utf-8 -*-
__author__ = 'catherine'

import numpy as np
import pandas as pd
import seaborn as sns
from sklearn import decomposition
from sklearn.utils import shuffle
from sklearn.cross_validation import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn import preprocessing
from sklearn.ensemble import GradientBoostingClassifier


names = ["Nearest Neighbors", "Decision Tree",
         "Random Forest", "AdaBoost", "Naive Bayes"  #, "RBF SVM", "Linear SVM"
         , "Gradient Boosting"
         ]
classifiers = [
    KNeighborsClassifier(2),
    DecisionTreeClassifier(max_depth=5),
    RandomForestClassifier(max_depth=10, n_estimators=15, max_features=5),
    AdaBoostClassifier(),
    GaussianNB()  #,
    # SVC(gamma=2, C=1), SVC(kernel="linear", C=0.025)
    , GradientBoostingClassifier()
]

sns.set_context("poster")
sns.set_palette("colorblind")

#
# Identifier les colonnes incomplètes
#
def nb_empty(df):
    result = pd.DataFrame(columns=['col_name', 'total_rows', 'nb_empty_rows'])
    for col in df.columns:
        df_col = df[[col]]
        df_col_dna = df_col.dropna()
        result.loc[len(result)] = [col, len(df_col), len(df_col) - len(df_col_dna)]
    return result


#
# Remplir les valeurs non renseignées d'une colonne par une constante
# Cette opération s'appliquera surtout aux colonnes catégorielle où
# l'on peut considérer que l'absence d'information est une information
#
def fill_na_col_with_cste(df, col_name, value):
    df[col_name] = df[[col_name]].fillna(value)


#
# Remplir les cellules non renseignées avec des valeurs "signifiantes"
# afin de conserver un nombre de lignes suffisamment conséquent pour
# l'apprentissage
#
def fill_na(df):
    # fill COUNTRY
    fill_na_col_with_cste(df, u'COUNTRY', 'WW')
    # fill SOURCE_BEGIN_MONTH
    fill_na_col_with_cste(df, u'SOURCE_BEGIN_MONTH', '--')
    # fill APP_NB
    fill_na_col_with_cste(df, u'APP_NB', -1.0)
    # fill APP_NB_PAYS
    fill_na_col_with_cste(df, u'APP_NB_PAYS', -1.0)
    # fill APP_NB_TYPE
    fill_na_col_with_cste(df, u'APP_NB_TYPE', -1.0)
    # fill FISRT_APP_COUNTRY
    fill_na_col_with_cste(df, u'FISRT_APP_COUNTRY', '--')
    # fill LANGUAGE_OF_FILLING
    fill_na_col_with_cste(df, u'LANGUAGE_OF_FILLING', '--')
    # fill INV_NB
    fill_na_col_with_cste(df, u'INV_NB', -1.0)
    # fill INV_NB_PAYS
    fill_na_col_with_cste(df, u'INV_NB_PAYS', -1.0)
    # fill INV_NB_TYPE
    fill_na_col_with_cste(df, u'INV_NB_TYPE', -1.0)
    # fill FISRT_INV_COUNTRY
    fill_na_col_with_cste(df, u'FISRT_INV_COUNTRY', '--')
    # fill cited_n
    fill_na_col_with_cste(df, u'cited_n', -1.0)
    # fill cited_nmiss
    fill_na_col_with_cste(df, u'cited_nmiss', -1.0)
    # fill cited_age_std
    fill_na_col_with_cste(df, u'cited_age_std', -1.0)
    # fill pct_NB_IPC_LY
    fill_na_col_with_cste(df, u'pct_NB_IPC_LY', -1.0)
    # fill PRIORITY_MONTH
    fill_na_col_with_cste(df, u'PRIORITY_MONTH', '-1/-1')


#
# Numérisation d'une colonne à données catégorielles
#
def num_col_category(df, col_name):
    df[col_name] = pd.factorize(df[col_name])[0]


#
# Numérisation d'une colonne de type MM/YYYY (mois/année)
#
def num_date(df, col_name):
    inter = pd.DataFrame()
    inter[['val1', 'val2']] = df[col_name].str.extract('([0-9]+|-1)\/([0-9]+|-1)')
    inter = inter.astype(int)
    inter['val2'] *= 100
    df[col_name] = inter['val2']+inter['val1']


#
# Numérisation de la colonne FIRST_CLASS
#
def num_first_class(df):
    inter = pd.DataFrame()
    inter[['val1', 'val2']] = df[u'FIRST_CLASSE'].str.extract('[0-9A-Z]{4}([0-9]+)\/([0-9]+)')
    inter = inter.astype('float')
    inter['val'] = inter['val1']*10000. + inter['val2']
    df[u'FIRST_CLASSE'] = inter['val']


#
# Numérisation complète du dataset
#
def numerize(df):
    num_col_category(df, u'VOIE_DEPOT')
    num_col_category(df, u'COUNTRY')
    num_col_category(df, u'SOURCE_BEGIN_MONTH')
    num_col_category(df, u'FISRT_APP_COUNTRY')
    num_col_category(df, u'FISRT_APP_TYPE')
    num_col_category(df, u'LANGUAGE_OF_FILLING')
    num_col_category(df, u'TECHNOLOGIE_SECTOR')
    num_col_category(df, u'TECHNOLOGIE_FIELD')
    num_col_category(df, u'MAIN_IPC')
    num_col_category(df, u'FISRT_INV_COUNTRY')
    num_col_category(df, u'FISRT_INV_TYPE')
    num_col_category(df, u'SOURCE_CITED_AGE')
    num_col_category(df, u'SOURCE_IDX_ORI')
    num_col_category(df, u'SOURCE_IDX_RAD')
    if u'VARIABLE_CIBLE' in df.columns:
        num_col_category(df, u'VARIABLE_CIBLE')
    num_date(df, u'PRIORITY_MONTH')
    num_date(df, u'FILING_MONTH')
    num_date(df, u'PUBLICATION_MONTH')
    num_date(df, u'BEGIN_MONTH')
    num_first_class(df)


#
# Separate X and y (training Dataset only)
#
def get_x_y(df, y_var_name):
    y = df[[y_var_name]]
    X = df[[col for col in df.columns if col != y_var_name]]
    return X, y



if __name__ == '__main__':
    df = pd.read_csv("train.csv", sep=";", encoding="utf-8")
    # remplir les cellules non renseignées avec des valeurs "signifiantes"
    fill_na(df)

    df_na_analyse = nb_empty(df)
    # print(df_na_analyse)

    fill_na(df)
    numerize(df)

    # print(len(df))
    df = df.dropna()
    df = shuffle(df).reset_index()
    # print(len(df))

    # récupérer entrées et sorties
    X, y = get_x_y(df, u'VARIABLE_CIBLE')

    # Analyse en composantes principales
    # X -= X.mean()
    pca = decomposition.IncrementalPCA(n_components=25)
    pca.fit(X)
    X = pca.transform(X)
    X = preprocessing.scale(X)
    # print(X.shape)

    # Créer les datasets de train, validation et test
    X_train, X_test, y_train, y_test = train_test_split(X, y.values, test_size=.4)
    X_test, X_valid, y_test, y_valid = train_test_split(X_test, y_test, test_size=.5)

    # print(X_train.shape)
    # print(X_valid.shape)
    # print(X_test.shape)

    # iterate over classifiers
    for name, clf in zip(names, classifiers):
        clf.fit(X_train, np.ravel(y_train))
        score = clf.score(X_valid, y_valid)
        score2 = clf.score(X_test, y_test)
        print name, score, score2

# -*- coding: utf-8 -*-

from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer, _document_frequency
import numpy as np
import scipy as sp

"""
 Creating a BM25Vectorizer class inherited from sklearn TfidfVectorizer
 Just adapt the transformer class
"""

class BM25Transformer(TfidfTransformer):

    def __init__(self, k1=1.5, b=0.75, norm='l2', use_idf=True, smooth_idf=True,
                 sublinear_tf=False):
        super(norm=norm, use_idf=use_idf, smooth_idf=smooth_idf,
                 sublinear_tf=sublinear_tf)
        self._k1 = k1
        self._b = b

    def fit(self, X, y=None):
        """Learn the bm25 vector (global term weights)
        Parameters
        ----------
        X : sparse matrix, [n_samples, n_features]
            a matrix of term/token counts
        """
        if not sp.issparse(X):
            X = sp.csc_matrix(X)
        if self.use_idf:
            n_samples, n_features = X.shape
            df = _document_frequency(X)

            # perform idf smoothing if required
            df += int(self.smooth_idf)
            n_samples += int(self.smooth_idf)

            # log+1 instead of log makes sure terms with zero idf don't get
            # suppressed entirely.
            idf = np.log((float(n_samples) - df + 0.5) / (df + 0.5))
            self._idf_diag = sp.spdiags(idf,
                                        diags=0, m=n_features, n=n_features)

        return self
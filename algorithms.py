# -*- coding: utf-8 -*-
#
# algorithms.py
#
# The module is part of model_comparison.
#

"""
Representations of algorithms.
"""

__author__ = 'author 1', 'author 2'
__email__ = 'email1', 'email2'

from scipy import linalg
import scipy as sp
from sklearn import linear_model
import numpy as np

class OLS:
    """The ordinary least squares algorithm"""
    #import numpy as np

    def __init__(self, lmd = 0,random_state=None):

        self.random_state = random_state
        self.lmd = lmd

        # NOTE: Varialbe set with fit method.
        self.beta = None

    def fit(self, X, y):
        """Train the model"""
        self.beta = sp.linalg.inv(X.T @ X)@ X.T @ y

    def predict(self, X):
        """Aggregate model predictions """
        return X @ self.beta

               #print(y)
        #term1 =  np.dot(X.T, y)
        #term2 = np.dot(self.lmd*np.identity(len(y)), np.dot(X.T, y))
        #print(term2.shape)
class Ridge:
    """The Ridge algorithm."""
    #import numpy as np

    def __init__(self, lmd, random_state=None):
        self.lmd = lmd
        self.random_state = random_state

        # NOTE: Varible set wtih fit method.
        self.beta = None

    def fit(self, X, y):
        """Train the model."""

        self.beta = linalg.inv(X.T@ X - self.lmd*np.identity(X.shape[1])@X.T@y)

    def predict(self, X):
        """Aggregate model predictions."""
        return X @ self.beta


class Lasso:
    """The LASSO algorithm."""
    # when the first column is 1 the use fit_intercept = True.

    def __init__(self, lmd, random_state=None):
        self.lmd = lmd
        self.random_state = random_state
        self.model = None

    def fit(self, X, y):
        """Train the model."""
        self.model = linear_model.Lasso(self.lmd)
        self.model.fit(X, y)

        return self

    def predict(self, X):
        """Aggregate model predictions."""

        return self.model.predict(X)

"""
Various functions and classes made while developing
pipelines and/or cleaning data.
"""
from typing import List

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler

import pandas as pd


class EquipmentScaler(BaseEstimator, TransformerMixin):
    """
    Scaler meant to except columns from the equipment
    data set.
    """
    def __init__(self, attr_names: List) -> None:
        """
        Constructor takes a list of column headers
        to be passed into the dataframe.
        """
        self.attr_names = attr_names

    def fit(self, X: pd.core.frame.DataFrame) -> 'EquipmentScaler':
        """
        Made available for use in fit_transform.
        """
        return self

    def transform(self, X):
        """
        Apply the standard scaler to the selected columns
        of the copied dataframe.
        """
        X_copy = X.copy()
        scaler = StandardScaler()
        X_copy[self.attr_names] = scaler.fit_transform(X_copy[self.attr_names].values)
        return X_copy

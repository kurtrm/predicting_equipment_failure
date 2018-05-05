"""
Various functions and classes made while developing
pipelines and/or cleaning data.
"""
from typing import List, Text


from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler, LabelBinarizer

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

    def transform(self, X: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
        """
        Apply the standard scaler to the selected columns
        of the copied dataframe.
        """
        X_copy = X.copy()
        scaler = StandardScaler()
        X_copy[self.attr_names] = scaler.fit_transform(X_copy[self.attr_names].values)
        return X_copy


class TargetBinarizer(BaseEstimator, TransformerMixin):
    """
    Scaler meant to except columns from the equipment
    data set.
    """
    def __init__(self, target_name: Text) -> None:

        """
        Constructor takes the target name
        to be passed into the dataframe.
        """
        self.target_name = target_name

    def fit(self, X: pd.core.frame.DataFrame) -> 'TargetBinarizer':
        """
        Made available for use in fit_transform.
        """
        return self

    def transform(self, X: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
        """
        Apply the label binarizer to the target column.
        """
        X_copy = X.copy()
        binarizer = LabelBinarizer()
        X_copy[self.target_name] = binarizer.fit_transform(X_copy[self.target_name].values)
        return X_copy


class NameChanger(BaseEstimator, TransformerMixin):
    """
    Change column headers to better more readable names.
    """
    def __init__(self, column_names: List=None) -> None:
        """
        Take the list of column_names as an optional argument.
        """
        if column_names is None:
            self.column_names = ['date', 'temp', 'humidity',
                                 'Operator', 'Measure1', 'Measure2',
                                 'Measure3', 'Measure4', 'Measure5',
                                 'Measure6', 'Measure7', 'Measure8',
                                 'Measure9', 'Measure10', 'Measure11',
                                 'Measure12', 'Measure13', 'Measure14',
                                 'Measure15', 'hours_since_prev_fail',
                                 'failure', 'year', 'month', 'day-of-month',
                                 'day-of-week', 'hour', 'minute', 'second']
        else:
            self.column_names = column_names

    def fit(self, X: pd.core.frame.DataFrame) -> 'NameChanger':
        """
        Fit made available for fit_transform.
        """
        return self

    def transform(self, X: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
        """
        Change the column headers to better names.
        """
        X_copy = X.copy()
        X_copy.columns = self.column_names
        return X_copy


class MakeDummies(BaseEstimator, TransformerMixin):
    """
    For categorical features, make dummies and
    concatentate them with the original dataframe.
    """
    def __init__(self, attr_names: List) -> None:

        """
        Takes a list of attr_names and col_names.
        The order of the column names should correspond
        to the expected ordering of the dummie columns.
        Assumes the user has done preliminary data exploration.
        """
        self.attr_names = attr_names
        self._daysofweek = ['Monday',
                            'Tuesday',
                            'Wednesday',
                            'Thursday',
                            'Friday', 'Saturday', 'Sunday']


    def fit(self, X: pd.core.frame.DataFrame) -> 'MakeDummies':
        """
        Made available for fit_transform.
        """
        return self

    def transform(self, X: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
        """
        Transform the selected columns into separate binary columns,
        drop the originals, and concatenate them to the original dataframe.
        """
        X_copy = X.copy()
        dummies = pd.get_dummies(X_copy, columns=self.attr_names)
        if 'day-of-week' in self.attr_names:
            dummies = dummies.rename(columns={f'day-of-week_{i}': day
                                              for i, day in enumerate(self._daysofweek, 1)})
        if 'Operator' in self.attr_names:
            dummies = dummies.rename(columns={f'Operator_Operator{i}': f'Operator{i}'
                                              for i in range(1, 9)})
        return dummies


class DropColumns(BaseEstimator, TransformerMixin):
    """
    Drop columns from the final transformed df.
    """
    def __init__(self, column_names: List) -> None:
        """
        Return a dataframe that drops the columns.
        """
        self.column_names = column_names

    def fit(self, X: pd.core.frame.DataFrame) -> 'MakeDummies':
        """
        Made available for fit_transform.
        """
        return self

    def transform(self, X: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
        """
        Drop the columns.
        """
        X_copy = X.copy()
        return X_copy.drop(self.column_names, axis=1)

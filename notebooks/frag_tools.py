"""
Various functions and classes made while developing
pipelines and/or cleaning data.
"""
import json
from typing import List, Text, Callable
import yaml

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler, LabelBinarizer

import googlemaps
import pandas as pd

# ================== Transformer ==========================


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


class BackupMakeDummies(BaseEstimator, TransformerMixin):
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

    def fit(self, X: pd.core.frame.DataFrame) -> 'DropColumns':
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


class AddressLatLong(BaseEstimator, TransformerMixin):
    """
    Transformer to turn all of the current lat/longs
    to their actual lat/longs.
    """
    def fit(self, X: pd.core.frame.DataFrame) -> 'AddressLatLong':
        """
        Made available for fit_transform.
        """
        return self

    def transform(self, X: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
        """
        Extract json from file and replace the
        latitude and longitude columns in the dataframe.
        """
        X_copy = X.copy()
        path_all = '/mnt/c/Users/kurtrm/' \
                   'projects/predicting_equipment_failure/' \
                   'src/static/data/geocoded_address.json'
        path_corrected = '/mnt/c/Users/kurtrm/' \
                         'projects/predicting_equipment_failure/' \
                         'src/static/data/corrected_addresses.json'
        with open(path_all, 'r') as f:
            geocoded_all = json.load(f)
        with open(path_corrected, 'r') as f:
            geocoded_corrected = json.load(f)
        lat_longs = pd.DataFrame([location[0]['geometry']['location']
                                 for location in geocoded_all])
        X_copy[['Latitude', 'Longitude']] = lat_longs
        # Below, these addresses are hard coded corrections to lat_longs
        # Indices of bad addresses
        bad_addresses = [12, 15, 47, 107, 218, 227, 254, 381, 383, 386, 396,
                         423, 518, 521, 562, 570, 592, 656, 700, 727, 805, 969,
                         1038, 1092, 1121, 1207, 1251, 1273, 1360, 1384, 1387,
                         1403, 1424, 1462, 1464, 1671]
        corrected = [location['geometry']['location']
                     for location in geocoded_corrected]
        for bad_address, correction in zip(bad_addresses, corrected):
            X_copy.at[bad_address, ['Latitude', 'Longitude']] = correction['lat'], correction['lng']

        return X_copy


class CleanAddresses(BaseEstimator, TransformerMixin):
    """
    Take the addresses from the raw dataframe and combine them.
    """
    def fit(self, X: pd.core.frame.DataFrame) -> 'CleanAddresses':
        """
        Made available for fit_transform.
        """
        return self

    def transform(self, X: pd.core.frame.DataFrame, geocode: bool=False) -> pd.core.frame.DataFrame:
        """
        Combine the address columns.
        """
        X_copy = X.copy()
        location_info = X_copy[['AssetLocation',
                                'AssetCity',
                                'AssetState',
                                'AssetZip']]
        joined_series = location_info.apply(lambda x: ", ".join(x.tolist()),
                                            axis=1)
        if geocode:
            geocode_data(joined_series.tolist(), to_file=geocode)

        return joined_series


class Binarize(BaseEstimator, TransformerMixin):
    """
    Binarize columns.
    """
    def __init__(self, attr_names: List) -> None:
        """
        Initialize with the names of the attributes to
        apply the transformation.
        """
        self.attr_names = attr_names

    def fit(self, X: pd.core.frame.DataFrame) -> 'Binarize':
        """
        Made available for fit_transform.
        """
        return self

    def transform(self, X: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
        """
        Binarize the attr_names columns to 0 and 1.
        """
        X_copy = X.copy()
        X_copy[self.attr_names] = X_copy[['VegMgmt',
                                          'PMLate',
                                          'WaterExposure',
                                          'MultipleConnects',
                                          'Storm']].applymap(lambda x: 1 if 'Y' in x else 0)
        return X_copy


class CurrentMakeDummies(BaseEstimator, TransformerMixin):
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

    def fit(self, X: pd.core.frame.DataFrame) -> 'CurrentMakeDummies':
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

        return dummies


class ChangeTypes(BaseEstimator, TransformerMixin):
    """
    Change the types of columns
    """
    def __init__(self, attr_names: List, funcs: List[Callable]) -> None:
        """
        Accepts a list of the column names to change.
        The types must be in the same order as the column names.
        """
        self.attr_names = attr_names
        self.funcs = funcs

    def fit(self, X: pd.core.frame.DataFrame) -> 'ChangeTypes':
        """
        Made available for fit_transform.
        """
        return self

    def transform(self, X: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
        """
        Transform the the dataframe columns into self.types.
        """
        X_copy = X.copy()
        for column, func in zip(self.attr_names, self.funcs):
            X_copy[column] = X_copy[column].apply(func)

        return X_copy

# ================ Functions =======================


def geocode_data(addresses: List, to_file: bool=False) -> List:
    """
    Take a list of addresses and convert them to
    lat/longs via the googlemaps geocoding API.
    """
    with open('/home/kurtrm/.secrets/geocoding.yaml', 'r') as f:
        key = yaml.load(f)
    gmaps = googlemaps.Client(key=key['API_KEY'])
    geocoded = [gmaps.geocode(address) for address in addresses]
    if to_file:
        path = '/mnt/c/Users/kurtrm/' \
               'projects/predicting_equipment_failure/' \
               'src/static/data/geocoded_address.json'
        with open(path, 'w') as f:
            json.dump(geocoded, f)

    return geocode_data


def custom_zip_cleaning(zipcode: int) -> int:
    """
    Takes a zipcode from the transformer dataset
    and makes it an intent:
    """
    try:
        return int(zipcode[:5])
    except ValueError:
        return 30189

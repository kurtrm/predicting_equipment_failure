"""
Various functions that compute metrics on the model.
"""
from sklearn.metrics import (roc_auc_score,
                             precision_recall_fscore_support,
                             accuracy_score)
from sklearn.externals import joblib
import numpy as np

from scripts import db
from scripts.profit_curve import threshold_prediction


model = joblib.load('static/models/final_grad_boost.pkl')
threshold = db.select_threshold()[0] / 100
fetched = db.fetch_test_data()
test_set = np.array(fetched)[:, 1:]
X_test, y_test = test_set[:, :-1], test_set[:, -1]
y_score = model.predict_proba(X_test)[:, 1]
y_threshold_score = threshold_prediction(model, X_test, threshold)


def get_auc_score():
    """
    Use sklearn roc_auc_score to compute auc.
    """
    return roc_auc_score(y_test, y_score)


def precision_recall_f1():
    """
    Wraps sklearn's precision_recall_f1_support function.
    """
    return precision_recall_fscore_support(y_test,
                                           y_threshold_score,
                                           average='binary')


def accuracy():
    """
    Wrap sklearn's accuracy function.
    """
    return accuracy_score(y_test, y_threshold_score)

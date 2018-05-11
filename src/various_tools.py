"""
I'm putting tools devised in Jupyter notebooks into
this file.
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import cross_val_score


def roc(model, X_test, y_test):
    """
    Compute TPRs and FPRs for ROC curve.
    """
    probs = model.predict_proba(X_test)[:, 1]
    sorted_probs = np.sort(probs)
    actual_pos = len(y_test[y_test == 1])
    actual_neg = len(y_test) - actual_pos
    fprs = np.empty(len(y_test))
    tprs = np.empty(len(y_test))
    for i, prob in enumerate(np.linspace(0, 1, len(sorted_probs))):
        partition = y_test[probs > prob]
        true_positives = len(partition[partition == 1])
        false_positives = len(partition[partition == 0])
        true_pos_rate = true_positives / actual_pos
        false_pos_rate = false_positives / actual_neg
        tprs[i] = true_pos_rate
        fprs[i] = false_pos_rate

    return tprs, fprs


def plot_roc(model, X_test, y_test, ax=None):
    """
    Compute ROC and AUC and graph.
    """
    if ax is None:
        fig, ax = plt.subplots()
    tprs, fprs = roc(model, X_test, y_test)
    ax.plot(fprs, tprs)
    ax.set_title('ROC Curve')
    ax.set_ylabel('True Positive Rate')
    ax.set_xlabel('False Positive Rate')


def cross_val_metrics(model, X_test, y_test, metrics):
    """
    Return metrics of the given model in a dictionary.
    """
    metrics_dict = {}
    for metric in metrics:
        scores = cross_val_score(model, X_test, y_test, scoring=metric, cv=5)
        metrics_dict[metric] = scores.mean()
    return metrics_dict


def make_metric_df(models: list, X_train: np.ndarray, y_train: np.ndarray, metrics: list) -> 'DataFrame':
    """
    Return a dataframe with the indices as the metrics and the columns as the models.
    """
    dataframe_dict = {}
    for model in models:
        score = cross_val_metrics(model, X_train, y_train, metrics)
        dataframe_dict[model.__class__.__name__] = score
    return pd.DataFrame(dataframe_dict)


def make_trained_metric_df(models: list, X_test: np.ndarray, y_test: np.ndarray, metrics: list) -> 'DataFrame':
    """
    Return a dataframe with the indices as the metrics and the columns as the models.
    """
    dataframe_dict = {}
    for model in models:
        score = cross_val_metrics(model, X_test, y_test, metrics)
        dataframe_dict[model.__class__.__name__] = score
    return pd.DataFrame(dataframe_dict)

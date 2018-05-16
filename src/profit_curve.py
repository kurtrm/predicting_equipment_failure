"""
Rough outline of how I want to display
the actual profit curve.
"""
import numpy as np
import pandas as pd
"""
X-axis: thresholds (0-1.0)
y-axis: profits (large integers)

Using the trained model, the test data, and a given threshold
calculate the confusion matrix



Have a cost confusion matrix consisting of the costs.
So:

 Actual ->          [Failure | Nominal]
 Predicted [Failure]   -100     -100
     |
     |     [Nominal]   -1000      0

-The cost of repair and failure would each have their own slide bar
-When the slide bar is changed, the values in this matrix would change

Multiply the cost matrix by the confusion matrix to get dollar values.
For each threshold, perform the previous step and sum the resulting matrix
Pass to D3 to graph

Actual ->          [Failure | Nominal]
 Predicted [Failure]   -100      0
     |
     |     [Nominal]   -1000     100

 Assume 1 hour equates to $100 revenue
 Repair costs $100 upfront
 Failure costs $1000
"""


def threshold_prediction(model, X, threshold=0.5):
    """
    Return predictions based on threshold.
    This code comes from class notes with modifications.
    """
    return np.where(model.predict_proba(X)[:, 1] > threshold,
                    model.classes_[1],
                    model.classes_[0])


def confusion_matrix(model, X_test, y_test, threshold=0.5):
    cf = pd.crosstab(y_test, threshold_prediction(model, X_test, threshold))
    cf.index.name = 'actual'
    cf.columns.name = 'predicted'
    return cf.values


def generate_cost_matrix(revenue, maintenance, repair):
    """
    Calculate the cost_matrix based on how much a transformer
    generates revenue, costs to maintain, and costs to repair.
    """
    return np.array([[maintenance, repair],
                     [maintenance, revenue]])


def sum_payout(cost_matrix, confusion_matrix):
    """
    Calculate the profit from cost and confusion matrices.
    """
    return (confusion_matrix * cost_matrix).sum()


def generate_profit_curve(cost_matrix,
                          model,
                          X_test, y_test, n_thresholds=100):
    """
    Generate the profit curve with a given cost matrix.
    """
    thresholds = np.linspace(0, 1, n_thresholds)
    totals = []
    thresholds_idx = []
    minimum = float('inf')
    for idx, threshold in enumerate(thresholds):
        iter_conf_matrix = confusion_matrix(model, X_test, y_test, threshold)
        payout = sum_payout(cost_matrix, iter_conf_matrix)
        if payout <= minimum:
            minimum = payout
        else:
            thresholds_idx.append(idx)
            totals.append(payout)

    return thresholds[thresholds_idx].tolist(), totals

"""
Module containing a class that provides a convenient interface
for computing ROC/AUC and plotting the results.
"""
import json

import numpy as np


class ROC:
    """
    Provides an interace to compute ROC and AUC,
    and to plot their graphs.
    """
    def __init__(self, probabilities: np.ndarray, labels: np.ndarray) -> None:
        """
        Initialize ROC/AUC, takes an array of probabilities
        and an array of labels (actual values).
        """
        self.probabilities = probabilities
        self.labels = labels
        self.conf_matrix_vals = None

    def roc(self) -> tuple:
        """
        Calculate the Receiver Operating Characteristics
        for the data and make it a property.
        """
        sorted_probs = np.sort(self.probabilities)
        actual_pos = len(self.labels[self.labels == 1])
        actual_neg = len(self.labels) - actual_pos
        conf_matrix_vals = np.empty((len(self.labels), 6))  # 6 corresponds to:
        for i, prob in enumerate(sorted_probs):  # tpr, fpr, tp, fp, tn, fn
            pos_partition = self.labels[self.probabilities >= prob]
            neg_partition = self.labels[self.probabilities < prob]
            tp = len(pos_partition[pos_partition == 1])
            fp = len(pos_partition[pos_partition == 0])
            tn = len(neg_partition[neg_partition == 1])
            fn = len(neg_partition[neg_partition == 0])
            tpr = tp / actual_pos
            fpr = fp / actual_neg
            conf_matrix_vals[i] = tpr, fpr, tp, fp, tn, fn
        self.conf_matrix_vals = conf_matrix_vals

        return self.conf_matrix_vals

    def to_json(self, filename: str) -> None:
        """
        Convert conf_matrix_vals to json.
        First checks if self.roc() as been called. If not,
        calls it. Drops the file in the current directory.
        """
        if self.conf_matrix_vals is None:
            arr = self.roc()
        else:
            arr = self.conf_matrix_vals
        list_o_dicts = [{"tpr": column[0],
                         "fpr": column[1],
                         "tp": column[2],
                         "fp": column[3],
                         "tn": column[4],
                         "fn": column[5]} for column in arr]
        with open(filename, 'w') as f:
            json.dump(list_o_dicts, f)

    # def auc(self, method: str='scratch') -> float:
    #     """
    #     Calculate the Area Under the Curve for the ROC.
    #     For fun, the user can choose one of three ways to calculate
    #     it.

    #     Parameters
    #     ----------
    #     method -> str: User can choose between 'scratch', 'sklearn',
    #     and 'scipy'. 'scratch' returns a score from an implementation
    #     made from scratch. 'sklearn' returns a score from sklearn's
    #     roc_auc_score. 'scipy' returns the auc from the scipy.integrate.trapz
    #     function.

    #     Returns
    #     -------
    #     float auc score.
    #     """
    #     TPRs, FPRs = self.roc
    #     if method == 'scratch':
    #         return self._scratch_riemann(TPRs, FPRs)
    #     elif method == 'sklearn':
    #         return auc(FPRs, TPRs)
    #     else:
    #         return -trapz(TPRs, FPRs)  # Why negative? Dunno.

    # def _scratch_riemann(self, tprs: np.ndarray, fprs: np.ndarray) -> float:
    #     """
    #     Private method for calculating a rough value for the
    #     auc.

    #     Parameters
    #     ----------
    #     tprs -> np.array: array of true positive rates.
    #     fprs -> np.array: array of false positive rates.

    #     Returns
    #     -------
    #     total -> float of auc score
    #     """
    #     total = 0
    #     p_tpr, p_fpr = 0, 0
    #     for tpr, fpr in zip(tprs, fprs):
    #         total += (tpr - p_tpr) * (fpr - p_fpr)
    #         p_tpr, p_fpr = tpr, fpr

    #     return total

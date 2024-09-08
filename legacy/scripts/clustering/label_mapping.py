# label_mapping.py
import numpy as np
from scipy.optimize import linear_sum_assignment

def map_labels(scipy_labels, sklearn_labels):
    """Map SciPy labels to match scikit-learn labels."""
    max_label = max(scipy_labels.max(), sklearn_labels.max()) + 1

    contingency_matrix = np.zeros((max_label, max_label), dtype=int)

    for scipy_label, sklearn_label in zip(scipy_labels, sklearn_labels):
        contingency_matrix[scipy_label, sklearn_label] += 1

    row_ind, col_ind = linear_sum_assignment(-contingency_matrix)

    label_mapping = {row: col for row, col in zip(row_ind, col_ind)}

    mapped_scipy_labels = np.array([label_mapping[label] for label in scipy_labels])

    return mapped_scipy_labels

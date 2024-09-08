import numpy as np
from scipy.optimize import linear_sum_assignment

def map_labels(scipy_labels, sklearn_labels):
    """Map SciPy labels to match scikit-learn labels."""
    scipy_labels = np.array(scipy_labels).flatten()  # Flatten the labels to 1D arrays
    sklearn_labels = np.array(sklearn_labels).flatten()  # Flatten the labels to 1D arrays

    max_label = int(max(scipy_labels.max(), sklearn_labels.max())) + 1  # Ensure max_label is an integer

    contingency_matrix = np.zeros((max_label, max_label), dtype=int)

    # Populate the contingency matrix
    for scipy_label, sklearn_label in zip(scipy_labels, sklearn_labels):
        contingency_matrix[int(scipy_label), int(sklearn_label)] += 1

    # Apply the Hungarian algorithm to find the best label mapping
    row_ind, col_ind = linear_sum_assignment(-contingency_matrix)

    # Create a mapping from SciPy labels to sklearn labels
    label_mapping = {row: col for row, col in zip(row_ind, col_ind)}

    # Map the SciPy labels to match the scikit-learn labels
    mapped_scipy_labels = np.array([label_mapping[int(label)] for label in scipy_labels])

    return mapped_scipy_labels

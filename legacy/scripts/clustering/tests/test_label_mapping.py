# tests/test_label_mapping.py
import unittest
import numpy as np
from ConceptX.label_mapping import map_labels

class TestLabelMapping(unittest.TestCase):

    def test_map_labels(self):
        sklearn_labels = np.array([0, 1, 1, 0, 2, 2])
        scipy_labels = np.array([2, 0, 0, 2, 1, 1])

        # Map labels
        mapped_scipy_labels = map_labels(scipy_labels, sklearn_labels)

        # Check if they are mapped correctly
        self.assertTrue(np.array_equal(mapped_scipy_labels, sklearn_labels))

if __name__ == '__main__':
    unittest.main()

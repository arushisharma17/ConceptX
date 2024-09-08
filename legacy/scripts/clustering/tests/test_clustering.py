# tests/test_clustering.py
import unittest
import numpy as np
from ConceptX.clustering import perform_agglomerative_clustering, create_linkage_matrix

class TestClustering(unittest.TestCase):

    def test_perform_agglomerative_clustering(self):
        points = np.random.rand(100, 5)
        clustering = perform_agglomerative_clustering(points, K=5)

        # Test labels shape
        self.assertEqual(len(clustering.labels_), 100)

        # Test number of unique clusters
        self.assertEqual(len(set(clustering.labels_)), 5)

    def test_create_linkage_matrix(self):
        points = np.random.rand(100, 5)
        linkage_matrix = create_linkage_matrix(points, output_path='./', K=5)

        # Test linkage matrix shape
        self.assertEqual(linkage_matrix.shape, (99, 4))

if __name__ == '__main__':
    unittest.main()

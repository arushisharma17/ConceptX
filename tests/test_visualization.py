# tests/test_visualization.py
import unittest
import os
import numpy as np
from clustering.visualization import plot_dendrogram, plot_clusters

class TestVisualization(unittest.TestCase):

    def test_plot_dendrogram(self):
        points = np.random.rand(100, 5)
        linkage_matrix = np.random.rand(99, 4)  # Random linkage matrix

        plot_dendrogram(linkage_matrix, output_path='./')

        # Check if the file was created
        self.assertTrue(os.path.exists('./dendrogram.png'))

    def test_plot_clusters(self):
        points = np.random.rand(100, 5)
        labels = np.random.randint(0, 5, 100)

        plot_clusters(points, labels, output_path='./', method='pca')

        # Check if the file was created
        self.assertTrue(os.path.exists('./clusters_pca.png'))

if __name__ == '__main__':
    unittest.main()

import unittest
import numpy as np
from scipy.cluster.hierarchy import linkage, fcluster  # Use fcluster for converting linkage matrix to labels

from clustering.synthetic_data import generate_synthetic_data
from clustering.agglomerative import perform_agglomerative_clustering, create_linkage_matrix
from clustering.visualization import plot_dendrogram, plot_clusters
from clustering.logger import log_start_time, log_end_time, log_input_data_summary, log_clustering_params, log_cluster_summary
from clustering.label_mapping import map_labels

class TestPipeline(unittest.TestCase):

    def test_pipeline(self):
        output_file = "test_pipeline_log.txt"
        output_path = "./test_output"
        K = 5  # Number of clusters

        # Step 1: Generate synthetic data
        points, vocab = generate_synthetic_data(num_points=100, num_dims=5)

        # Step 2: Log the environment and input data
        log_start_time(output_file)
        log_input_data_summary(points, vocab, output_file)
        log_clustering_params(K, output_file)

        # Step 3: Perform clustering using sklearn
        clustering = perform_agglomerative_clustering(points, K)

        # Step 4: Perform clustering using scipy
        linkage_matrix = create_linkage_matrix(points, output_path, K)
        plot_dendrogram(linkage_matrix, output_path)

        # Convert the linkage matrix to cluster labels
        scipy_labels = fcluster(linkage_matrix, t=K, criterion='maxclust')

        # Step 5: Map the labels and compare sklearn and scipy clustering
        mapped_scipy_labels = map_labels(scipy_labels, clustering.labels_)

        # Log the cluster summary
        clusters = {i: vocab[clustering.labels_ == i].tolist() for i in range(K)}
        log_cluster_summary(clusters, output_file)

        # Step 6: Verify if labels from both methods match closely
        similarity_score = np.mean(mapped_scipy_labels == clustering.labels_)
        self.assertTrue(similarity_score > 0.9, "Cluster labels do not match closely enough")

        # Step 7: Visualize the results
        plot_clusters(points, mapped_scipy_labels, output_path, method="pca")
        plot_clusters(points, clustering.labels_, output_path, method="tsne")

        log_end_time(output_file)

if __name__ == '__main__':
    unittest.main()

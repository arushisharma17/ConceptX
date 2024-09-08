import numpy as np
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import linkage, fcluster  # Added fcluster import
from collections import defaultdict
import dill as pickle
import time
import os  # Added to handle directories
from datetime import datetime
from .logger import log_start_time, log_end_time, log_runtime, log_cluster_summary, log_environment, log_input_data_summary
from .synthetic_data import generate_synthetic_data, save_synthetic_data
from .visualization import plot_dendrogram, plot_clusters
from .label_mapping import map_labels

output_file = "memory-profile-agg.txt"

def perform_agglomerative_clustering(points, K):
    """Perform agglomerative clustering using sklearn."""
    return AgglomerativeClustering(n_clusters=K, compute_distances=True).fit(points)

def create_linkage_matrix(points, output_path, K):
    """Create and save the linkage matrix using scipy."""
    # Ensure the output path exists
    os.makedirs(output_path, exist_ok=True)

    linkage_matrix = linkage(points, method='ward')
    np.save(f"{output_path}/agg_linkage_matrix_{K}.npy", linkage_matrix)
    return linkage_matrix



def agglomerative_cluster(points, vocab, K, output_path, ref=''):
    """Perform clustering and log details."""
    # Log start time and environment
    log_start_time(output_file)
    log_environment(output_file)
    log_input_data_summary(points, vocab, output_file)

    # Perform clustering with sklearn
    start_time = time.time()
    clustering = perform_agglomerative_clustering(points, K)
    end_time = time.time()
    log_runtime(start_time, end_time, output_file)

    # Perform clustering with scipy for comparison
    linkage_matrix = linkage(points, method='ward')
    scipy_labels = fcluster(linkage_matrix, t=K, criterion='maxclust')

    # Map SciPy labels to match sklearn labels
    mapped_scipy_labels = map_labels(scipy_labels, clustering.labels_)

    # Log cluster results summary
    clusters = defaultdict(list)
    for i, label in enumerate(mapped_scipy_labels):
        clusters[label].append(vocab[i])

    log_cluster_summary(clusters, output_file)

    # Save the results
    save_clustering_results(clustering, clusters, output_path, K, ref)

    log_end_time(output_file)

    return mapped_scipy_labels, clustering.labels_

def save_clustering_results(clustering, clusters, output_path, K, ref):
    """Save clustering results and clusters."""
    # Ensure output directory exists
    os.makedirs(output_path, exist_ok=True)

    model_file = f"{output_path}/model-{K}-agglomerative-clustering{ref}.pkl"
    with open(model_file, "wb") as fp:
        pickle.dump(clustering, fp)

    cluster_output = "\n".join([f"{word}|||{key}" for key, words in clusters.items() for word in words])
    cluster_file = f"{output_path}/clusters-agg-{K}{ref}.txt"
    with open(cluster_file, 'w') as f:
        f.write(cluster_output)

def main():
    """Main function to execute agglomerative clustering and save results."""
    # Generate synthetic data for testing
    points, vocab = generate_synthetic_data(num_points=100, num_dims=5, vocab_size=100)
    save_synthetic_data(points, vocab, point_file='synthetic_points.npy', vocab_file='synthetic_vocab.npy')

    # Now you can run the rest of the script on these synthetic files
    vocab_file = 'synthetic_vocab.npy'
    point_file = 'synthetic_points.npy'
    output_path = './output'
    cluster = 5

    # Load vocab and points
    vocab = np.load(vocab_file)
    points = np.load(point_file)

    # Create linkage matrix and visualize dendrogram
    linkage_matrix = create_linkage_matrix(points, output_path, cluster)
    plot_dendrogram(linkage_matrix, output_path)

    # Perform agglomerative clustering and visualize the clusters
    mapped_scipy_labels, sklearn_labels = agglomerative_cluster(points, vocab, cluster, output_path)
    plot_clusters(points, mapped_scipy_labels, output_path, method="pca")

    # Compare mapped SciPy labels and scikit-learn labels
    print("Mapped SciPy Labels:", mapped_scipy_labels)
    print("Scikit-learn Labels:", sklearn_labels)

    if np.array_equal(mapped_scipy_labels, sklearn_labels):
        print("The mapped SciPy labels match the scikit-learn labels.")
    else:
        print("The labels are different, check the mapping.")

# This ensures the script runs when executed directly
if __name__ == "__main__":
    main()

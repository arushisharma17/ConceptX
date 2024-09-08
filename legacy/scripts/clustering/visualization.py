import os
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

def plot_dendrogram(linkage_matrix, output_path):
    """Plot a dendrogram from the linkage matrix."""
    os.makedirs(output_path, exist_ok=True)  # Ensure the output path exists
    plt.figure(figsize=(10, 7))
    dendrogram(linkage_matrix)
    plt.title("Hierarchical Clustering Dendrogram")
    plt.xlabel("Sample index")
    plt.ylabel("Distance")
    plt.savefig(f"{output_path}/dendrogram.png")
    plt.show()

def plot_clusters(points, labels, output_path, method="pca"):
    """Plot clusters in 2D using PCA or t-SNE."""
    os.makedirs(output_path, exist_ok=True)  # Ensure the output path exists

    # Select dimensionality reduction method
    if method == "pca":
        reducer = PCA(n_components=2)
    elif method == "tsne":
        reducer = TSNE(n_components=2, random_state=42)
    else:
        raise ValueError("Method must be 'pca' or 'tsne'")

    # Apply dimensionality reduction
    reduced_points = reducer.fit_transform(points)

    # Plot clusters
    plt.figure(figsize=(10, 7))
    plt.scatter(reduced_points[:, 0], reduced_points[:, 1], c=labels, cmap='viridis', s=50, alpha=0.7)
    plt.title(f"Cluster Visualization ({method.upper()})")
    plt.savefig(f"{output_path}/clusters_{method}.png")
    plt.show()

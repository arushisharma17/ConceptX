import sys
import platform
import numpy as np
from datetime import datetime

def log_environment(output_file):
    """Log system, environment, and library details."""
    env_info = (
        f"Python Version: {sys.version}\n"
        f"NumPy Version: {np.__version__}\n"
        f"SciKit-Learn Version: {sklearn.__version__}\n"
        f"System: {platform.system()} {platform.release()}\n"
        f"Processor: {platform.processor()}\n"
        f"Machine: {platform.machine()}\n"
    )
    with open(output_file, "a") as f:
        f.write(env_info)

def log_input_data_summary(points, vocab, output_file):
    """Log input data summary."""
    input_summary = f"Points Shape: {points.shape}\nVocab Size: {len(vocab)}\n"
    with open(output_file, "a") as f:
        f.write(input_summary)

def log_clustering_params(K, output_file):
    """Log clustering parameters."""
    clustering_params = f"Number of Clusters: {K}\nDistance Metric: Euclidean\nLinkage: Ward\n"
    with open(output_file, "a") as f:
        f.write(clustering_params)

def log_start_time(output_file):
    """Log start time of the process."""
    start_time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(output_file, "a") as f:
        f.write(f"Start Time: {start_time_str}\n")

def log_end_time(output_file):
    """Log end time of the process."""
    end_time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(output_file, "a") as f:
        f.write(f"End Time: {end_time_str}\n")

def log_runtime(runtime, output_file):
    """Log runtime of the clustering process."""
    with open(output_file, "a") as f:
        f.write(f"Clustering Runtime: {runtime:.2f} seconds\n")

def log_cluster_summary(clusters, output_file):
    """Log a summary of the clusters."""
    cluster_summary = "Cluster Summary:\n"
    for cluster_id, members in clusters.items():
        cluster_summary += f"Cluster {cluster_id}: {len(members)} items\n"
    with open(output_file, "a") as f:
        f.write(cluster_summary)

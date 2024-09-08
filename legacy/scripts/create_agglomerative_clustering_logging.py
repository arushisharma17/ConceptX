import numpy as np
import sklearn
from sklearn.cluster import AgglomerativeClustering
from collections import defaultdict
import time
import argparse
import dill as pickle
from memory_profiler import profile
import sys
import platform
from datetime import datetime
from scipy.cluster.hierarchy import linkage

output_file = "memory-profile-agg.txt"

print("USAGE: create_agglomerative_clustering.py -p <POINT_FILE> -v <VOCAB_FILE> -k <CLUSTERS> -o <OUTPUT_FOLDER>")

@profile(stream=open(output_file, "w+"))
def perform_clustering(points, K):
    """Perform the clustering."""
    return AgglomerativeClustering(n_clusters=K, compute_distances=True).fit(points)

def agglomerative_cluster(points, vocab, K, output_path, ref=''):
    """Perform clustering and log details."""
    # Start time
    start_time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(output_file, "a") as f:
        f.write(f"Start Time: {start_time_str}\n")

    # Log environment and system details
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

    # Log input data summary
    input_summary = f"Points Shape: {points.shape}\nVocab Size: {len(vocab)}\n"
    with open(output_file, "a") as f:
        f.write(input_summary)

    # Log clustering parameters
    clustering_params = f"Number of Clusters: {K}\nDistance Metric: Euclidean\nLinkage: Ward\n"
    with open(output_file, "a") as f:
        f.write(clustering_params)

    # Perform clustering
    start_time = time.time()
    clustering = perform_clustering(points, K)
    end_time = time.time()
    runtime = f"Clustering Runtime: {end_time - start_time:.2f} seconds\n"
    with open(output_file, "a") as f:
        f.write(runtime)
    print('Finished clustering')

    # Log cluster results summary
    clusters = defaultdict(list)
    for i, label in enumerate(clustering.labels_):
        clusters[label].append(vocab[i])

    cluster_summary = "Cluster Summary:\n"
    for cluster_id, members in clusters.items():
        cluster_summary += f"Cluster {cluster_id}: {len(members)} items\n"
    with open(output_file, "a") as f:
        f.write(cluster_summary)

    # End time
    end_time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(output_file, "a") as f:
        f.write(f"End Time: {end_time_str}\n")

    # Save model and clusters to files
    fn = f"{output_path}/model-{K}-agglomerative-clustering{ref}.pkl"
    with open(fn, "wb") as fp:
        pickle.dump(clustering, fp)

    out = ""
    for key in clusters.keys():
        for word in clusters[key]:
            out += word + "|||" + str(key) + "\n"
    
    with open(f"{output_path}/clusters-agg-{K}{ref}.txt", 'w') as f:
        f.write(out)

    return out


# Argument parsing and main execution
parser = argparse.ArgumentParser()
parser.add_argument("--vocab-file","-v", help="output vocab file with complete path")
parser.add_argument("--point-file","-p", help="output point file with complete path")
parser.add_argument("--output-path","-o", help="output path clustering model and result files")
parser.add_argument("--cluster","-k", help="cluster number")
parser.add_argument("--count","-c", help="point count ratio", default=-1)

args2 = parser.parse_args()
vocab_file = args2.vocab_file
point_file = args2.point_file
output_path = args2.output_path
point_count_ratio = float(args2.count)
K = int(args2.cluster)

vocab = np.load(vocab_file)
original_count = len(vocab)
useable_count = int(point_count_ratio*original_count) if point_count_ratio != -1 else -1
vocab = np.load(vocab_file)[:useable_count]

points = np.load(point_file)[:useable_count, :]

# Create the linkage matrix using Ward's method
linkage_matrix = linkage(points, method='ward')

# Save the linkage matrix to a file
np.save(f"{output_path}/agg_linkage_matrix_{K}.npy", linkage_matrix)

start_time = time.time()
ref = '-' + str(point_count_ratio) if point_count_ratio > 0 else ''
output = agglomerative_cluster(points, vocab, K, output_path, ref)
end_time = time.time()

print(f"Total Runtime: {end_time - start_time:.2f} seconds")


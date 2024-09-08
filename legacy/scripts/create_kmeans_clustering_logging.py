import numpy as np
import time
from memory_profiler import profile
import argparse 
import sklearn
from sklearn.cluster import KMeans
import sys
import platform
from datetime import datetime

output_file = "memory-profile-kmeans.txt"

print("USAGE: create_kmeans_clustering.py -p <POINT_FILE> -v <VOCAB_FILE> -k <CLUSTERS> -o <OUTPUT_FOLDER>")

@profile(stream=open(output_file, "w+"))
def kmeans_cluster(P, V, K, output_path, ref=''):
    """
    Uses the point.npy P, vocab.npy V files of a layer (generated using https://github.com/hsajjad/ConceptX/ library) to produce a clustering of <K> clusters at <output_path> named clusters-kmeans-{K}.txt
    """
    # Start time for clustering
    start_time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(output_file, "a") as f:
        f.write(f"Start Time: {start_time_str}\n")
    
    # Log environment and system details
    env_info = (
        f"Python Version: {sys.version}\n"
        f"NumPy Version: {np.__version__}\n"
        f"SciKit-Learn Version: {KMeans.__module__}\n"
        f"System: {platform.system()} {platform.release()}\n"
        f"Processor: {platform.processor()}\n"
        f"Machine: {platform.machine()}\n"
    )
    with open(output_file, "a") as f:
        f.write(env_info)

    # Log input data summary
    input_summary = f"Points Shape: {P.shape}\nVocab Size: {len(V)}\n"
    with open(output_file, "a") as f:
        f.write(input_summary)

    # Log clustering parameters
    clustering_params = f"Number of Clusters: {K}\n"
    with open(output_file, "a") as f:
        f.write(clustering_params)
    
    # Perform KMeans clustering
    kmeans = KMeans(n_clusters=K, verbose=3)
    output = kmeans.fit(P)
    
    out_file =  f"{output_path}/clusters-kmeans-{K}{ref}.txt"

    clusters = {i:[] for i in range(K)}
    for v, l in zip(V, output.labels_):
       clusters[l].append(f'{v}|||{l}')

    out = ""
    for k,v in clusters.items():
        out += '\n'.join(v) + '\n'

    with open(out_file, 'w') as f2:
        f2.write(out)

    # Log cluster results summary
    cluster_summary = "Cluster Summary:\n"
    for cluster_id, members in clusters.items():
        cluster_summary += f"Cluster {cluster_id}: {len(members)} items\n"
    with open(output_file, "a") as f:
        f.write(cluster_summary)

    # End time for clustering
    end_time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(output_file, "a") as f:
        f.write(f"End Time: {end_time_str}\n")

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
K = int(args2.cluster)
point_count_ratio = float(args2.count)

P = np.load(point_file)
V = np.load(vocab_file)

useable_count = int(point_count_ratio*len(V)) if point_count_ratio != -1 else -1

P = P[:useable_count, :]
V = V[:useable_count]

start_time = time.time()
ref = '-' + str(point_count_ratio) if point_count_ratio > 0 else ''
kmeans_cluster(P, V, K, output_path, ref)
end_time = time.time()

# Log the total runtime
with open(output_file, "a") as f:
    f.write(f"Total Runtime: {end_time - start_time:.2f} seconds\n")

print(f"Runtime: {end_time - start_time:.2f} seconds")


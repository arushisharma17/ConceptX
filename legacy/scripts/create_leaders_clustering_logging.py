import numpy as np
import sklearn
from sklearn.cluster import AgglomerativeClustering
from collections import defaultdict
import argparse
import time
from memory_profiler import profile
from annoy import AnnoyIndex
import statistics
import sys
import platform
from datetime import datetime

output_file = "memory-profile-leaders.txt"

print("USAGE: create_leaders_clustering.py -p <POINT_FILE> -v <VOCAB_FILE> -k <CLUSTERS> -o <OUTPUT_FOLDER> -t <TAU> --fast ")

class Clique:
    """
    A clique of follower points for a leader point
    """
    def __init__(self, p, j):
        """
        Initialize a clique by adding the leader and its index
        """
        self.members = [p]
        self.member_indices = [j]
        self.centroid = p

    def __len__(self):
        return len(self.members)

    def add(self, p, j):
        """
        Add a new follower to the clique and update the centroid
        """
        self.centroid = (self.centroid * len(self.members) + p) / (1 + len(self.members))
        self.members.append(p)
        self.member_indices.append(j)

    def dist(self, p):
        """
        Returns the distance of point p to the centroid of the clique
        """
        return np.linalg.norm(p - self.centroid)

@profile(stream=open(output_file, "w+"))
def leaders_cluster(points, vocab, K, output_path, tau=None, ref='', is_fast=True, ann_file=None):
    """
    Uses the point.npy, vocab.npy files of a layer to produce a clustering of <K> clusters for threshold <tau> at <output_path> named clusters-leaders-{K}-{tau}.txt
    If the threshold tau is not provided, it's estimated.
    """
    # Start time for clustering
    start_time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(output_file, "a") as f:
        f.write(f"Start Time: {start_time_str}\n")

    # Log environment and system details
    env_info = (
        f"Python Version: {sys.version}\n"
        f"NumPy Version: {np.__version__}\n"
        f"SciKit-Learn Version: {AgglomerativeClustering.__module__}\n"
        f"Annoy Version: {AnnoyIndex.__module__}\n"
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
    clustering_params = f"Number of Clusters: {K}\nThreshold (tau): {tau}\nFast Mode: {is_fast}\n"
    with open(output_file, "a") as f:
        f.write(clustering_params)

    cliques = []

    if not is_fast:
        assert tau is not None
        for j, p in enumerate(points):
            if (j - 1) % 1000 == 0:
                print(j - 1, np.round(len(cliques) / j * 100, 2))
            found = False
            for c in cliques:
                if c.dist(p) < tau:
                    c.add(p, j)
                    found = True
                    break
            if not found:
                cliques.append(Clique(p, j))

    else:
        t = AnnoyIndex(points.shape[1], 'euclidean')
        if not ann_file:
            for i, p in enumerate(points):
                t.add_item(i, p)
            t.build(1000)
            t.save(f'{output_path}/leaders_{ref}.ann')
        else:
            t.load(ann_file)

        # Estimate tau if not provided
        if tau is None:
            m = np.random.choice(range(points.shape[0]), replace=False, size=(1000))
            dists_tau = [t.get_nns_by_item(i, 2, include_distances=True)[1] for i in m]
            tau = statistics.median([d[1] for d in dists_tau])

        used_indices = [0] * points.shape[0]
        for i, p in enumerate(points):
            if used_indices[i] != 0:
                continue
            ul = 100
            found = False
            while not found:
                neighbours, dists = t.get_nns_by_item(i, ul, include_distances=True)
                if dists[-1] < tau:
                    ul *= 2
                else:
                    for j in range(len(neighbours)):
                        if dists[j] > tau:
                            ul = j
                            found = True
                            break

            cliques.append(Clique(points[neighbours[0], :], neighbours[0]))
            used_indices[neighbours[0]] = 1
            for n in neighbours[1:ul]:
                if used_indices[n] == 1:
                    continue
                cliques[-1].add(points[n, :], n)
                used_indices[n] = 1
            if len(cliques) % 100 == 0:
                print(f'Cliques {len(cliques)} -- Points {sum(used_indices)}/{points.shape[0]}')

    centroids = [c.centroid for c in cliques]

    clustering = AgglomerativeClustering(n_clusters=K, compute_distances=True).fit(centroids)

    word_clusters = defaultdict(list)
    for i, label in enumerate(clustering.labels_):
        word_clusters[label].extend([vocab[u] for u in cliques[i].member_indices])

    out = ""
    for key, words in word_clusters.items():
        for word in words:
            out += f"{word}|||{key}\n"

    output_file_path = f'{output_path}/clusters-leaders-{K}-{tau}{ref}.txt'
    with open(output_file_path, 'w') as of:
        of.write(out)

    # Log the clustering output file path
    with open(output_file, "a") as f:
        f.write(f"Output File: {output_file_path}\n")

    # Log cluster results summary
    cluster_summary = "Cluster Summary:\n"
    for key, words in word_clusters.items():
        cluster_summary += f"Cluster {key}: {len(words)} items\n"
    with open(output_file, "a") as f:
        f.write(cluster_summary)

    # End time for clustering
    end_time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(output_file, "a") as f:
        f.write(f"End Time: {end_time_str}\n")

    return out, tau

# Argument parsing and main execution
parser = argparse.ArgumentParser()
parser.add_argument("--vocab-file", "-v", help="input vocab file with complete path")
parser.add_argument("--point-file", "-p", help="output point file with complete path")
parser.add_argument("--output-path", "-o", help="output path clustering model and result files")
parser.add_argument("--cluster", "-k", help="cluster number")
parser.add_argument("--count", "-c", help="point count ratio", default=-1)
parser.add_argument("--tau", "-t", help="Leaders threshold")
parser.add_argument("--fast", action='store_true')
parser.add_argument("--ann", '-a', help="ann file to load")

args2 = parser.parse_args()
vocab_file = args2.vocab_file
point_file = args2.point_file
output_path = args2.output_path
is_fast = args2.fast
ann_file = args2.ann

point_count_ratio = float(args2.count)
K = int(args2.cluster)

vocab = np.load(vocab_file)
original_count = len(vocab)
useable_count = int(point_count_ratio * original_count) if point_count_ratio != -1 else -1
vocab = np.load(vocab_file)[:useable_count]

points = np.load(point_file)[:useable_count, :]

tau = float(args2.tau) if args2.tau is not None else None
K = int(args2.cluster)
ref = "-" + str(point_count_ratio) if point_count_ratio > 0 else ""

start_time = time.time()
leaders_cluster(points, vocab, K, output_path, tau, ref, is_fast=is_fast, ann_file=ann_file)
end_time = time.time()

# Log the total runtime
with open(output_file, "a") as f:
    f.write(f"Total Runtime: {end_time - start_time:.2f} seconds\n")

print(f"Runtime: {end_time - start_time:.2f} seconds")


import numpy as np
from clustering.logger import log_start_time, log_environment, log_end_time, log_cluster_summary

# Simulate a clustering process
output_file = "cluster_log.txt"
points = np.random.rand(100, 5)
vocab = np.array([f"word_{i}" for i in range(100)])

# Log the environment
log_start_time(output_file)
log_environment(output_file)
log_input_data_summary(points, vocab, output_file)

# Simulate clusters
clusters = {0: ["word_0", "word_1"], 1: ["word_2", "word_3"]}
log_cluster_summary(clusters, output_file)

# End logging
log_end_time(output_file)

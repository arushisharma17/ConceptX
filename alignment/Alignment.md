# Assigning Labels to Clusters Using Python

This tutorial walks through the process of assigning labels to clusters based on word labels in sentences, using a Python script. We'll use two methods (`M1` and `M2`) to explore different strategies for label assignment.

## Prerequisites

- Python 3.x
- Libraries: `argparse`, `os`, `numpy`
- Sample input files: `sentence_file.txt`, `label_file.txt`, and `cluster_file.txt`

### Sample Files

1. **`sentence_file.txt`**
   - This file contains sentences, one per line.

   ```plaintext
   I love programming
   Python is great
   ```
   
2. **`label_file.txt`**
   - This file contains the corresponding labels for each word in the sentences, one per line.

   ```plaintext
   PRON VERB NOUN
   NOUN AUX ADJ
   ```
   
3. **`cluster_file.txt`**
   - This file contains clusters of words, with the following format: 
     word|||frequency|||sentence_index|||word_index|||cluster_id.

   ```plaintext
   love|||5|||0|||1|||cluster_1
   programming|||8|||0|||2|||cluster_1
   Python|||3|||1|||0|||cluster_2
   great|||7|||1|||2|||cluster_2
   ```

4. Sample Output
   ```plaintext
   Cluster cluster_1 assigned label: NOUN
   Cluster cluster_2 assigned label: NONE
   Number of clusters successfully assigned a label: 1
   Unique tags: {'PRON', 'VERB', 'NOUN', 'AUX', 'ADJ'}
   Number of clusters: 2, 33.33%
   Number of tags covered: 1, 20.0%
   Overall Alignment Score: 0.2667
   ```

## Script Explanation

The script is designed to assign labels to clusters of words by analyzing the word labels in the sentences. The script provides two methods (`M1` and `M2`) for label assignment.

### 1. Command-Line Interface

The script uses the `argparse` library to define a command-line interface. You can run the script with the following arguments:

- `--sentence-file`: Path to the sentence file
- `--label-file`: Path to the label file
- `--cluster-file`: Path to the cluster file
- `--threshold`: Alignment threshold (e.g., 0.5 for 50%)
- `--method`: Method to use for label assignment (`M1` or `M2`)

### 2. Loading Data

The script loads the sentences, labels, and clusters from the input files. The `load_sentences_and_labels()` function loads the sentences and their corresponding labels, while the `load_clusters()` function loads the cluster information.

### 3. Label Map Creation

Two different functions create label maps depending on the chosen method:

- **`create_label_map()`**: Maps each `(word_index, word)` pair to its label. Used in method `M1`.
- **`create_label_map_2()`**: Organizes labels by tag and groups words associated with each tag. Used in method `M2`.

### 4. Assigning Labels to Clusters

The script provides two methods for assigning labels to clusters:

- **`assign_labels_to_clusters()`** (Method `M1`): This method counts the frequency of labels within each cluster and assigns the most common label to the cluster if it exceeds the specified threshold.
- **`assign_labels_to_clusters_2()`** (Method `M2`): This method evaluates matches between words in clusters and predefined label sets, assigning labels based on a threshold.

### 5. Analyzing the Results

The script outputs statistics about the clusters, such as the number of clusters that received a label, the percentage of unique tags covered, and an overall alignment score.

## How to Run the Script

1. **Prepare Input Files**: Make sure you have the `sentence_file.txt`, `label_file.txt`, and `cluster_file.txt` files ready in your working directory.
2. **Run the Script**: Use the following command to run the script with Method 1 and a threshold of 50%.

```bash
python alignment.py --sentence-file sentence_file.txt --label-file label_file.txt --cluster-file cluster_file.txt --threshold 50 --method M1












# Clustering and Labeling Alignment Methods

This repository implements two methods (M1 and M2) for assigning labels to clusters based on word labels in sentences. The goal of both methods is to evaluate the alignment between clusters (formed by grouping words with similar characteristics) and predefined labels for those words.

## Alignment Methods Overview

The alignment process consists of the following steps:

1. **Loading Data**: Load sentences, corresponding labels, and clusters.
2. **Creating Label Maps**: Create mappings between words and their labels.
3. **Assigning Labels to Clusters**: Assign labels to clusters based on the words contained in those clusters.
4. **Analyzing the Alignment**: Evaluate the alignment of clusters to the predefined labels and calculate alignment metrics.

## Method M1

### Steps:
1. **Create a Label Map**: 
   - For each word in the sentence, map the word (along with its position in the sentence) to its corresponding label.
   - The result is a dictionary where the keys are word positions and words, and the values are their respective labels.

2. **Assign Labels to Clusters**:
   - Group clusters of words based on cluster IDs.
   - Count how often each label appears within the cluster.
   - Assign the label that appears most frequently within the cluster as the representative label if it exceeds a given threshold (e.g., 70%). Otherwise, assign the label "NONE".

3. **Analyze Clusters**:
   - Calculate and print metrics including:
     - Distribution of assigned labels across clusters.
     - Number of unique labels covered by the clusters.
     - Overall alignment score.

### Strengths:
- Straightforward approach, relies on counting label occurrences to determine the dominant label.
- Flexible threshold to control strictness of label assignment.

### Weaknesses:
- May struggle with clusters containing a mix of labels, especially if no clear dominant label exists.
- Relies heavily on word-level labels, potentially missing the broader context of a cluster.

## Method M2

### Steps:
1. **Create a Label Map with Filtering**:
   - Create a label map where labels are mapped to words.
   - Filter out labels associated with fewer than six words to focus on labels with sufficient representation.

2. **Assign Labels to Clusters**:
   - Group clusters of words based on cluster IDs.
   - Compare words in the cluster with the filtered label map.
   - Assign the label if a significant proportion of the words in the cluster match the label (based on the threshold). If no label meets the criteria, assign the label "NONE".

3. **Analyze Clusters**:
   - Calculate and print metrics, similar to M1, including the number of clusters assigned a label and the overall alignment score.

### Strengths:
- Filters out noise by focusing on frequently occurring labels, potentially improving alignment accuracy.
- Reduces the impact of low-frequency labels that may introduce noise.

### Weaknesses:
- Filtering out low-frequency labels may result in the loss of meaningful labels.
- Like M1, relies on word-level labels, potentially missing higher-level semantic or syntactic roles.

## Comparison of Methods

| Feature                      | Method M1                                   | Method M2                                   |
|------------------------------|---------------------------------------------|---------------------------------------------|
| **Label Map**                 | Creates a label map for all words           | Filters out labels associated with fewer than 6 words |
| **Cluster Label Assignment**  | Based on the most frequent label in a cluster | Based on comparing words in clusters to a filtered label map |
| **Threshold**                 | Assigns a label if it exceeds a given threshold | Similar threshold-based assignment |
| **Filtering**                 | No filtering applied                        | Filters low-frequency labels |
| **Strengths**                 | Simpler approach, no filtering              | Filters out noise, potentially more accurate |
| **Weaknesses**                | May assign "NONE" to clusters with mixed labels | May lose meaningful low-frequency labels    |

## Metrics for Evaluation

1. **Assigned Cluster Count**: The number of clusters that were successfully assigned a label (i.e., not labeled as "NONE").
2. **Unique Tag Coverage**: The number of unique tags covered by the clusters, as a percentage of the total unique tags in the dataset.
3. **Overall Alignment Score**: A combined metric that averages the proportion of clusters assigned a label and the proportion of unique tags covered.

These metrics help evaluate the effectiveness of each method in aligning clusters with predefined labels. A higher alignment score indicates better performance.

## Potential Improvements

Both methods have room for improvement, particularly in dealing with clusters that contain a mix of labels. Some potential enhancements include:
- **Incorporating Context**: Using context-aware techniques, such as BIO-labeling, to capture higher-level semantic or syntactic roles of clusters.
- **LLM-based Labeling**: Leveraging large language models to assign labels based on the broader context of a cluster, rather than relying solely on individual word-level labels.
- **Multi-level Clustering**: Analyzing clusters at multiple levels of abstraction, such as grouping functions, loops, or other code structures together.

These improvements can help refine the alignment process and lead to more accurate cluster labeling.

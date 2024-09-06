# ConceptX
Analyzing Latent Concept in Code-trained Transformer Models

### 1. Clone and Set Up ConceptX (for clustering)
module purge
module load micromamba
module load git

First, clone the **ConceptX** repository and set up the environment for extracting activations.

```bash
cd /work/LAS/jannesar-lab/arushi/LatentConceptAnalysis
cd <your project dir>

# Clone the ConceptX repository
git clone https://github.com/arushisharma17/ConceptX.git
cd ConceptX

# Initialize micromamba
eval "$(micromamba shell hook --shell=bash)"

# Create and activate the 'clustering' environment from the NeuroX repository
micromamba env create --name=clustering

# Activate the environment
micromamba activate clustering

# Check if environment activation was successful and proceed with package installation
if micromamba activate clustering; then
    echo "Environment 'env_activations' activated successfully."

    # Install Hugging Face transformers package
    python -m pip install git+https://github.com/huggingface/transformers

    # Install NeuroX in editable mode
    pip install -e .

    # List installed packages to verify installation
    echo "Listing installed packages in 'clustering':"
    micromamba list

    # Deactivate environment after setup
    micromamba deactivate
else
    echo "Failed to activate environment 'clustering'."
    exit 1
fi

cd ..
```



The code has been split into three parts. 1) get concept clusters, 2) generate auto-labels data, 3) calculate the alignment between auto-labels and concepts.

## Get concept clusters
get_clusters/getclusters.sh provides step-by-step commands to create concept clusters. You need to specify path to a sentence file.

### Proprocessing
This step invovles tokenizing the input sentences and extracting word-level contextualized embeddings. The setup requires setting up neurox environment using env_neurox.yml.

```
conda env create --file=env_neuron.yml
```

### Run clustering
Cluster the word-level contextualized embeddings. This step requires setting up the clustering environment.

```
conda env create --file=env_clustering
```

## Generate Auto-labels
Label the sentence file with pre-defined concepts

### Linguistic Annotations
Label words with their linguistic information such as parts-of-speech, suffixes, wordNet, etc. The following command tags the sentence file with their part of speech information.

```
python --model_name "QCRI/bert-base-multilingual-cased-pos-english" --sentence_file data/text.in --output_file text.in.pos
```

### Trivial labels
auto-labels/Trivial/README provides step by step instructions to create trivial labels for the input sentence file.


## Calculate alignment
This step calculates the alignment score between a given label file and the concept clusters. 

```
python scripts/align_with_single_auto_tag.py label_file sentence_file cluster_file
```

cluster_file is the cluster output of step 1. sentence_file is the list of sentences whose words are labeled. 




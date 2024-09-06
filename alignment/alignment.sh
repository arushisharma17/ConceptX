#!/bin/bash
#SBATCH --time=2-0:00:00  # max job runtime
#SBATCH --cpus-per-task=1  # number of processor cores
#SBATCH --nodes=1  # number of nodes
#SBATCH --partition=gpu  # partition(s)
#SBATCH --gres=gpu:1
#SBATCH --mem=256G  # max memory
#SBATCH -J "Clustering"  # job name
#SBATCH --mail-user=arushi17@iastate.edu  # email address
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL 


# Load necessary modules and set environment variables
module purge
module load micromamba

# Set the MAMBA_ROOT_PREFIX and CONCEPTX_ROOT environment variables
export MAMBA_ROOT_PREFIX=/work/LAS/jannesar-lab/arushi/ConceptX/micromamba
export CONCEPTX_ROOT=/work/LAS/jannesar-lab/arushi/ConceptX/CodeConceptNet

alignmentDir=$CONCEPTX_ROOT/alignment/
dataDir=$CONCEPTX_ROOT/data/

# Initialize micromamba shell
eval "$(micromamba shell hook --shell=bash)"
#micromamba env create -y --file=env_clustering.yml
if micromamba activate clustering; then
    echo "Environment 'clustering' activated successfully."
    # List installed packages in the environment
    # echo "Listing installed packages in 'clustering':"
    #micromamba list
else
    echo "Failed to activate environment 'clustering'."
    exit 1
fi

# Change to the appropriate directory
cd $alignmentDir

python alignment_updated.py --sentence-file "$dataDir/java.in" --label-file "$dataDir/java.label" --cluster-file "${CONCEPTX_ROOT}/get_clusters/clusters/java_test/layer12/no_logging/agglomerative/clusters-agg-500.txt" --thresholds 50 60 70 --methods M1 M2

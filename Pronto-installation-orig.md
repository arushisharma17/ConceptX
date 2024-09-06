# ConceptX Installation Guide

## Overview
This guide provides detailed steps to set up the ConceptX environment using micromamba on Pronto or Nova systems.

## Prerequisites
- Access to Pronto or Nova systems.
- Basic knowledge of SLURM for job scheduling.
- Git installed on your system.

## Installation Steps

### 1. Allocate a Compute Node
On the head node of Pronto or Nova, allocate a compute node with 4 CPUs:
```bash
srun -N1 -n4 -t4:0:0 --pty bash
```

### 2. Create Directory for Micromamba Environments
Navigate to your project directory and create a directory for the micromamba environments:
```bash         
cd /to/your/proj/dir/
mkdir micromamba
```

### 3. Define the Environment Root Prefix
Set the MAMBA_ROOT_PREFIX environment variable to the path where the micromamba environments will be installed:
```bash
export MAMBA_ROOT_PREFIX=/work/LAS/jannesar-lab/arushi/micromamba
```

### 4. Purge Modules and Load Required Modules
Clear any currently loaded modules and load the necessary ones, like git for cloning the repository:   
```bash
module purge
module load git
```
### 5. Clone ConceptX Repository and set up your own github repo
- Clone the ConceptX repository from GitHub to your local project directory:
```bash
git clone https://github.com/hsajjad/ConceptX
```
- Create a new repository on github

- Initialize your local repository:
```bash
git init
git remote add origin https://github.com/YOUR_USERNAME/CodeConceptNet.git
```

### 6. Set the `CONCEPTX_ROOT` Environment Variable
Define the `CONCEPTX_ROOT` environment variable to point to the ConceptX directory:
```bash
export CONCEPTX_ROOT=/work/las-research/xfzhao/test/conceptx/ConceptX/
cd $CONCEPTX_ROOT
```

### 7. Backup the Original YML Files
Make backups of the original environment YML files:
```bash 
cp env_clustering.yml env_clustering.yml.save
cp env_neurox.yml env_neurox.yml.save
```

### 8. Modify YML Files to Include Perl
Replace the last line in both env_clustering.yml and env_neurox.yml to include Perl:
```bash
sed -i "s/prefix:.*/  - perl/g" env_clustering.yml
sed -i "s/prefix:.*/  - perl/g" env_neurox.yml
```

### 9. Verify Changes to YML Files
Use the diff command to verify that the changes were applied correctly:
```bash
diff env_clustering.yml env_clustering.yml.save
diff env_neurox.yml env_neurox.yml.save
```

### 10. Create neurox_pip Environment
Use micromamba to create the `neurox_pip` environment from the modified YML file:
```bash
micromamba env create -y --file=env_neurox.yml
```

### 11. Activate and Verify neurox_pip Environment
Activate the environment and check the installation paths for Perl and Python:
```bash
eval "$(micromamba shell hook --shell=bash)"
micromamba activate neurox_pip
which perl    # should show the path to Perl in the environment
which python  # should show the path to Python in the environment
micromamba deactivate
```

### 12. Create clustering Environment
Similarly, create the clustering environment from the modified YML file:
```bash
micromamba env create -y --file=env_clustering.yml
```

### 13. Activate and Verify clustering Environment
Activate the environment and verify the paths for Perl and Python:
```bash
micromamba activate clustering
which perl    # should show the path to Perl in the environment
which python  # should show the path to Python in the environment
micromamba deactivate
```

### 14. Run the Demo Data
Now you need to modify the get_clusters.sh script tp get_clusters.sh.micromamba to run it with the new paths and micromamba installation.The get_clusters.sh.micromamba is provided. 

## Notes
- Ensure Perl is included in the environment YML files.
- Modify `getclusters.sh` to use the full path for scripts to run from any location.

This installation guide ensures that the environments are correctly set up with all necessary dependencies, including Perl, which is required for some preprocessing steps in the ConceptX pipeline. By modifying the YML files to include Perl, you avoid issues related to missing dependencies and ensure that the pipeline runs smoothly.



















#!/bin/bash
# setup.sh

# Create conda environment
conda create -n protein_pred python=3.11 -y
conda activate protein_pred

# Install dependencies
conda install pytorch torchvision -c pytorch -y
conda install -c conda-forge pymol-open-source -y
pip install boltz

# Set environment variables
echo 'export PYTORCH_ENABLE_MPS_FALLBACK=1' >> ~/.bashrc
echo 'export CUDA_VISIBLE_DEVICES=""' >> ~/.bashrc
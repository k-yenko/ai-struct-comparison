#!/bin/bash

# make necessary directories
mkdir -p data/chai/input
mkdir -p data/chai/output

# install chai-lab
pip install chai_lab==0.4.2

# download receptor (GLP-1R) sequence
wget -O data/chai/input/glp1r.fasta "https://rest.uniprot.org/uniprotkb/P43220.fasta"

# create GLP-1(7-36) sequence file directly
cat > data/chai/input/glp1.fasta << EOF
>GLP1_7_36
HAEGTFTSDVSSYLEGQAAKEFIAWLVKGR
EOF

# combine sequences into a single FASTA file for the complex
cat data/chai/input/glp1r.fasta data/chai/input/glp1.fasta > data/chai/input/complex.fasta

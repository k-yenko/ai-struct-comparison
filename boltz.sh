# install pytorch
conda install pytorch torchvision -c pytorch

export PYTORCH_ENABLE_MPS_FALLBACK=1
export CUDA_VISIBLE_DEVICES=""

# install boltz 
pip install boltz

#create fasta files 
echo ">glp1|protein
HAEGTFTSDVSSYLEGQAAKEFIAWLVKGRG" > glp1.fasta

# place holder for glp1R, v0219, and vu

# Run Boltz for each
boltz predict glp1.fasta --use_msa_server --out_dir output_glp1
boltz predict v0219.fasta --use_msa_server --out_dir output_v0219
boltz predict vu045.fasta --use_msa_server --out_dir output_vu045
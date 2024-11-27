# run_predictions.py

import os
import subprocess
from prepare_sequences import molecules

def run_boltz(fasta_file, output_dir):
    """Run Boltz prediction for a given FASTA file"""
    cmd = f"boltz predict {fasta_file} --use_msa_server --out_dir {output_dir}"
    print(f"Running: {cmd}")
    try:
        subprocess.run(cmd, shell=True, check=True)
        print(f"Successfully completed Boltz prediction for {fasta_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error running Boltz for {fasta_file}: {e}")

def main():
    # Set up directories
    base_dir = os.path.dirname(os.path.abspath(__file__))
    results_dir = os.path.join(base_dir, "results", "boltz")
    
    # Create directories
    os.makedirs(results_dir, exist_ok=True)

    # Run individual predictions
    for name in molecules.keys():
        fasta_file = f"data/boltz/fasta/{name}.fasta"
        output_dir = os.path.join(results_dir, f"single/{name}")
        run_boltz(fasta_file, output_dir)

if __name__ == "__main__":
    main()
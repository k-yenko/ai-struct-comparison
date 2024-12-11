import os
import subprocess
from prepare_sequences import molecules
import torch

# set device
if torch.backends.mps.is_available():
       device = torch.device("mps")
else:
       device = torch.device("cpu")

def run_boltz(fasta_file, output_dir, device):
    """Run Boltz prediction for a given FASTA file"""
    accelerator_option = "cpu"  # Always use CPU for Apple Silicon
    cmd = f"boltz predict --accelerator {accelerator_option} {fasta_file} --use_msa_server --out_dir {output_dir}"
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
        run_boltz(fasta_file, output_dir, device)  # Pass the device here
if __name__ == "__main__":
    main()
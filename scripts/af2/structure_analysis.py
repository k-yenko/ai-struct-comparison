import subprocess
import os
from Bio import PDB
import numpy as np

def check_structure(file_path):
    """Check if structure file is readable and valid"""
    try:
        parser = PDB.PDBParser(QUIET=True) if file_path.endswith('.pdb') else PDB.MMCIFParser(QUIET=True)
        structure = parser.get_structure('test', file_path)
        
        # Print chain information
        print(f"\nFile: {file_path}")
        for chain in structure.get_chains():
            num_residues = len(list(chain.get_residues()))
            print(f"Chain {chain.id}: {num_residues} residues")
        
        return True
    except Exception as e:
        print(f"Error reading {file_path}: {str(e)}")
        return False

def calculate_metrics(model_path, reference_path, output_dir):
    """Calculate LDDT and TM-score for a model against reference"""
    
    # First check if structures are valid and print chain info
    print("\nChecking reference structure:")
    if not check_structure(reference_path):
        return {'TM-score': 0.0}
    
    print("\nChecking model structure:")
    if not check_structure(model_path):
        return {'TM-score': 0.0}
    
    # Run TM-align with timeout
    cmd = f"TMalign {model_path} {reference_path}"
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)  # 30 second timeout
        print("\nTMalign output:")
        print(result.stdout)
        print("\nTMalign errors:")
        print(result.stderr)
    except subprocess.TimeoutExpired:
        print("TMalign timed out after 30 seconds")
        return {'TM-score': 0.0}
    except Exception as e:
        print(f"Error running TMalign: {str(e)}")
        return {'TM-score': 0.0}
    
    # Initialize tm_score
    tm_score = None
    
    # Parse TM-score from output
    for line in result.stdout.split('\n'):
        if 'TM-score=' in line:
            try:
                tm_score = float(line.split('=')[1].split()[0])
                break
            except (IndexError, ValueError) as e:
                print(f"Error parsing TM-score from line: {line}")
                print(f"Error details: {e}")
    
    # Check if we found a TM-score
    if tm_score is None:
        print("Warning: Could not find TM-score in output")
        tm_score = 0.0
    
    return {'TM-score': tm_score}

if __name__ == "__main__":
    # Reference structure (PDB)
    reference = "data/common/structures/6x18.pdb"
    
    # Models to evaluate
    models = {
        'chai': "data/projects/glp1r_glp1/chai/pred.model_idx_0.rank_0.cif",
        'boltz': "results/glp1r_glp1/boltz/glp1r_glp1_model_0.cif",
        'af3': "data/projects/glp1r_glp1/af3/fold_glp_1r_and_glp_1_model_0.cif",
        'af2': "data/projects/glp1r_glp1/af2/AF-P43220-F1-model_v4.pdb"
    }
    
    # Calculate metrics for each model
    results = {}
    for name, path in models.items():
        if not os.path.exists(path):
            print(f"\nSkipping {name} due to missing file")
            continue
            
        print(f"\nCalculating metrics for {name}...")
        metrics = calculate_metrics(path, reference, "results/metrics")
        results[name] = metrics
        print(f"TM-score: {metrics['TM-score']:.3f}")
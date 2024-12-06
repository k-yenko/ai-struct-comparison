import os
import pymol
from pymol import cmd

def calculate_rmsd(pred_path, true_path, name, output_dir):
    """Calculate RMSD between predicted and true structures"""
    # Initialize PyMOL in command-line mode
    pymol.finish_launching(['pymol', '-qc'])
    
    try:
        # Load structures
        cmd.load(pred_path, "pred")
        cmd.load(true_path, "true")
        
        # Perform alignment
        rmsd = cmd.align("pred", "true")
        print(f"{name} RMSD: {rmsd[0]:.2f} Å")
        
        # Save results
        os.makedirs(output_dir, exist_ok=True)
        with open(os.path.join(output_dir, "rmsd_results.txt"), "a") as f:
            f.write(f"{name}\t{rmsd[0]:.2f}\n")
        
        # Save aligned structure
        cmd.save(os.path.join(output_dir, f"aligned_{name}.pdb"), "pred")
        
        return rmsd[0]
    
    finally:
        cmd.quit()

if __name__ == "__main__":
    # Paths
    true_path = "data/pdb/structures/6x18.pdb"
    output_dir = "data/analysis"
    
    # Analyze Chai prediction
    chai_path = "data/chai/input/pred.model_idx_0.rank_0.cif"
    calculate_rmsd(chai_path, true_path, "chai_prediction", output_dir)
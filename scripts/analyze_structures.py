import os
import threading
import time
import pymol # you need to switch envs to molview to import pymol
from pymol import cmd

def initialize_pymol():
    """Initialize PyMOL in command-line mode"""
    pymol.finish_launching(['pymol', '-qc'])  # Quiet and no GUI
    time.sleep(2)  # Give PyMOL time to initialize

def analyze_structures():
    """Load and analyze structures"""
    # Load ground truth
    cmd.load("data/pdb/structures/6x18.pdb", "ground_truth")
    
    # Load Boltz prediction
    cmd.load("results/boltz/complexes/glp1r_glp1/boltz_results_glp1r_glp1/predictions/glp1r_glp1/glp1r_glp1_model_0.cif", "boltz_pred")
    
    # Basic visualization
    cmd.hide("everything")
    cmd.show("cartoon")
    
    # Color structures differently
    cmd.color("cyan", "ground_truth")
    cmd.color("salmon", "boltz_pred")
    
    # Align structures
    alignment = cmd.align("boltz_pred", "ground_truth")
    rmsd = alignment[0]  # Get RMSD from alignment
    
    # Save alignment information
    with open("results/structure_comparison.txt", "w") as f:
        f.write(f"Structure Comparison Results:\n")
        f.write(f"RMSD between structures: {rmsd:.2f} Å\n")
        f.write(f"Number of aligned atoms: {alignment[1]}\n")
    
    # Save aligned structures
    cmd.save("results/aligned_ground_truth.pdb", "ground_truth")
    cmd.save("results/aligned_boltz_pred.pdb", "boltz_pred")
    
    # Create a session file that can be opened in PyMOL GUI later
    cmd.save("results/comparison.pse")
    
    print(f"RMSD between structures: {rmsd:.2f} Å")
    print("Results saved to results/structure_comparison.txt")
    print("Aligned structures saved as PDB files")
    print("PyMOL session saved as results/comparison.pse")

def main():
    # Initialize PyMOL in command-line mode
    initialize_pymol()
    
    # Run analysis
    analyze_structures()
    
    # Clean up
    cmd.quit()

if __name__ == "__main__":
    main()
import pymol
from pymol import cmd
import os

def debug_structures():
    # Start PyMOL in command-line mode
    pymol.finish_launching(['pymol', '-qc'])
    
    # Get current working directory and construct full paths
    base_dir = os.getcwd()
    pdb_path = os.path.join(base_dir, "data/pdb/structures/6x18.pdb")
    boltz_path = os.path.join(base_dir, "results/boltz/complexes/glp1r_glp1/boltz_results_glp1r_glp1/predictions/glp1r_glp1/glp1r_glp1_model_0.cif")
    
    # Print paths to verify
    print(f"PDB path: {pdb_path}")
    print(f"Boltz path: {boltz_path}")
    
    # Check if files exist
    print(f"PDB file exists: {os.path.exists(pdb_path)}")
    print(f"Boltz file exists: {os.path.exists(boltz_path)}")
    
    # Try loading ground truth
    cmd.load(pdb_path, "ground_truth")
    print("Number of atoms in ground truth:", cmd.count_atoms("ground_truth"))
    
    # Try loading Boltz
    cmd.load(boltz_path, "boltz_pred")
    print("Number of atoms in Boltz:", cmd.count_atoms("boltz_pred"))
    
    # Check what objects are loaded
    print("Loaded objects:", cmd.get_object_list())
    
    # Save the current state
    cmd.save("debug_session.pse")

if __name__ == "__main__":
    debug_structures()
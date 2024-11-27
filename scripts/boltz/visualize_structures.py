# visualize_structures.py

import os
import pymol
from pymol import cmd

def load_structures(base_dir):
    """Load all predicted structures"""
    # Load single molecule predictions
    single_dir = os.path.join(base_dir, "results/boltz/single")
    for mol in os.listdir(single_dir):
        struct_path = os.path.join(single_dir, mol, "predictions", f"{mol}_model_0.cif")
        if os.path.exists(struct_path):
            cmd.load(struct_path, mol)

    # Load complex predictions
    complex_dir = os.path.join(base_dir, "results/boltz/complexes")
    for complex_name in ["glp1r_glp1", "glp1r_glp1_v0219", "glp1r_glp1_vu045"]:
        struct_path = os.path.join(complex_dir, complex_name, "predictions", 
                                 f"{complex_name}_model_0.cif")
        if os.path.exists(struct_path):
            cmd.load(struct_path, complex_name)
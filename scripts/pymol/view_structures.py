import pymol
from pymol import cmd

# Clear everything first
cmd.delete('all')

# Define color schemes for each structure (receptor, peptide)
colors = {
    'true_filtered': ('cyan', 'marine'),
    'chai': ('salmon', 'red'),
    'boltz': ('yellow', 'orange'),
    'boltz2': ('gray70', 'gray30'),
    'af3': ('forest', 'lime')
}

# Load and filter PDB structure
cmd.load("data/pdb/structures/6x18.pdb", "true")
cmd.select("true_complex", "true and chain R+P")
cmd.create("true_filtered", "true_complex")
cmd.delete("true")
cmd.delete("true_complex")

# Load other structures
structures = {
    "chai": "data/chai/input/pred.model_idx_0.rank_0.cif",
    "boltz": "results/boltz/complexes/glp1r_glp1/predictions/glp1r_glp1_model_0.cif",
    "boltz2": "boltz_combination_outputs/glp1r_glp1/boltz_results_glp1r_glp1/predictions/glp1r_glp1/glp1r_glp1_model_0.cif",
    "af3": "data/af3/fold_glp_1r_and_glp_1_model_0.cif"
}

# Load additional structures
for name, path in structures.items():
    cmd.load(path, name)

# Hide everything initially
cmd.hide("everything")

# Set up visualization for each structure
for struct in ['true_filtered'] + list(structures.keys()):
    # Show receptor as cartoon and peptide as sticks
    cmd.show("cartoon", f"{struct} and chain R")
    cmd.show("sticks", f"{struct} and chain P")
    
    # Color receptor and peptide differently
    receptor_color, peptide_color = colors[struct]
    cmd.color(receptor_color, f"{struct} and chain R")
    cmd.color(peptide_color, f"{struct} and chain P")

# Turn off labels
cmd.set("label_size", 0)

# Align structures and calculate RMSD
print("\nRMSD values when aligned to true structure:")
for struct in structures.keys():
    rmsd = cmd.align(struct, "true_filtered")[0]
    print(f"{struct.upper()} RMSD: {rmsd:.2f} Å")

# Center the view
cmd.zoom("visible")
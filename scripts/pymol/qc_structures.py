import pymol
from pymol import cmd

# Load and filter PDB structure
cmd.load("data/pdb/structures/6x18.pdb", "true")
cmd.select("true_complex", "true and chain R+P")
cmd.create("true_filtered", "true_complex")
cmd.delete("true")
cmd.delete("true_complex")

# Load other structures
structures = {
    "chai": "data/chai/input/pred.model_idx_0.rank_0.cif",
    "boltz": "results/boltz/glp1r_glp1_model_0.cif",
    "af3": "data/af3/fold_glp_1r_and_glp_1_model_0.cif"
}

# Load additional structures
for name, path in structures.items():
    cmd.load(path, name)


# Align structures and calculate RMSD
print("\nRMSD values when aligned to true structure:")
for struct in structures.keys():
    rmsd = cmd.align(struct, "true_filtered")[0]
    print(f"{struct.upper()} RMSD: {rmsd:.2f} Å")

# Center the view
cmd.zoom("visible")
import pymol
from pymol import cmd

# Paths
true_path = "data/pdb/structures/6x18.pdb"
chai_path = "data/chai/input/pred.model_idx_0.rank_0.cif"
boltz_path = "/Users/katherineyenko/Desktop/sandbox/ai-struct-comparison/results/boltz/complexes/glp1r_glp1/predictions/glp1r_glp1_model_0.cif"

# Load structures
cmd.load(true_path, "true")
cmd.load(chai_path, "chai")
cmd.load(boltz_path, "boltz")

# Color schemes
cmd.color("cyan", "true")
cmd.color("salmon", "chai")
cmd.color("yellow", "boltz")

# Align structures
cmd.align("chai", "true")
cmd.align("boltz", "true")

# Show as cartoon
cmd.show_as("cartoon")
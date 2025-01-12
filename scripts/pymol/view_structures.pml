# script for running line-by-line in PyMOL

# Load ground truth (6X18) and color chains
load data/common/structures/6x18.pdb, true
remove not chain R+P and true
color marine, true and chain R    # receptor in dark blue
color orange, true and chain P    # peptide in orange
show cartoon, true and chain R    # receptor as cartoon
show sticks, true and chain P     # peptide as sticks

# Load Chai prediction
load data/projects/glp1r_glp1/chai/pred.model_idx_0.rank_0.cif, chai
color slate, chai and chain A     # receptor in grey-blue
color salmon, chai and chain B    # peptide in pink
show cartoon, chai and chain A    # receptor as cartoon
show sticks, chai and chain B     # peptide as sticks

# Load Boltz prediction
load results/glp1r_glp1/boltz/glp1r_glp1_model_0.cif, boltz
color forest, boltz and chain A   # receptor in green
color yellow, boltz and chain B   # peptide in yellow
show cartoon, boltz and chain A   # receptor as cartoon
show sticks, boltz and chain B    # peptide as sticks

# Load AlphaFold3 prediction (model 0)
load data/projects/glp1r_glp1/af3/fold_glp_1r_and_glp_1_model_0.cif, af3
color purple, af3 and chain A     # receptor in purple
color pink, af3 and chain B       # peptide in pink
show cartoon, af3 and chain A     # receptor as cartoon
show sticks, af3 and chain B      # peptide as sticks

# Load AlphaFold2 prediction
load data/projects/glp1r_glp1/af2/AF-P43220-F1-model_v4.pdb, af2
color red, af2 and chain A     # receptor in red
color blue, af2 and chain B   # peptide in blue
show cartoon, af2 and chain A   # receptor as cartoon
show sticks, af2 and chain B    # peptide as sticks

# Hide everything first then show specific representations
hide everything
show cartoon, chain R+A
show sticks, chain P+B

# Align all predictions to PDB and get RMSD values
print "\nRMSD values when aligned to true structure:"
align chai, true
align boltz, true
align af3, true
align af2, true

# Make sure everything is visible
enable all
zoom all

# Turn off labels if any
set label_size, 0
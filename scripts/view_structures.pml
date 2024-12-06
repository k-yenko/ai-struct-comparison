# Clear everything
delete all

# Load ground truth (6X18) and color chains
load data/pdb/structures/6x18.pdb, true
remove not chain R+P and true
color marine, true and chain R    # receptor in dark blue
color orange, true and chain P    # peptide in orange

# Load Chai prediction
load data/chai/input/pred.model_idx_0.rank_0.cif, chai
color slate, chai and chain A     # receptor in grey-blue
color salmon, chai and chain B    # peptide in pink

# Load Boltz prediction
load /Users/katherineyenko/Desktop/sandbox/ai-struct-comparison/results/boltz/complexes/glp1r_glp1/predictions/glp1r_glp1_model_0.cif, boltz
color forest, boltz and chain A   # receptor in green
color yellow, boltz and chain B   # peptide in yellow

# Load AlphaFold3 prediction (model 0)
load data/af3/fold_glp_1r_and_glp_1_model_0.cif, af3
color purple, af3 and chain A     # receptor in purple
color pink, af3 and chain B       # peptide in pink

# Show all as cartoon
show cartoon

# Align all predictions to PDB, get 
align chai, true
align boltz, true
align af3, true

# Make sure everything is visible
enable all
zoom all
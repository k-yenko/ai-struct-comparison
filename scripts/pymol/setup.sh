# Step 1: Install necessary build tools (if not already installed)
# For macOS, you may need to install Xcode command line tools
xcode-select --install

# Step 2: Install PyMOL using Homebrew
brew install pymol

# Step 3: Run PyMOL
pymol

# Step 4: Run PyMOL for GLP-1R and GLP-1 peptide, comparing Boltz-1, Chai-1, AF3 to PDB 6X18 as ground truth
pymol scripts/view_structures.pml
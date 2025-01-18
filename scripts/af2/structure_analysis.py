import numpy as np
from Bio import PDB
from Bio.PDB import *
import pandas as pd

# Create parser and structure objects
parser = PDB.PDBParser()
structure = parser.get_structure('glp1r', 'data/projects/glp1r_glp1/af2/AF-P43220-F1-model_v4.pdb')

# Extract chain A
chain_A = structure[0]['A']

# Get residues and their properties
residue_data = []

# Calculate surface accessibility
sr = SASA.ShrakeRupley()
sr.compute(structure, level="R")

for res in chain_A:
    if res.id[0] == ' ':  # Only standard amino acids
        # Get pLDDT from B-factor (AF2 stores confidence scores here)
        try:
            plddt = np.mean([atom.bfactor for atom in res])
            # Convert AF2 scale (0-100) to 0-1
            plddt = plddt/100
        except:
            plddt = 0
            
        # Get surface accessibility
        sasa = res.sasa
            
        residue_data.append({
            'residue_id': res.id[1],
            'residue_name': res.resname,
            'plddt': plddt,
            'sasa': sasa
        })

# Convert to DataFrame
df = pd.DataFrame(residue_data)

# Calculate sliding window averages (7-residue window)
window_size = 7
df['plddt_window'] = df['plddt'].rolling(window=window_size, center=True).mean()
df['sasa_window'] = df['sasa'].rolling(window=window_size, center=True).mean()

# Identify high-confidence surface regions
threshold_plddt = 0.7  # High confidence threshold
threshold_sasa = np.percentile(df['sasa_window'].dropna(), 70)  # Top 30% exposed

# Find regions meeting both criteria
high_quality_surface = df[
    (df['plddt_window'] >= threshold_plddt) & 
    (df['sasa_window'] >= threshold_sasa)
].copy()

# Find continuous regions
high_quality_surface['region'] = (
    high_quality_surface['residue_id'].diff() != 1).cumsum()

# Group into regions
regions = []
for region_id, group in high_quality_surface.groupby('region'):
    if len(group) >= 5:  # Minimum 5 residues per region
        regions.append({
            'start': group['residue_id'].iloc[0],
            'end': group['residue_id'].iloc[-1],
            'avg_plddt': group['plddt'].mean(),
            'avg_sasa': group['sasa'].mean(),
            'size': len(group)
        })

# Print overall statistics
print("\nOverall Structure Statistics:")
print(f"Average pLDDT: {df['plddt'].mean():.3f}")
print(f"Minimum pLDDT: {df['plddt'].min():.3f}")
print(f"Maximum pLDDT: {df['plddt'].max():.3f}")

print("\nPromising Surface Regions:")
for i, region in enumerate(regions, 1):
    print(f"\nRegion {i}:")
    print(f"Residues {region['start']}-{region['end']} ({region['size']} residues)")
    print(f"Average pLDDT: {region['avg_plddt']:.3f}")
    print(f"Average SASA: {region['avg_sasa']:.1f}")

# Look for low confidence regions to avoid
low_confidence = df[df['plddt'] < 0.5]
if not low_confidence.empty:
    print("\nLow Confidence Regions to Avoid:")
    print(low_confidence[['residue_id', 'residue_name', 'plddt']].to_string(index=False))
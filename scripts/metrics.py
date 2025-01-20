import numpy as np
from pathlib import Path
import subprocess
import tempfile
from Bio import PDB
from Bio.SVDSuperimposer import SVDSuperimposer

def calculate_rmsd(model_structure, ref_structure):
    """Calculate RMSD between peptide chains after aligning receptor backbone"""
    print("\nCalculating RMSD...")
    
    # Get chains
    ref_receptor = ref_structure[0]['R']
    ref_peptide = ref_structure[0]['P']
    model_receptor = model_structure[0]['A']
    model_peptide = model_structure[0]['B'] if 'B' in model_structure[0] else None
    
    if not model_peptide:
        print("No peptide chain found in model")
        return 0.0
    
    # First align using receptor backbone atoms with iterative fitting
    ref_coords = []
    model_coords = []
    atom_pairs = []
    
    # Get all matching residues first
    for ref_res in ref_receptor.get_residues():
        try:
            model_res = model_receptor[ref_res.id]
            if 'CA' in ref_res and 'CA' in model_res:
                atom_pairs.append((ref_res['CA'], model_res['CA']))
        except KeyError:
            continue
    
    max_cycles = 5
    cutoff_factor = 2.0
    current_pairs = atom_pairs
    
    for cycle in range(max_cycles):
        # Get coordinates for current pairs
        ref_coords = np.array([a[0].get_coord() for a in current_pairs])
        model_coords = np.array([a[1].get_coord() for a in current_pairs])
        
        # Perform superposition
        sup = SVDSuperimposer()
        sup.set(ref_coords, model_coords)
        sup.run()
        rot, tran = sup.get_rotran()
        
        # Calculate distances and RMSD
        aligned_coords = np.dot(model_coords, rot) + tran
        dists = np.sqrt(np.sum((ref_coords - aligned_coords)**2, axis=1))
        rmsd = np.sqrt(np.mean(dists**2))
        
        # Reject outliers
        cutoff = rmsd * cutoff_factor
        new_pairs = [pair for pair, dist in zip(current_pairs, dists) if dist < cutoff]
        
        print(f"Cycle {cycle+1}: Receptor RMSD = {rmsd:.3f}Å ({len(current_pairs)} atoms)")
        
        if len(new_pairs) == len(current_pairs):
            break
            
        current_pairs = new_pairs
    
    # Now calculate RMSD for peptide using final transformation
    peptide_ref_coords = []
    peptide_model_coords = []
    
    for ref_res in ref_peptide.get_residues():
        try:
            model_res = model_peptide[ref_res.id]
            if 'CA' in ref_res and 'CA' in model_res:
                peptide_ref_coords.append(ref_res['CA'].get_coord())
                model_coord = np.dot(model_res['CA'].get_coord(), rot) + tran
                peptide_model_coords.append(model_coord)
        except KeyError:
            continue
    
    # Calculate final peptide RMSD
    peptide_ref_coords = np.array(peptide_ref_coords)
    peptide_model_coords = np.array(peptide_model_coords)
    peptide_rmsd = np.sqrt(np.mean(np.sum((peptide_ref_coords - peptide_model_coords)**2, axis=1)))
    
    print(f"\nFinal statistics:")
    print(f"Aligned {len(current_pairs)} receptor CA atoms")
    print(f"Calculated RMSD over {len(peptide_ref_coords)} peptide CA atoms")
    
    return peptide_rmsd

def calculate_lddt_pli(model_structure, ref_structure, cutoff_distance=8.0):
    """Calculate LDDT-PLI score for protein-peptide interface"""
    # Get chains
    ref_receptor = ref_structure[0]['R']
    ref_peptide = ref_structure[0]['P']
    model_receptor = model_structure[0]['A']
    model_peptide = model_structure[0]['B'] if 'B' in model_structure[0] else None
    
    if not model_peptide:
        return 0.0
    
    # Find interface pairs (only protein-peptide contacts)
    interface_pairs = {'ref': [], 'model': []}
    
    for ref_res in ref_receptor.get_residues():
        for ref_pep_res in ref_peptide.get_residues():
            for ref_atom in ref_res.get_atoms():
                for ref_pep_atom in ref_pep_res.get_atoms():
                    dist = ref_atom - ref_pep_atom
                    if dist < cutoff_distance:
                        try:
                            model_res = model_receptor[ref_res.id]
                            model_pep_res = model_peptide[ref_pep_res.id]
                            model_atom = model_res[ref_atom.name]
                            model_pep_atom = model_pep_res[ref_pep_atom.name]
                            
                            interface_pairs['ref'].append((ref_atom, ref_pep_atom))
                            interface_pairs['model'].append((model_atom, model_pep_atom))
                        except KeyError:
                            continue
    
    if not interface_pairs['ref']:
        return 0.0
    
    # Calculate distances
    ref_dists = [a1 - a2 for a1, a2 in interface_pairs['ref']]
    model_dists = [a1 - a2 for a1, a2 in interface_pairs['model']]
    deviations = [abs(d1 - d2) for d1, d2 in zip(ref_dists, model_dists)]
    
    # Calculate scores for different thresholds
    thresholds = [2.0, 4.0, 6.0, 8.0]  # Adjusted for GLP1R-GLP1 interaction
    scores = []
    
    print("\nLDDT-PLI scores per threshold:")
    for threshold in thresholds:
        within_threshold = sum(1 for dev in deviations if dev <= threshold)
        score = within_threshold / len(deviations)
        print(f"Threshold {threshold:.1f}Å: {within_threshold}/{len(deviations)} = {score:.3f}")
        scores.append(score)
    
    return np.mean(scores)

def calculate_tm_score(model_path, reference_path, is_af2=False):
    """Calculate TM-score using TMalign"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.pdb') as temp_ref, \
         tempfile.NamedTemporaryFile(mode='w', suffix='.pdb') as temp_model:
        
        # Parse structures
        ref_parser = PDB.PDBParser(QUIET=True)
        ref_structure = ref_parser.get_structure('ref', reference_path)
        
        model_parser = PDB.PDBParser(QUIET=True) if str(model_path).endswith('.pdb') else PDB.MMCIFParser(QUIET=True)
        model_structure = model_parser.get_structure('model', model_path)
        
        # Save structures, handling AF2 specially
        io = PDB.PDBIO()
        
        if is_af2:
            # Create a class to select only receptor chain
            class ChainSelector(PDB.Select):
                def accept_chain(self, chain):
                    return chain.id == 'R'
            
            io.set_structure(ref_structure)
            io.save(temp_ref.name, select=ChainSelector())
        else:
            io.set_structure(ref_structure)
            io.save(temp_ref.name)
        
        io.set_structure(model_structure)
        io.save(temp_model.name)
        
        try:
            result = subprocess.run(['TMalign', temp_model.name, temp_ref.name], 
                                 capture_output=True, text=True, check=True)
            
            for line in result.stdout.split('\n'):
                if "TM-score=" in line and "(if normalized by length of Chain_2)" in line:
                    return float(line.split('=')[1].split('(')[0])
            
            return 0.0
            
        except Exception as e:
            print(f"Error calculating TM-score: {e}")
            return 0.0

def main():
    reference = Path("data/common/structures/6x18.pdb")
    models = {
        'chai': Path("data/projects/glp1r_glp1/chai/pred.model_idx_0.rank_0.cif"),
        'boltz': Path("results/glp1r_glp1/boltz/glp1r_glp1_model_0.cif"),
        'af3': Path("data/projects/glp1r_glp1/af3/fold_glp_1r_and_glp_1_model_0.cif"),
        'af2': Path("data/projects/glp1r_glp1/af2/AF-P43220-F1-model_v4.pdb")
    }
    
    print("\nCalculating metrics for GLP1R-GLP1 models...")
    print("-" * 50)
    
    for name, path in models.items():
        if not path.exists():
            continue
            
        print(f"\nProcessing {name}...")
        
        # Calculate TM-score with special handling for AF2
        tm_score = calculate_tm_score(path, reference, is_af2=(name == 'af2'))
        
        # Parse structures
        ref_parser = PDB.PDBParser(QUIET=True)
        model_parser = PDB.PDBParser(QUIET=True) if str(path).endswith('.pdb') else PDB.MMCIFParser(QUIET=True)
        
        ref_structure = ref_parser.get_structure('ref', reference)
        model_structure = model_parser.get_structure('model', path)
        
        # Calculate metrics
        rmsd = calculate_rmsd(model_structure, ref_structure)
        lddt = calculate_lddt_pli(model_structure, ref_structure)
        tm_score = calculate_tm_score(path, reference)
        
        print(f"\nResults for {name}:")
        print(f"RMSD: {rmsd:.3f}Å")
        print(f"LDDT-PLI: {lddt:.3f}")
        print(f"TM-score: {tm_score:.3f}")
        print("-" * 50)

if __name__ == "__main__":
    main()
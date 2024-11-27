# import packages
import boltz
import os
import subprocess

# create dicts
molecules = {
    "glp1r": {
        "type": "protein",
        "sequence": "MAGAPGPLRLALLLLGMVGRAGPRPQGATVSLWETVQKWREYRRQCQRSLTEDPPPATDLFCNRTFDEYACWPDGEPGSFVNVSCPWYLPWASSVPQGHVYRFCTAEGLWLQKDNSSLPWRDLSECEESKRGERSSPEEQLLFLYIIYTVGYALSFSALVIASAILLGFRHLHCTRNYIHLNLFASFILRALSVFIKDAALKWMYSTAAQQHQWDGLLSYQDSLSCRLVFLLMQYCVAANYYWLLVEGVYLYTLLAFSVLSEQWIFRLYVSIGWGVPLLFVVPWGIVKYLYEDEGCWTRNSNMNYWLIIRLPILFAIGVNFLIFVRVICIVVSKLKANLMCKTDIKCRLAKSTLTLIPLLGTHEVIFAFVMDEHARGTLRFIKLFTELSFTSFQGLMVAILYCFVNNEVQLEFRKSWERW",
    },
    "glp1": {
        "type": "protein",
        "sequence": "HAEGTFTSDVSSYLEGQAAKEFIAWLVKGRG",
    },
    "v0219": {
        "type": "smiles",
        "sequence": "FC(C1=CC=C(C2=NOC(CN3CC(CN4CCOCC4)CCC3)=N2)C=C1)(F)F", 
    },
    "vu045": {
        "type": "smiles",
        "sequence": "O=C(NC[C@H]1N(CCC1)C(C)C)C(C2=C3N(C4=C2C=CC=C4)C)=CN(C3=O)C5CCCC5",
    } 
}

# Define combinations
combinations = [
    {
        "name": "glp1r_glp1",
        "molecules": ["glp1r", "glp1"]
    },
    {
        "name": "glp1r_glp1_v0219",
        "molecules": ["glp1r", "glp1", "v0219"]
    },
    {
        "name": "glp1r_glp1_vu045",  # Using shorter name
        "molecules": ["glp1r", "glp1", "vu045"]
    }
]

def create_combined_fasta(combination, molecules):
    """Create a FASTA file combining multiple molecules"""
    filename = f"{combination['name']}.fasta"
    with open(filename, 'w') as f:
        for i, mol_name in enumerate(combination['molecules']):
            mol = molecules[mol_name]
            chain_id = chr(65 + i)  # A=65, B=66, C=67 in ASCII
            f.write(f">{chain_id}|{mol['type']}\n{mol['sequence']}\n")
    return filename

def run_boltz(fasta_file, output_dir):
    """Run Boltz prediction for a given FASTA file"""
    # Set environment variables for Mac M1/M2 compatibility
    env = os.environ.copy()
    env["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
    env["CUDA_VISIBLE_DEVICES"] = ""
    
    cmd = f"boltz predict {fasta_file} --use_msa_server --out_dir {output_dir}"
    print(f"Running: {cmd}")
    try:
        subprocess.run(cmd, shell=True, check=True, env=env)
        print(f"Successfully completed Boltz prediction for {fasta_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error running Boltz for {fasta_file}: {e}")

def main():
    # Create output directory if it doesn't exist
    base_output_dir = "boltz_combination_outputs"
    if not os.path.exists(base_output_dir):
        os.makedirs(base_output_dir)

    # Process each combination
    for combo in combinations:
        print(f"\nProcessing combination: {combo['name']}...")
        
        # Create combined FASTA file
        fasta_file = create_combined_fasta(combo, molecules)
        print(f"Created combined FASTA file: {fasta_file}")
        
        # Create combination-specific output directory
        output_dir = os.path.join(base_output_dir, combo['name'])
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Run Boltz
        run_boltz(fasta_file, output_dir)

if __name__ == "__main__":
    main()
# prepare_sequences.py

import os

# Create data directory if it doesn't exist
data_dir = "data/boltz/fasta"
os.makedirs(data_dir, exist_ok=True)

# Molecule information
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

def create_fasta_file(name, mol_type, sequence):
    """Create a FASTA file for a molecule"""
    filename = os.path.join(data_dir, f"{name}.fasta")
    with open(filename, 'w') as f:
        f.write(f">{name}|{mol_type}\n{sequence}\n")
    return filename

def main():
    # Create individual FASTA files
    for name, info in molecules.items():
        create_fasta_file(name, info["type"], info["sequence"])
        print(f"Created FASTA file for {name}")

if __name__ == "__main__":
    main()
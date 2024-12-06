# prepare_sequences.py

import os

# Create data directory if it doesn't exist
data_dir = "data/boltz/fasta"
os.makedirs(data_dir, exist_ok=True)

# Molecule information
molecules = {
    "glp1r": {
        "type": "protein",
        "sequence": "MAGAPGPLRLALLLLGMVGRAGPRPQGATVSLWETVQKWREYRRQCQRSLTEDPPPATDLFCNRTFDEYACWPDGEPGSFVNVSCPWYLPWASSVPQGHVYRFCTAEGLWLQKDNSSLPWRDLSECEESKRGERSSPEEQLLFLYIIYTVGYALSFSALVIASAILLGFRHLHCTRNYIHLNLFASFILRALSVFIKDAALKWMYSTAAQQHQWDGLLSYQDSLSCRLVFLLMQYCVAANYYWLLVEGVYLYTLLAFSVLSEQWIFRLYVSIGWGVPLLFVVPWGIVKYLYEDEGCWTRNSNMNYWLIIRLPILFAIGVNFLIFVRVICIVVSKLKANLMCKTDIKCRLAKSTLTLIPLLGTHEVIFAFVMDEHARGTLRFIKLFTELSFTSFQGLMVAILYCFVNNEVQLEFRKSWERWRLEHLHIQRDSSMKPLKCPTSSLSSGATAGSSMYTATCQASCS",
    },
    "glp1": {
        "type": "protein",
        "sequence": "HAEGTFTSDVSSYLEGQAAKEFIAWLVKGR",
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
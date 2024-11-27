# scripts/download_pdbs.py

import os
from urllib.request import urlretrieve

# define reference structure
reference_structures = {
    "6x18": {
        "description": "GLP-1R bound to GLP-1 (Cryo-EM)",
        "url": "https://files.rcsb.org/download/6X18.pdb",
        "citation": "DOI: 10.1038/s41586-020-2497-1"
    }
}

def download_pdb(pdb_id, url, output_dir):
    """download PDB file"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_file = os.path.join(output_dir, f"{pdb_id}.pdb")
    if not os.path.exists(output_file):
        print(f"downloading {pdb_id}...")
        urlretrieve(url, output_file)
        print(f"downloaded {pdb_id} to {output_file}")

    else:
        print(f"file {output_file} already exists, skipping download")

def main():
    # Set up paths relative to ai-struct-comparison
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Go up one level from scripts
    pdb_dir = os.path.join(base_dir, "data", "pdb", "structures")
    
    # Download each reference structure
    for pdb_id, info in reference_structures.items():
        download_pdb(pdb_id, info["url"], pdb_dir)
        
        # Create citation file
        with open(os.path.join(pdb_dir, f"{pdb_id}_info.txt"), 'w') as f:
            f.write(f"Structure: {pdb_id}\n")
            f.write(f"Description: {info['description']}\n")
            f.write(f"Citation: {info['citation']}\n")

if __name__ == "__main__":
    main()
import pymol
from pymol import cmd
import time

def view_structures():
    # Initialize PyMOL
    pymol.finish_launching(['pymol', '-qc'])
    
    # Load structures
    cmd.load("data/pdb/structures/6x18.pdb", "ground_truth")
    cmd.load("results/boltz/complexes/glp1r_glp1/boltz_results_glp1r_glp1/predictions/glp1r_glp1/glp1r_glp1_model_0.cif", "boltz_pred")
    
    time.sleep(2)
    
    # Clear everything first
    cmd.hide("everything", "all")
    
    # Select and show only the relevant chains
    cmd.select("gt_complex", "ground_truth and (chain R or chain P)")
    cmd.select("pred_complex", "boltz_pred and (chain A or chain B)")
    
    # Show only cartoon representation for the selected chains
    cmd.show("cartoon", "gt_complex")
    cmd.show("cartoon", "pred_complex")
    
    # Color the structures
    cmd.color("salmon", "ground_truth and chain R")  # receptor
    cmd.color("magenta", "ground_truth and chain P") # peptide
    cmd.color("cyan", "boltz_pred and chain A")      # predicted receptor
    cmd.color("yellow", "boltz_pred and chain B")    # predicted peptide
    
    # Position them separately
    cmd.alter_state(1, "ground_truth", "x-=30")
    cmd.alter_state(1, "boltz_pred", "x+=30")
    
    # Remove any leftover selections
    cmd.delete("gt_complex")
    cmd.delete("pred_complex")
    
    # Set background to black
    cmd.bg_color("black")
    
    # Ensure proper rendering
    cmd.set("cartoon_fancy_helices", 1)
    cmd.set("cartoon_transparency", 0)
    
    # Center view
    cmd.zoom("visible")
    
    # Save session
    cmd.save("comparison.pse")

if __name__ == "__main__":
    view_structures()
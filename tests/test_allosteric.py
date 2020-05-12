from pele_platform.constants import constants as cs
from pele_platform import main
import pandas as pd
import glob
import os

test_path = os.path.join(cs.DIR, "Examples")

yaml = os.path.join(test_path, "Allosteric/input_skipref.yaml")
def test_allosteric_skipref(yaml=yaml):

    job, _ = main.run_platform(yaml)

    # checkpoints
    files_refinement = glob.glob(os.path.join(job.pele_dir, "refinement_simulation/results/BestStructs/epoch*"))

    # test
    assert not files_refinement

yaml = os.path.join(test_path, "Allosteric/input_global.yaml")
def test_allosteric(energy_result=-1.51, yaml=yaml):

    job, _ = main.run_platform(yaml)

    # checkpoints
    output_csv = pd.read_csv(os.path.join(job.pele_dir, "output/clustering_output.csv"))
    best_energy = round(output_csv["binding_energy"].min(),2)
    nfiles = len(glob.glob(os.path.join(job.pele_dir, "output/refinement_input/*.pdb")))
    nfiles_refinement = len(glob.glob(os.path.join(job.pele_dir, "refinement_simulation/results/BestStructs/epoch*")))

    # test
    assert nfiles == job.n_components 
    assert best_energy == energy_result
    assert nfiles_refinement


yaml = os.path.join(test_path, "Allosteric/input_global_xtc.yaml")
def test_allosteric_xtc(energy_result=-1.51, yaml=yaml):

    job, _ = main.run_platform(yaml)

    # checkpoints
    output_csv = pd.read_csv(os.path.join(job.pele_dir, "output/clustering_output.csv"))
    best_energy = round(output_csv["binding_energy"].min(),2)
    nfiles = len(glob.glob(os.path.join(job.pele_dir, "output/refinement_input/*.pdb")))
    nfiles_refinement = len(glob.glob(os.path.join(job.pele_dir, "refinement_simulation/results/BestStructs/epoch*")))

    # test
    assert nfiles == job.n_components 
    assert best_energy == energy_result
    assert nfiles_refinement
import os
import shutil
import PELE_Platform.Utilities.PlopRotTemp.main as plop
import PELE_Platform.Utilities.Helpers.system_prep as sp
import PELE_Platform.Utilities.Helpers.helpers as hp


def create_template(system, res, pele_dir, forcefield):
    template_dir = os.path.join(pele_dir, "DataLocal/Templates/{}/HeteroAtoms/".format(forcefield))
    rotamers_dir = os.path.join(pele_dir, "DataLocal/LigandRotamerLibs")
    output_pdb = os.path.join(pele_dir, "miss_residue.pdb")
    syst = sp.SystemBuilder.build_system(system, None, res, pele_dir, output=output_pdb)
    print(syst.lig, res)
    plop.main(syst.lig, res, pele_dir, forcefield, 4, 1000, -1, mae_charges=False, clean=True)
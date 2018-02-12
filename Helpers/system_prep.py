import os
from schrodinger import structure as st
import StringIO
import MSM_PELE.Helpers.helpers as hp
from prody import *


def build_complex(receptor, ligand):
    """ From the receptor and ligand in pdb build
        another pdb with the whole complex
    """
    complex_content = []

    name = os.path.basename(os.path.splitext(receptor)[0])
    dirname = os.path.dirname(receptor)
    complex = os.path.join(dirname, "{}_complex.pdb".format(name)) 

    with open(receptor, 'r') as pdb_file:
        receptor_text = [line for line in pdb_file if line.startswith("ATOM") or line.startswith("HETATM") or line.startswith("TER")]

    with open(ligand, 'r') as pdb_file:
        ligand_text = [line for line in pdb_file if line.startswith("HETATM")]

    if not receptor_text  or not ligand_text:
        raise ValueError("The ligand_pdb was not properly created check your mae file")

    complex_content.extend(receptor_text + ["TER\n"] + ligand_text + ["END"])
 
    with open(complex, 'w') as fout:
        fout.write("".join(complex_content))
    
    return complex


def convert_mae(ligands):
    """
       Desciption: From each structure retrieve
       a .mae file of the ligand in the receptor.

       Output:
            structure_mae: ligand
            res = residue
    """

    
    for structure in st.StructureReader(ligands):
        for residue in structure.residue:
            res = residue.pdbres.strip()
        str_name = "{}".format(res)
        try:
            structure.write(str_name + ".mae")
        except ValueError:
            str_name = "{}".format(res)
        finally:
            structure.write(str_name + ".mae")
            structure_mae = "{}.mae".format(str_name)
    return structure_mae, res


def retrieve_receptor(system, residue):
    """
    This function returns receptor of the complex of interest.

    :param complex: system format pdb

    :output: receptor text
    """
    ligand = os.path.abspath("lig.pdb")
    with open(system, 'r') as pdb_file:
        receptor_text = [line for line in pdb_file if line.startswith("ATOM")]
    with open(system, 'r') as pdb_file:
        ligand_text = [line for line in pdb_file if line[17:20].strip() == residue]
    if not receptor_text  or not ligand_text:
        raise ValueError("Something went wrong when extracting the ligand. Ligand must be a HETATOM")
    with open(ligand, "w") as fout:
	fout.write("".join(ligand_text))

    return "".join(receptor_text), ligand

def convert_pdb(lig_mae):
    name = os.path.basename(os.path.splitext(lig_mae)[0])
    dirname = os.path.dirname(lig_mae)
    for structure in st.StructureReader(lig_mae):
        struct_pdb = os.path.join(dirname, "{}.pdb".format(name))
        structure.write(struct_pdb)
    return struct_pdb
    
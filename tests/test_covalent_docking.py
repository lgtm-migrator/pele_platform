import glob
import os
import pytest

import tests.utils
from pele_platform import main
from pele_platform.constants import constants


test_path = os.path.join(constants.DIR, "Examples", "covalent_docking")

expected_params1 = [
    '"type": "localNonBondingEnergy"',
    '"radius": 5',
    '"sideChainsToPerturb": { "links": {"ids": ["A:273"] } },',
    '"overlapFactor": 0.77,',
    '"numberOfTrials": 12,',
    '"atLeastOneSelectedTrial": true',
]

expected_params2 = ['"refinementAngle": 15.0']


def test_covalent_docking_production():
    """
    Runs covalent docking in test mode to ensure all metrics and user-defined variables are set correctly in pele.conf
    and the simulation finished without any errors.
    """
    yaml_file = os.path.join(test_path, "input2.yaml")
    job, sel, job2 = main.run_platform_from_yaml(yaml_file)

    errors = tests.utils.check_file(job.pele_dir, "pele.conf", expected_params1, [])
    errors = tests.utils.check_file(
        job2.pele_dir, "pele.conf", expected_params1 + expected_params2, errors
    )
    assert not errors

    clusters = glob.glob(
        os.path.join(job2.pele_dir, "results", "clusters", "cluster*.pdb")
    )
    assert len(clusters) > 0


@pytest.mark.parametrize("input_yaml", ["input1.yaml", "input3.yaml"])
def test_ligands(input_yaml):
    """
    Runs covalent docking in test mode to check parametrization of covalent ligands.
    """
    yaml_file = os.path.join(test_path, input_yaml)
    main.run_platform_from_yaml(yaml_file)

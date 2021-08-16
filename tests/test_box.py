import os
import pytest

import pele_platform.constants.constants as cs
import pele_platform.main as main
import tests.utils

test_path = os.path.join(cs.DIR, "Examples")

BOX_RES_ARGS = os.path.join(test_path, "box/input.yaml")
OUT_IN_ARGS = os.path.join(test_path, "out_in/input_box_center.yaml")
GPCR_ARGS = os.path.join(test_path, "box/input_gpcr.yaml")

BOX_RES = [
    '"fixedCenter": [-3.6559998989105225, 64.46499633789062, 2.3980000019073486]',
]

OUT_IN_BOX = [
    '"fixedCenter": [100.0, 100.0, 100.0]',
    '"radius": 100.0,'
]

GPCR_VALUES = [
    '"radius": 19.970223159033843,',
    '"fixedCenter": [-71.78435134887695, -13.431749963760375, -42.46209926605225]',
]


@pytest.mark.parametrize(
    ("yaml_file", "expected_lines"),
    [
        (BOX_RES_ARGS, BOX_RES),
        (OUT_IN_ARGS, OUT_IN_BOX),
        (GPCR_ARGS, GPCR_VALUES)
    ],
)
def test_box_center_from_residue(yaml_file, expected_lines):
    """
    Checks if box center is correctly set in pele.conf:
     - when it is extracted from an atom string
     - when it's set by the user using coordinates (and it should ignore calculated one).

    Parameters
    -----------
    yaml_file : str
        Path to YAML file.
    expected_lines : List[str]
        List of lines expected to be found in pele.conf file.
    """
    errors = []
    job = main.run_platform_from_yaml(yaml_file)
    errors = tests.utils.check_file(job[0].pele_dir, "pele.conf", expected_lines, errors)
    assert not errors

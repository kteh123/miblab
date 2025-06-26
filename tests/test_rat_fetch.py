import os
import shutil
import pytest
from miblab import rat_fetch

@pytest.mark.parametrize("dataset", [
    None,                       # default: should fetch 'bosentan_highdose'
    "bosentan_highdose",        # explicit group
    "all",                      # all groups
])
def test_rat_fetch(dataset, tmp_path):
    """
    Test rat_fetch with different dataset options:
    - Default (None) → should download bosentan_highdose
    - Specific group
    - All groups
    """

    test_folder = tmp_path / "download"

    try:
        paths = rat_fetch(dataset=dataset, folder=str(test_folder))
    except Exception as e:
        pytest.fail(f"rat_fetch raised an exception for dataset={dataset!r}: {e}")

    # Check: folder was created
    assert test_folder.exists(), "Target folder was not created"

    # Check: at least one file was downloaded
    downloaded_files = list(test_folder.glob("*.zip"))
    assert len(downloaded_files) > 0, f"No ZIP files downloaded for dataset={dataset!r}"

    print(f"{len(downloaded_files)} files downloaded successfully for dataset={dataset!r}")
import filecmp
import os
from pathlib import Path
from zipfile import ZipFile

import pytest


@pytest.mark.require_optional_deps
@pytest.mark.parametrize(
    'n',
    [
        pytest.param(
            1, marks=pytest.mark.filecopy('update_changelog/test_1/ChangeLog.md', '__tmp__')
        ),
        pytest.param(
            2, marks=pytest.mark.filecopy('update_changelog/test_2/ChangeLog.md', '__tmp__')
        ),
    ],
)
def test_update_changelog(tmp_path, n):
    from scripts.update_changelog import update_changelog

    ZipFile(f'update_changelog/test_{n}/repo.zip').extractall(tmp_path)
    os.chdir(tmp_path)
    update_changelog('ChangeLog.md')
    assert filecmp.cmp(
        'ChangeLog.md',
        Path(__file__).parent / 'update_changelog' / f'test_{n}' / 'new_ChangeLog.md',
    )

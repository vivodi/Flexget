import os
import shutil
from pathlib import Path

import pytest
import vcr
from click.testing import CliRunner

from flexget.ui import v1, v2
from scripts.dev_tools import bump_version, cli_bundle_webui, get_changelog, version


def test_version(tmp_path):
    os.makedirs(tmp_path / 'flexget', exist_ok=True)
    shutil.copy('dev_tools/dev_version.py', tmp_path / 'flexget' / '_version.py')
    os.chdir(tmp_path / 'flexget')
    runner = CliRunner()
    result = runner.invoke(version)
    assert result.exit_code == 0
    assert result.output == '3.13.19.dev\n'


@pytest.mark.parametrize(
    ('bump_from', 'bump_to', 'version'),
    [
        (
            'dev',
            'release',
            '3.13.19',
        ),
        (
            'release',
            'dev',
            '3.13.20.dev',
        ),
    ],
)
def test_bump_version(tmp_path, bump_from, bump_to, version):
    os.makedirs(tmp_path / 'flexget', exist_ok=True)
    shutil.copy(
        Path(__file__).parent / f'dev_tools/{bump_from}_version.py',
        tmp_path / 'flexget' / '_version.py',
    )
    os.chdir(tmp_path / 'flexget')
    runner = CliRunner()
    result = runner.invoke(bump_version, [bump_to])
    assert result.exit_code == 0
    with open(tmp_path.joinpath('flexget/_version.py')) as f:
        assert f"__version__ = '{version}'\n" in f


@vcr.use_cassette('cassettes/test_cli_bundle_webui.yaml')
@pytest.mark.parametrize('args', [[], ['--version', 'v2'], ['--version', 'v1'], ['--version', '']])
@pytest.mark.xdist_group(name="bundle webui")
def test_cli_bundle_webui(args):
    v1_path = Path(v1.__file__).parent / 'app'
    v2_path = Path(v2.__file__).parent / 'dist'
    shutil.rmtree(v1_path, ignore_errors=True)
    shutil.rmtree(v2_path, ignore_errors=True)
    runner = CliRunner()
    result = runner.invoke(cli_bundle_webui, args)
    assert result.exit_code == 0
    if 'v1' in args:
        assert v1_path.is_dir()
    elif 'v2' in args:
        assert v2_path.is_dir()
    else:
        assert v1_path.is_dir()
        assert v2_path.is_dir()


@vcr.use_cassette('cassettes/test_get_changelog.yaml')
def test_get_changelog():
    runner = CliRunner()
    result = runner.invoke(get_changelog, ['v3.13.6'])
    assert result.exit_code == 0
    assert result.output == (
        '[all commits](https://github.com/Flexget/Flexget/compare/v3.13.5...v3.13.6)\n'
        '### Changed\n'
        '- Strictly ignore 19xx-20xx from episode parsing\n'
        '- Strictly ignore 19xx-20xx from episode parsing\n'
    )

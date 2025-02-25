import os
import shutil
from pathlib import Path

import pytest
from click.testing import CliRunner

import flexget
from scripts.dev_tools import bump_version, cli_bundle_webui, get_changelog, version


@pytest.mark.require_optional_deps
@pytest.mark.online
class TestDevTools:
    @pytest.mark.filecopy('dev_tools/dev_version.py', '__tmp__/flexget/_version.py')
    def test_version(self, tmp_path):
        os.chdir(tmp_path)
        runner = CliRunner()
        result = runner.invoke(version)
        assert result.exit_code == 0
        assert result.output == '3.13.19.dev\n'

    @pytest.mark.parametrize(
        ('bump_type', 'version'),
        [
            pytest.param(
                'release',
                '3.13.19',
                marks=pytest.mark.filecopy(
                    'dev_tools/dev_version.py', '__tmp__/flexget/_version.py'
                ),
            ),
            pytest.param(
                'dev',
                '3.13.20.dev',
                marks=pytest.mark.filecopy(
                    'dev_tools/release_version.py', '__tmp__/flexget/_version.py'
                ),
            ),
        ],
    )
    def test_bump_version(self, tmp_path, bump_type, version):
        os.chdir(tmp_path)
        runner = CliRunner()
        result = runner.invoke(bump_version, [bump_type])
        assert result.exit_code == 0
        with open(tmp_path.joinpath('flexget/_version.py')) as f:
            assert f"__version__ = '{version}'\n" in f

    @pytest.mark.parametrize(
        'args', [[], ['--version', 'v2'], ['--version', 'v1'], ['--version', '']]
    )
    @pytest.mark.xdist_group(name="bundle webui")
    def test_cli_bundle_webui(self, args):
        os.environ['BUNDLE_WEBUI'] = 'true'
        v1 = Path(flexget.ui.v1.__file__).parent / 'app'
        v2 = Path(flexget.ui.v2.__file__).parent / 'dist'
        shutil.rmtree(v1, ignore_errors=True)
        shutil.rmtree(v2, ignore_errors=True)
        runner = CliRunner()
        result = runner.invoke(cli_bundle_webui, args)
        assert result.exit_code == 0
        if 'v1' in args:
            assert v1.is_dir()
        elif 'v2' in args:
            assert v2.is_dir()
        else:
            assert v1.is_dir()
            assert v2.is_dir()

    def test_get_changelog(self):
        runner = CliRunner()
        result = runner.invoke(get_changelog, ['v3.13.6'])
        assert result.exit_code == 0
        assert result.output == (
            '[all commits](https://github.com/Flexget/Flexget/compare/v3.13.5...v3.13.6)\n'
            '### Changed\n'
            '- Strictly ignore 19xx-20xx from episode parsing\n'
            '- Strictly ignore 19xx-20xx from episode parsing\n'
        )

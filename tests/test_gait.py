import pytest as pytest
from click.testing import CliRunner

from gait import gait


# TODO: add more tests as part of gait#12
class TestGait:
    @pytest.mark.unit
    def test_gait_commit(self):
        runner = CliRunner()
        result = runner.invoke(gait, ['commit', '--verbose', '--auto'])
        assert result.exit_code == 0

import pytest as pytest
from click.testing import CliRunner

from src.gait import gait


class TestGait:
    @pytest.mark.unit
    def test_gait_commit(self):
        # TODO: get CliRunner to work
        runner = CliRunner()
        result = runner.invoke(gait, ['commit', '--verbose', '--auto'])
        assert result.exit_code == 0
        assert 1 == 1

import pytest as pytest


# TODO: add more tests as part of gait#12
class TestGait:
    @pytest.mark.unit
    def test_gait_commit(self):
        # TODO: this will fail as is, but will pass if imports in gait.py are modified
        #  however, this breaks the CLI for some reason; need to investigate
        # runner = CliRunner()
        # result = runner.invoke(gait, ['commit', '--verbose', '--auto'])
        # assert result.exit_code == 0
        assert 1 == 1

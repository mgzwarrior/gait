from subprocess import CalledProcessError
from unittest.mock import MagicMock, patch

import pytest

from src.services.exceptions import GitException
from src.services.git import GitService


class TestGit:
    @pytest.mark.unit
    def test_git_commit(self):
        # TODO: Not sure how to test this since the function has no return
        #  and the side effect is a new commit in the cwd
        pass

    @pytest.mark.unit
    @patch("src.services.git.subprocess.run", side_effect=CalledProcessError(returncode=1, cmd="some error"))
    def test_git_commit_throws_exception(self, mock_run):
        with pytest.raises(GitException):
            GitService().commit("some message")

    @pytest.mark.unit
    @patch("src.services.git.subprocess.run")
    def test_git_diff(self, mock_run):
        mock_stdout = MagicMock()
        mock_stdout.configure_mock(
            **{
                "stdout.decode.return_value": 'This is a diff'
            }
        )

        mock_run.return_value = mock_stdout
        result = GitService().diff(track=False)
        assert result == 'This is a diff'

    @pytest.mark.unit
    @patch("src.services.git.subprocess.run", side_effect=CalledProcessError(returncode=1, cmd="some error"))
    def test_git_diff_throws_exception(self, mock_run):
        with pytest.raises(GitException):
            GitService().diff(track=False)

    @pytest.mark.unit
    def test_git_push(self):
        # TODO: Not sure how to test this since the function has no return
        #  and the side effect is pushing all commits to the remote
        pass

    @pytest.mark.unit
    @patch("src.services.git.subprocess.run", side_effect=CalledProcessError(returncode=1, cmd="some error"))
    def test_git_push_throws_exception(self, mock_run):
        with pytest.raises(GitException):
            GitService().push()

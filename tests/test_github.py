from subprocess import CalledProcessError
from unittest.mock import patch

import pytest

from src.services.exceptions import GitHubException
from src.services.github import GitHubService


class TestGithub:
    @pytest.mark.unit
    def test_github_create_pull_request(self):
        # TODO: Not sure how to test this since the function has no return
        #  and the side effect is a PR being created in GitHub
        pass

    @pytest.mark.unit
    @patch("src.services.github.subprocess.run", side_effect=CalledProcessError(returncode=1, cmd="some error"))
    def test_github_create_pull_request_throws_exception(self, mock_run):
        with pytest.raises(GitHubException):
            GitHubService().create_pull_request("Test Title", "Test Message")

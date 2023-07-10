import subprocess

from .exceptions import GitHubException


class GitHubService:
    @staticmethod
    def create_pull_request(title: str, message: str) -> None:
        cmd = [f"gh pr create --title {title} --body {message}"]

        try:
            # Disable for testing
            subprocess.run(cmd, shell=True, check=True)
        except subprocess.CalledProcessError as exc:
            raise GitHubException(exc) from exc

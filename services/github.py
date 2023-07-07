import subprocess

from services.exceptions import GitHubException


class GitHubService:
    @staticmethod
    def create_pull_request(title: str, message: str) -> None:
        cmd = [f"gh pr create --title {title} --body {message}"]

        try:
            subprocess.run(cmd, shell=True, check=True)
        except subprocess.CalledProcessError as exc:
            raise GitHubException(exc) from exc
"""Git service module."""
import subprocess

from exceptions import GitException


class GitService:
    """Git service class"""
    @staticmethod
    def commit(message: str) -> None:
        """Commit with passed message."""
        cmd = ['git commit -m', message]

        try:
            subprocess.run(cmd, shell=True, check=True)
        except subprocess.CalledProcessError as exc:
            raise GitException(exc) from exc

    @staticmethod
    def diff() -> str:
        """Get diff."""
        cmd = ['git --no-pager diff']

        try:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True, check=True)
        except subprocess.CalledProcessError as exc:
            raise GitException(exc) from exc

        return str(result.stdout)

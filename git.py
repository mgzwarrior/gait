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
            # Disable for testing
            # subprocess.run(cmd, shell=True, check=True)
            pass
        except subprocess.CalledProcessError as exc:
            raise GitException(exc) from exc

    @staticmethod
    def diff() -> None:
        """Get diff."""
        cmd = ['git --no-pager diff']

        try:
            with open("diff.txt", "w", encoding="utf-8") as diff_file:
                subprocess.run(cmd, stdout=diff_file, shell=True, check=True)
        except subprocess.CalledProcessError as exc:
            raise GitException(exc) from exc

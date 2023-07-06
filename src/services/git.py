import subprocess
import uuid

from .exceptions import GitException


class GitService:
    @staticmethod
    def commit(message: str) -> None:
        cmd = ["git commit -m", message]

        try:
            # Disable for testing
            # subprocess.run(cmd, shell=True, check=True)
            pass
        except subprocess.CalledProcessError as exc:
            raise GitException(exc) from exc

    @staticmethod
    def diff() -> str:
        cmd = ["git --no-pager diff"]
        filename = f"diffs/diff-{uuid.uuid1()}.txt"

        try:
            with open(filename, "w", encoding="utf-8") as diff_file:
                subprocess.run(cmd, stdout=diff_file, shell=True, check=True)
        except subprocess.CalledProcessError as exc:
            raise GitException(exc) from exc

        return filename

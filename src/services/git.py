import os
import subprocess
import uuid
from pathlib import Path

from .exceptions import GitException


class GitService:
    @staticmethod
    def commit(message: str) -> None:
        try:
            # Disable for testing
            subprocess.run(
                f"git add . ; git commit -m '{message}'", shell=True, check=True
            )
        except subprocess.CalledProcessError as exc:
            raise GitException(exc) from exc

    @staticmethod
    def diff(track: bool) -> str:
        cmd = ["git --no-pager diff"]
        cur_path = os.path.abspath(os.curdir)
        filename = f"src/diffs/diff-{uuid.uuid1()}.txt"

        try:
            with open(
                os.path.join(cur_path, filename), "w", encoding="utf-8"
            ) as diff_file:
                subprocess.run(cmd, stdout=diff_file, shell=True, check=True)
            with open(filename, "w", encoding="utf-8") as diff_file:
                if track:
                    subprocess.run(cmd, stdout=diff_file, shell=True, check=True)
                else:
                    return str(
                        subprocess.run(
                            cmd, shell=True, capture_output=True, check=True
                        ).stdout
                    )
        except subprocess.CalledProcessError as exc:
            raise GitException(exc) from exc

        return filename

    @staticmethod
    def push() -> None:
        cmd = ["git push"]

        try:
            # Disable for testing
            subprocess.run(cmd, shell=True, check=True)
        except subprocess.CalledProcessError as exc:
            raise GitException(exc) from exc

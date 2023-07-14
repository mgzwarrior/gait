import os
import subprocess
import uuid

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
            if track:
                with open(os.path.join(cur_path, filename), "w", encoding="utf-8") as diff_file:
                    subprocess.run(cmd, stdout=diff_file, shell=True, check=True)
            else:
                data = subprocess.run(
                    cmd, shell=True, stdout=subprocess.PIPE, check=True
                )
                result = data.stdout.decode("utf-8")
                return result
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

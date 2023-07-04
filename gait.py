"""Main gait module, contains CLI commands created via Click."""
import json
import logging

import click

from exceptions import GitException, OpenAIException
from git import GitService
from gpt import OpenAIService

logger = logging.getLogger("gait")
logging.basicConfig(filename="gait.log", filemode="w", level=logging.DEBUG)


@click.group()
def gait() -> None:
    """Gait CLI."""
    return None


@gait.command()
@click.option("--verbose", "-v", help="Verbose mode.", is_flag=True)
def commit(verbose) -> None:
    """Generate a commit message."""
    git_service = GitService()
    openai_service = OpenAIService()

    try:
        git_service.diff()
    except GitException as exc:
        logger.error(exc)
        raise click.ClickException(str(exc))

    if verbose:
        print("Git full diff:")
        with open("diff.txt", "r", encoding="utf-8") as diff_file:
            print(diff_file.read())

    try:
        with open("diff.txt", "r", encoding="utf-8") as diff_file:
            models = json.loads(openai_service.generate_commit_message(diff_file.read()))
            logger.info(json.dumps(models, indent=4))
    except OpenAIException as exc:
        logger.error(exc)
        raise click.ClickException(str(exc))

    if verbose:
        print("ChatGPT full response:")
        print(json.dumps(models, indent=4))

    message = json.dumps(models["choices"][0]["text"], indent=4)

    print(f"ChatGPT generated the following commit message: '{message}'")

    print("Would you like to commit this message? [y/n/edit]")

    choice = input()

    if choice == "y":
        print("Committing...")
        try:
            git_service.commit(message)
        except GitException as exc:
            logger.error(exc)
            raise click.ClickException(str(exc))
    elif choice == "edit":
        print("Please enter your commit message below:")
        user_commit_message = input()
        print("Committing...")
        try:
            git_service.commit(user_commit_message)
        except GitException as exc:
            logger.error(exc)
            raise click.ClickException(str(exc))
    else:
        print("Aborting...")


if __name__ == "__main__":
    gait()

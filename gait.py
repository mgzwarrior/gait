import json
import logging

import click
import click_config_file

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
@click.option("--auto", "-a", default=False, help="Automatic commit mode.", is_flag=True)
@click.option("--verbose", "-v", default=False, help="Verbose mode.", is_flag=True)
@click_config_file.configuration_option(config_file_name=".gaitconfig")  # Note that this does not work implicitly
def commit(auto, verbose) -> None:
    git_service = GitService()
    openai_service = OpenAIService()

    try:
        diff_fn = git_service.diff()
    except GitException as exc:
        logger.error(exc)
        raise click.ClickException(str(exc))

    if verbose:
        print("Git full diff:")
        with open(diff_fn, "r", encoding="utf-8") as diff_file:
            print(diff_file.read())

    try:
        with open(diff_fn, "r", encoding="utf-8") as diff_file:
            models = json.loads(openai_service.generate_commit_message(diff_file.read()))
            logger.info(json.dumps(models, indent=4))
    except OpenAIException as exc:
        logger.error(exc)
        raise click.ClickException(str(exc))

    if verbose:
        print("ChatGPT full response:")
        print(json.dumps(models, indent=4))

    message = json.dumps(models["choices"][0]["text"], indent=4)

    if auto:
        __git_commit(git_service, message)
    else:
        print(f"ChatGPT gene rated the following commit message: '{message}'")

        print("Would you like to commit this message? [y/n/edit]")

        choice = input()

        if choice == "y":
            __git_commit(git_service, message)
        elif choice == "edit":
            print("Please enter your commit message below:")
            user_commit_message = input()
            __git_commit(git_service, user_commit_message)
        else:
            print("Aborting...")


def __git_commit(service: GitService, message: str) -> None:
    print("Committing...")
    try:
        service.commit(message)
    except GitException as exc:
        logger.error(exc)
        raise click.ClickException(str(exc))


if __name__ == "__main__":
    gait()

import json
import logging

import click
import click_config_file

from services.exceptions import GitException, OpenAIException
from services.git import GitService
from services.openai import OpenAIService

logger = logging.getLogger("gait")
logging.basicConfig(filename="gait.log", filemode="w", level=logging.DEBUG)

CONFIG_FILENAME = ".gaitconfig"


@click.group()
def gait() -> None:
    return None


@gait.command()
@click.option(
    "--auto", "-a", default=False, help="Automatic commit mode.", is_flag=True
)
@click.option("--verbose", "-v", default=False, help="Verbose mode.", is_flag=True)
@click_config_file.configuration_option(
    config_file_name=CONFIG_FILENAME
)  # Note that this does not work implicitly
def commit(auto, verbose) -> None:
    git_service = GitService()
    openai_service = OpenAIService()

    try:
        diff_fn = git_service.diff()
    except GitException as exc:
        logger.error(exc)
        raise click.ClickException(str(exc))

    try:
        with open(diff_fn, "r", encoding="utf-8") as diff_file:
            diff = diff_file.read()
            commit_message = json.loads(openai_service.generate_commit_message(diff))

            if verbose:
                print(f"Diff: {diff}")
                print(
                    f"Generated commit message: {json.dumps(commit_message, indent=4)}"
                )

            logger.info(json.dumps(commit_message, indent=4))
    except OpenAIException as exc:
        logger.error(exc)
        raise click.ClickException(str(exc))

    message = json.dumps(commit_message["choices"][0]["text"], indent=4)

    if auto:
        __git_commit(git_service, message)
    else:
        print(f"ChatGPT generated the following commit message: '{message}'")
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

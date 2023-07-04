import json
import logging
import os
import subprocess
from getpass import getpass
from pathlib import Path

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
    """Gait is a CLI tool that uses OpenAI's ChatGPT to generate commit messages.
    It is designed to be used with Git.
    """
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
    """This command is ued to generate a commit message using ChatGPT.
    The message is generated based on the diff of the current branch and the master branch.
    There are two modes for this command: interactive mode (default) and automatic mode.
    """
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


@gait.command()
@click.option("--verbose", "-v", default=False, help="Verbose mode.", is_flag=True)
@click_config_file.configuration_option(
    config_file_name=CONFIG_FILENAME
)  # Note that this does not work implicitly
def configure(verbose) -> None:
    """This command is used to configure Gait.
    If required, it will prompt the user for their OpenAI API key and test the connection.
    """
    print("Setting up Gait...")

    if os.getenv("OPENAI_API_KEY"):
        __test_openai_connection(verbose)
    else:
        print("In order to use Gait, you must setup an OpenAI API key for your account.")
        print("Navigating to https://platform.openai.com/account/api-keys to create a new key.")

        key = getpass(prompt="Please enter your OpenAI API Key: ")

        # TODO: fix this part since env var does not persist
        os.environ["OPENAI_API_KEY"] = key

        __test_openai_connection(verbose)

    # TODO: Add git config verification

    print("Gait setup complete!")


def __git_commit(service: GitService, message: str) -> None:
    print("Committing...")

    try:
        service.commit(message)
    except GitException as exc:
        logger.error(exc)
        raise click.ClickException(str(exc))


def __test_openai_connection(verbose: bool) -> None:
    try:
        openai_service = OpenAIService()
        response = openai_service.test_connection()
    except OpenAIException as exc:
        logger.error(exc)
        raise click.ClickException(str(exc))

    if verbose:
        print(f"OpenAI response: {json.dumps(response, indent=4)}")

    print("OpenAI setup complete!")


if __name__ == "__main__":
    gait()

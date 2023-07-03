"""Main gait module, contains CLI commands created via Click."""
import json
import logging

import click

from exceptions import GitException
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
    service = OpenAIService()

    try:
        models = json.loads(service.generate_commit_message())
    except GitException as exc:
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
        # Disabled for testing
        # service.commit(message)
    elif choice == "edit":
        print("Please enter your commit message below:")
        user_commit_message = input()
        print("Committing...")
        # Disabled for testing
        # service.commit(user_commit_message)
    else:
        print("Aborting...")

    logger.info(json.dumps(models, indent=4))


if __name__ == "__main__":
    gait()

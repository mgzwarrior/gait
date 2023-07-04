import json
import logging

import click

from exceptions import GitException
from gpt import OpenAIService

logger = logging.getLogger("gait")
logging.basicConfig(filename="gait.log", filemode="w", level=logging.DEBUG)


@click.group()
def gait() -> None:
    return None


@gait.command()
def commit() -> None:
    service = OpenAIService()

    try:
        models = json.loads(service.generate_commit_message())
    except GitException as error:
        logger.error(error)

        raise click.ClickException(str(error))

    print(json.dumps(models, indent=4))
    logger.info(json.dumps(models, indent=4))


if __name__ == "__main__":
    gait()

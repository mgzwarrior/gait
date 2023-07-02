import json
import logging

import click

from gpt import OpenAIService

logger = logging.getLogger("gait")
logging.basicConfig(filename="gait.log", filemode="w", level=logging.DEBUG)


@click.group()
def gait() -> None:
    return None


@gait.command()
def commit() -> None:
    service = OpenAIService()
    models = json.loads(service.generate_commit_message())
    print(json.dumps(models, indent=4))

    logger.info(json.dumps(models, indent=4))


if __name__ == "__main__":
    gait()

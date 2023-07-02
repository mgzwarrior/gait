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
    #  There is a bug in this line.  The generate_commit_message method returns
    #  malformed JSON that uses single-quoted strings.  This makes it difficult to play with the results.
    models = json.loads(service.generate_commit_message(diff=""))
    print(models)

    logger.info(json.dumps(models, indent=4))


if __name__ == "__main__":
    gait()

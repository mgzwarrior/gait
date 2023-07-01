import logging

import click

logger = logging.getLogger("gait-logger")


@click.group()
def gait() -> None:
    return None


@gait.command()
@click.argument("commit")
def commit() -> None:
    pass


if __name__ == "__main__":
    gait()

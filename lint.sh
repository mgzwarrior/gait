#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

isort --profile black . --skip-gitignore
black .
# mypy --strict *.py & pylint *.py
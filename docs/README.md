<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./img/logo_dark.png">
  <img alt="Shows the gait logo in light mode and dark mode." src="./img/logo_light.png" width=50% height=50%>
</picture>

A git AI productivity tool.

[![Pylint](https://github.com/mgzwarrior/gait/actions/workflows/pylint.yml/badge.svg)](https://github.com/mgzwarrior/gait/actions/workflows/pylint.yml)
[![update-gh-pages-branch](https://github.com/mgzwarrior/gait/actions/workflows/mkdocs.yml/badge.svg)](https://github.com/mgzwarrior/gait/actions/workflows/mkdocs.yml)
[![pages-build-deployment](https://github.com/mgzwarrior/gait/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/mgzwarrior/gait/actions/workflows/pages/pages-build-deployment)
[![CodeQL](https://github.com/mgzwarrior/gait/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/mgzwarrior/gait/actions/workflows/github-code-scanning/codeql)

## Installation

```bash
pyenv install

pip3 install -r requirements.txt -r test-requirements.txt
```

## Setup

Before using gait, you must create an OpenAI secret API key.  To do this, login to your OpenAI account (or create one if you don't already have one, they are free!), click "Personal" in the top right, then click "View API keys" in the dropdown that appears.  On the next page, click "Create new secret key" and give it a name.  Copy the key that is created.

You will need to add this key to an environment variable called `OPENAI_API_KEY`.

### zsh

Open your `.zshrc` and add the following line:

```
export OPENAI_API_KEY="<insert-api-key-here>"
```

Run `source ~/.zshrc` in an open terminal window or open a new one and verify by running `echo $OPENAI_API_KEY`.

## Usage

```commandline
python3 gait.py --help

Usage: gait.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  commit

# TODO - python3 gait.py commit
```

## Development

To lint the code using [Qodana](https://www.jetbrains.com/help/qodana/getting-started.html), run:

```bash
qodana scan --show-report
```

### Updating Requirements

When new libraries are added using pip, be sure to update the `requirements.txt` file by running:

```bash
pip3 freeze > requirements.txt
```

### Linting

Lint the entire project by running pylint using the following command:

```bash
pylint $(git ls-files '*.py')
```

This is also run automatically as a GitHub Workflow for all pushes to the `main` branch.

### Documentation

Use the `/docs` folder for documentation.

Docs can be served locally using mkdocs with the following command:

```bash
mkdocs serve
```

## Resources

- [OpenAI Cookbook](https://github.com/openai/openai-cookbook) - a GitHub repo containing a number of userful tips for using the OpenAI API.
- [OpenAI Tokenizer](https://platform.openai.com/tokenizer) - a utility from OpenAI to tokenize a given text prompt.
- :construction: [click-man](https://github.com/click-contrib/click-man) - a library to create man pages for click applications.
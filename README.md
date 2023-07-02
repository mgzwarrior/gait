# gAIt

A git AI productivity tool.

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
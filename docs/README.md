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

### Production (Beta)

```bash
pip install --index-url https://test.pypi.org/simple/ src --user
```

### Development

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
Usage: gait.py [OPTIONS] COMMAND [ARGS]...

  Gait is a CLI tool that uses OpenAI's ChatGPT to generate commit messages.
  It is designed to be used with Git.

Options:
  --help  Show this message and exit.

Commands:
  commit     This command is ued to generate a commit message using ChatGPT.
  configure  This command is used to configure Gait.
  push       This command is ued to push changes to the remote repository...
```

### Configure

```commandline
Usage: gait.py configure [OPTIONS]

  This command is used to configure Gait. If required, it will prompt the user
  for their OpenAI API key and test the connection.

Options:
  -v, --verbose  Verbose mode.
  --config FILE  Read configuration from FILE.
  --help         Show this message and exit.
```

### Commit

```commandline
Usage: gait.py commit [OPTIONS]

  This command is ued to generate a commit message using ChatGPT. The message
  is generated based on the diff of the current branch and the master branch.
  There are two modes for this command: interactive mode (default) and
  automatic mode.

Options:
  -a, --auto          Automatic commit mode.
  -m, --message TEXT  Commit message.
  -s, --skip          Skip OpenAI message generation.
  -t, --track         Track commit flow to train the OpenAI model
  -v, --verbose       Verbose mode.
  --config FILE       Read configuration from FILE.
  --help              Show this message and exit.
```

#### Examples

1. Use gait in interactive mode:

```commandline
$ python3 gait.py commit
ChatGPT gene rated the following commit message: '"\n\nAdd commit command help and example usage to README.md"'
Would you like to commit this message? [y/n/edit]
n
Aborting...
```

2. Use gait in interactive mode, but skip OpenAI message generation:

```commandline
$ python3 gait.py commit -s
Beginning gait commit...
Please enter your commit message below:

```

3. Use gait in interactive mode, but provide a commit message manually:

```commandline
$ python3 gait.py commit -m 'My commit message' # Note that this will automatically skip OpenAI message generation
Beginning gait commit...
Please enter your commit message below:

```

4. Use gait in automatic mode:

```commandline
$ python3 gait.py commit -a
Committing...
```

5. Use gait in verbose mode:

```commandline
$ python3 gait.py commit -a -v
---full-git-diff---
ChatGPT full response:
{
    "id": "cmpl-7Yek3DUb2PgIqQpN7C2BWKPSF0KJn",
    "object": "text_completion",
    "created": 1688494119,
    "model": "text-davinci-003",
    "choices": [
        {
            "text": " Commit: Add commit command help and example usage to README.md",
            "index": 0,
            "logprobs": null,
            "finish_reason": "stop"
        }
    ],
    "usage": {
        "prompt_tokens": 437,
        "completion_tokens": 14,
        "total_tokens": 451
    }
}
Committing...
```

### Push
    
```commandline
$ python3 gait.py push --help
Usage: gait.py push [OPTIONS]

  This command is ued to push changes to the remote repository and create a
  pull request with a title and description generated using ChatGPT. The title
  and description are generated based on the commits being pushed to the
  remote. There are two modes for this command: interactive mode (default) and
  automatic mode.

Options:
  -a, --auto     Automatic commit mode.
  -v, --verbose  Verbose mode.
  --config FILE  Read configuration from FILE.
  --help         Show this message and exit.
```

#### Examples

1. Use gait in interactive mode:

```commandline
$ python3 gait.py push
Beginning gait push...
You have the following commits ready to push.  Continue? [y/n]
y
Pushing...
ChatGPT generated the following pull request title: 'Temp Title' and description: 'This is a temporary description'
Would you like to create pull request using this title and description? [y/n/edit]
n
Aborting...
```

2. Use gait in automatic mode:

```commandline
$ python3 gait.py push -a
Beginning gait push...
Pushing...
Creating pull request using GitHub CLI...
Pull request created!
Gait push complete!
```

3. Use gait in verbose mode:

```commandline
$ python3 gait.py push -a -v
Beginning gait push...
Pushing...
Creating pull request using GitHub CLI...
Pull request created!
Gait push complete!
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

### Packaging for Distribution

When you are ready to distribute a new version of gait, run the following command:

```bash
python -m build
```

This will generate a `dist` folder containing a `.tar.gz` file and a `.whl` file.  These can be uploaded to PyPI using `twine`.  To install `twine`, run:

```bash
pip3 install twine
```

Then upload the files to PyPI Test using the following command:

```bash
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

Before uploading to PyPI for production, consider signing the distribution using GPG.  To do this, run the following command:

```bash
gpg --detach-sign -a dist/src-0.0.1.tar.gz
```

This will generate a `.asc` file in the `dist` folder.  Upload this file to PyPI using the following command:

```bash
twine upload dist/*
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

```commandline
mkdocs serve
```

### Training Data

When developing in the gait project, we sometimes want to generate training data from using the gait CLI.  To do this, we can use the `--track` flag when running the `commit` command like so:

```commandline
python3 gait.py commit -t
```

## Resources

- [OpenAI Cookbook](https://github.com/openai/openai-cookbook) - a GitHub repo containing a number of userful tips for using the OpenAI API.
- [OpenAI Tokenizer](https://platform.openai.com/tokenizer) - a utility from OpenAI to tokenize a given text prompt.
- :construction: [click-man](https://github.com/click-contrib/click-man) - a library to create man pages for click applications.
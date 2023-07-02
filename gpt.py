import os
import subprocess

import openai


class OpenAIService(object):
    def __init__(self):
        self.__set_openai_api_key()

    def generate_commit_message(self) -> str:
        diff_file = open("diff.txt", "w")
        cmd = ['git --no-pager diff']
        subprocess.run(cmd, stdout=diff_file, shell=True)

        with open("diff.txt", "r") as diff:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=self.generate_prompt(str(diff.read())),
                temperature=0.5
            )

        return str(response)

    @staticmethod
    def generate_prompt(diff: str) -> str:
        return """Write a git commit message based on the following diff within the <<< >>> below.
        
<<<{}>>>""".format(diff)

    @staticmethod
    def __set_openai_api_key() -> None:
        openai.api_key = os.getenv("OPENAI_API_KEY")

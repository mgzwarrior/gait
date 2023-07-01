import os

import openai


class OpenAIService(object):
    def __init__(self):
        self.__set_openai_api_key()

    def generate_commit_message(self, diff: str) -> str:
        return str(openai.Model.list())

    def __set_openai_api_key(self) -> None:
        openai.api_key = os.getenv("OPENAI_API_KEY")

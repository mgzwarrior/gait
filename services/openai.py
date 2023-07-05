import os
import textwrap
from typing import Optional, Type

import openai
import tiktoken
from openai.api_resources.abstract.engine_api_resource import EngineAPIResource

from services.exceptions import OpenAIException
from services.git import GitService

SAMPLE_DIFF = """
diff --git a/README.md b/README.md
index 9f9c653..4dd9f3a 100644
--- a/README.md
+++ b/README.md
@@ -53,7 +53,3 @@ qodana scan --show-report
 ## Helpful Resources
 
 [OpenAI Cookbook](https://github.com/openai/openai-cookbook)
-
-## New Section
-
-Some content.
\\ No newline at end of file
"""


class OpenAIService:
    DEFAULT_MODEL = "text-davinci-003"
    COMPLETION_MODELS = ["text-davinci-003"]
    CHAT_COMPLETION_MODELS = ["gpt-3.5-turbo"]

    DEFAULT_TEMPERATURE = 0.5
    API_TOKEN_LIMIT_PER_REQUEST = 1000

    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        temperature: float = DEFAULT_TEMPERATURE
    ):
        self.model = model
        self.temperature = temperature
        self.__set_openai_completion_engine()
        self.__set_openai_api_key()

    def create_pull_request_on_remote_push(self):
        pass

    def generate_pull_request_description(self) -> str:
        pass

    def generate_commit_message(self, diff: str) -> str:
        try:
            commit_message = self.__create_completion(
                user_prompt=self.__generate_commit_message_prompt(diff)
            )
        except openai.error.OpenAIError as error:
            raise OpenAIException(error) from error

        return commit_message

    @staticmethod
    def test_connection() -> bool:
        try:
            response = openai.Model.list()
        except openai.error.OpenAIError as exc:
            raise OpenAIException(exc) from exc

        if not response:
            return False
        return True

    def __create_completion(
        self, user_prompt: str, system_prompt: Optional[str] = None
    ) -> str:
        if self.completion_engine == openai.ChatCompletion:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]

            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.API_TOKEN_LIMIT_PER_REQUEST,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )
            return str(response["choices"][0]["message"]["content"].strip())
        else:
            response = openai.Completion.create(
                model=self.model,
                prompt=user_prompt,
                temperature=self.temperature,
            )
            return str(response)

    def __generate_diff_summary(self) -> str:
        """
        Based on the approach described in GPT best practices below.

        https://platform.openai.com/docs/guides/gpt-best-practices/tactic-summarize-long-documents-piecewise-and-construct-a-full-summary-recursively
        """
        diff = GitService().diff()
        expected_token_usage_count = self.__count_tokens(diff)
        print(f"Expected token usage: {expected_token_usage_count}")

        num_batches = self.API_TOKEN_LIMIT_PER_REQUEST / expected_token_usage_count
        print(f"Number of batches to summarize: {num_batches}")

        chunks = textwrap.wrap(
            diff, self.API_TOKEN_LIMIT_PER_REQUEST, replace_whitespace=False
        )
        previous_summary = None

        for chunk in chunks:
            previous_summary = self.__generate_diff_batch_summary(
                chunk, previous_summary
            )

        final_summary = previous_summary
        return final_summary

    def __generate_diff_batch_summary(self, chunk: str, previous_summary: str) -> str:
        if previous_summary is not None:
            return self.__create_completion(
                system_prompt="You are going to be given a git diff summarization and a new git diff. "
                "Your task is to compare the two and produce a new summarization with a "
                "limit of X words.",
                user_prompt="Summarize the previous git diff summarization within the << >> and "
                "the following git diff within the <<< >>> below into X words."
                f"<<{previous_summary}>>"
                f"<<<{chunk}>>>",
            )
        else:
            return self.__create_completion(
                system_prompt="You are going to be given a git diff. "
                "Your task is to produce a summarization with a limit of X words.",
                user_prompt="Summarize the following git diff within the <<< >>> below into X words."
                f"<<<{chunk}>>>",
            )

    @staticmethod
    def __generate_commit_message_prompt(diff: str) -> str:
        return f"""Write a git commit message based on the following diff within the <<< >>> below.
        
<<<{diff}>>>"""

    def __count_tokens(self, diff: str) -> int:
        encoding = tiktoken.encoding_for_model(self.model)
        return len(encoding.encode(diff))

    def __set_openai_completion_engine(self) -> None:
        self.completion_engine: Type[EngineAPIResource] = openai.Completion

        if self.model in self.CHAT_COMPLETION_MODELS:
            self.completion_engine = openai.ChatCompletion
        elif self.model in self.COMPLETION_MODELS:
            self.completion_engine = openai.Completion

    @staticmethod
    def __set_openai_api_key() -> None:
        openai.api_key = os.getenv("OPENAI_API_KEY")

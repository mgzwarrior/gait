import os
from typing import Type

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
        self, model: str = DEFAULT_MODEL, temperature: float = DEFAULT_TEMPERATURE
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
            commit_message = self.__create_diff_completion(diff)
        except openai.error.OpenAIError as error:
            raise OpenAIException(error) from error

        return commit_message

    def __create_diff_completion(self, diff: str) -> str:
        if self.completion_engine == openai.ChatCompletion:
            messages = [
                {
                    "role": "system",
                    "content": "This is text summarization of git diffs.",
                },
                {"role": "user", "content": self.__generate_prompt(diff)},
            ]

            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=0.5,
                max_tokens=500,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )
            return str(response["choices"][0]["message"]["content"].strip())
        else:
            response = openai.Completion.create(
                model=self.model,
                prompt=self.__generate_prompt(diff),
                temperature=self.temperature,
            )
            return str(response)

    def __generate_diff_summary(self, summary_batch_size: int) -> str:
        """
        Based on the approach described in GPT best practices below.

        https://platform.openai.com/docs/guides/gpt-best-practices/tactic-summarize-long-documents-piecewise-and-construct-a-full-summary-recursively
        """
        diff = GitService().diff()

        encoding = tiktoken.encoding_for_model(self.model)
        expected_token_usage_count = len(encoding.encode(diff))
        num_batches = self.API_TOKEN_LIMIT_PER_REQUEST / expected_token_usage_count

        for _ in range(1, int(num_batches)):
            # Create batch from diff & send to below function.
            # summary = self.__generate_diff_batch_summary(batch, summary_batch_size) -> calls API for summary.
            # Feed the summary back into the next request to create next.
            pass

        return ""

    def __generate_diff_batch_summary(self, summary_batch_size: int) -> str:
        pass

    @staticmethod
    def __generate_prompt(diff: str) -> str:
        return f"""Write a git commit message based on the following diff within the <<< >>> below.
        
<<<{diff}>>>"""

    def __set_openai_completion_engine(self) -> None:
        self.completion_engine: Type[EngineAPIResource] = openai.Completion

        if self.model in self.CHAT_COMPLETION_MODELS:
            self.completion_engine = openai.ChatCompletion
        elif self.model in self.COMPLETION_MODELS:
            self.completion_engine = openai.Completion

    @staticmethod
    def __set_openai_api_key() -> None:
        openai.api_key = os.getenv("OPENAI_API_KEY")

"""ChatGPT module, contains OpenAIService class."""
import os
import subprocess

import openai

from exceptions import GitException, OpenAIException

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
    """OpenAI Service."""
    def __init__(self):
        self.__set_openai_api_key()

    def generate_commit_message(self, diff: str) -> str:
        """Generate a commit message."""
        try:
            #  To use real git diff
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=self.generate_prompt(diff),
                temperature=0.5
            )
            #  To use sample diff
            # response = openai.Completion.create(
            #     model="text-davinci-003",
            #     prompt=self.generate_prompt(SAMPLE_DIFF),
            #     temperature=0.5
            # )
        except openai.error.OpenAIError as exc:
            raise OpenAIException(exc) from exc

        return str(response)

    @staticmethod
    def generate_prompt(diff: str) -> str:
        """Generate a prompt for the OpenAI API."""
        return f"""Write a git commit message based on the following diff within the <<< >>> below.
        
<<<{diff}>>>"""

    @staticmethod
    def __set_openai_api_key() -> None:
        """Set the OpenAI API key."""
        openai.api_key = os.getenv("OPENAI_API_KEY")

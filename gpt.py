import os
import subprocess

import openai

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
\ No newline at end of file

"""


class OpenAIService(object):
    def __init__(self):
        self.__set_openai_api_key()

    def generate_commit_message(self) -> str:
        diff_file = open("diff.txt", "w")
        cmd = ['git --no-pager diff']
        subprocess.run(cmd, stdout=diff_file, shell=True)

        with open("diff.txt", "r") as diff:
            #  To use real git diff
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=self.generate_prompt(str(diff.read())),
                temperature=0.5
            )

            #  To use sample diff
            # response = openai.Completion.create(
            #     model="text-davinci-003",
            #     prompt=self.generate_prompt(SAMPLE_DIFF),
            #     temperature=0.5
            # )

        return str(response)

    @staticmethod
    def generate_prompt(diff: str) -> str:
        return """Write a git commit message based on the following diff within the <<< >>> below.
        
<<<{}>>>""".format(diff)

    @staticmethod
    def __set_openai_api_key() -> None:
        openai.api_key = os.getenv("OPENAI_API_KEY")

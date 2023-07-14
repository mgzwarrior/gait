from unittest.mock import MagicMock

import pytest

from src.services.openai import OpenAIService


class TestOpenAI:
    @pytest.mark.unit
    def test_openai_generate_commit_message(self):
        openai = MagicMock()
        openai.Completion.create.return_value = {
            "choices": [
                {
                    "text": "This is a test commit message."
                }
            ]
        }
        result = OpenAIService().generate_commit_message("This is a test diff")
        assert result == "This is a test commit message."

    @pytest.mark.unit
    def test_openai_test_connection(self):
        openai = MagicMock()
        openai.Model.list.return_value = ["some_value"]
        result = OpenAIService().test_connection()
        assert result is True

import json
from unittest.mock import MagicMock, patch

import pytest

from src.services.openai import OpenAIService


class TestOpenAI:
    @pytest.mark.unit
    @patch("src.services.openai.openai.Completion.create")
    def test_openai_generate_commit_message(self, mock_completion_create):
        mock_completion_create.return_value = json.dumps({
            "choices": [
                {
                    "text": "This is a test commit message."
                }
            ]
        })
        result = json.loads(OpenAIService().generate_commit_message("This is a test diff"))
        assert json.dumps(result["choices"][0]["text"], indent=4) == '"This is a test commit message."'

    @pytest.mark.unit
    def test_openai_test_connection(self):
        openai = MagicMock()
        openai.Model.list.return_value = ["some_value"]
        result = OpenAIService().test_connection()
        assert result is True

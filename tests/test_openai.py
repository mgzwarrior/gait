import json
from unittest.mock import MagicMock, patch

import openai
import pytest

from src.services.exceptions import OpenAIException
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
    @patch("src.services.openai.openai.Completion.create", side_effect=openai.error.OpenAIError)
    def test_openai_test_connection_throws_exception(self, mock_model_list):
        with pytest.raises(OpenAIException):
            OpenAIService().generate_commit_message("This is a test diff")

    @pytest.mark.unit
    @patch("src.services.openai.openai.Model.list")
    def test_openai_test_connection(self, mock_model_list):
        mock_model_list.return_value = ["some_value"]
        result = OpenAIService().test_connection()
        assert result is True

    @pytest.mark.unit
    @patch("src.services.openai.openai.Model.list", side_effect=openai.error.OpenAIError)
    def test_openai_test_connection_throws_exception(self, mock_model_list):
        with pytest.raises(OpenAIException):
            OpenAIService().test_connection()

"""Custom exceptions for the gait module."""


class GitException(Exception):
    """Raised when a subprocess running git fails."""

class OpenAIException(Exception):
    """Raised when an OpenAI request fails."""

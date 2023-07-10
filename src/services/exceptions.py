"""Custom exceptions for the src module."""


class GitException(Exception):
    """Raised when a subprocess running git fails."""


class GitHubException(Exception):
    """Raised when a GitHub request fails."""


class OpenAIException(Exception):
    """Raised when an OpenAI request fails."""

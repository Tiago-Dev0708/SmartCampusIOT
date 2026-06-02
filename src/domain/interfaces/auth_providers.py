"""Abstract interfaces for authentication providers."""
from abc import ABC, abstractmethod

class PasswordHasherInterface(ABC):
    """Port for hashing and verifying passwords."""

    @abstractmethod
    def hash(self, password: str) -> str:
        """Hash a plain text password."""
        ...

    @abstractmethod
    def verify(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a plain password against a hash."""
        ...

class TokenProviderInterface(ABC):
    """Port for generating authentication tokens."""

    @abstractmethod
    def create_access_token(self, subject: str) -> str:
        """Create a short-lived access token."""
        ...

    @abstractmethod
    def create_refresh_token(self, subject: str) -> str:
        """Create a long-lived refresh token."""
        ...

    @abstractmethod
    def decode_token(self, token: str) -> dict:
        """Decode and validate a token, returning its payload."""
        ...

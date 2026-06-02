"""Custom domain exceptions.

These exceptions are raised by the domain and use-case layers and
translated into appropriate HTTP responses by the presentation layer.
"""


class DomainError(Exception):
    """Base class for all domain-level errors."""


class SensorNotFoundError(DomainError):
    """Raised when a requested sensor reading does not exist."""


class ClassroomNotFoundError(DomainError):
    """Raised when a requested classroom cannot be found."""


class RoomNotFoundError(DomainError):
    """Raised when a requested room cannot be found."""


class InvalidRoomStatusError(DomainError):
    """Raised when an invalid room status value is provided."""


class AuthenticationError(DomainError):
    """Raised when authentication credentials are invalid."""


class UserNotFoundError(DomainError):
    """Raised when a user cannot be found."""

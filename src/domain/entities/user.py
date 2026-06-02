"""Domain entity for system users."""
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone

@dataclass
class UserEntity:
    """Pure domain entity representing a user."""
    name: str
    email: str
    password_hash: str
    role: str = "user"
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

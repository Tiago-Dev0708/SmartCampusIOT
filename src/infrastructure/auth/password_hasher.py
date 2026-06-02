"""Password hashing adapter using native bcrypt."""
import bcrypt
from src.domain.interfaces.auth_providers import PasswordHasherInterface

class PasswordHasher(PasswordHasherInterface):
    """Concrete implementation for password hashing using native bcrypt."""

    def hash(self, password: str) -> str:
        """Hash password using native bcrypt."""
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        """Verify plain password against hashed password."""
        password_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        try:
            return bcrypt.checkpw(password_bytes, hashed_bytes)
        except Exception:
            return False

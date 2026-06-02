"""Use case for registering a new user."""
from src.domain.entities.user import UserEntity
from src.domain.interfaces.repositories import UserRepositoryInterface
from src.domain.interfaces.auth_providers import PasswordHasherInterface

class RegisterUserUseCase:
    """Orchestrates the user registration flow."""

    def __init__(
        self,
        user_repo: UserRepositoryInterface,
        password_hasher: PasswordHasherInterface,
    ) -> None:
        self.user_repo = user_repo
        self.password_hasher = password_hasher

    async def execute(self, name: str, email: str, plain_password: str) -> UserEntity:
        """Hash password, create UserEntity and save to repository."""
        existing = await self.user_repo.get_by_email(email)
        if existing:
            raise ValueError("Email already registered")
        
        hashed = self.password_hasher.hash(plain_password)
        user = UserEntity(name=name, email=email, password_hash=hashed)
        
        await self.user_repo.save(user)
        return user

"""Use case for authenticating a user and generating JWT tokens."""
from src.domain.interfaces.repositories import UserRepositoryInterface
from src.domain.interfaces.auth_providers import PasswordHasherInterface, TokenProviderInterface

class LoginUserUseCase:
    """Orchestrates the login flow and JWT token generation."""

    def __init__(
        self,
        user_repo: UserRepositoryInterface,
        password_hasher: PasswordHasherInterface,
        token_provider: TokenProviderInterface,
    ) -> None:
        self.user_repo = user_repo
        self.password_hasher = password_hasher
        self.token_provider = token_provider

    async def execute(self, email: str, plain_password: str) -> dict:
        """Verify credentials and return access and refresh tokens."""
        user = await self.user_repo.get_by_email(email)
        
        if not user or not self.password_hasher.verify(plain_password, user.password_hash):
            raise ValueError("Invalid credentials")

        access_token = self.token_provider.create_access_token(str(user.id))
        refresh_token = self.token_provider.create_refresh_token(str(user.id))

        return {
            "user": user,
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

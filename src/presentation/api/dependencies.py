"""FastAPI dependency-injection factories.

Every route depends on use-case factories created here via ``Depends()``.
The session is yielded from a generator so it is always closed properly.
"""

from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.user import UserEntity

from src.application.use_cases.get_analytics import GetAnalyticsUseCase
from src.application.use_cases.get_dashboard import GetDashboardUseCase
from src.application.use_cases.save_sensor_data import SaveSensorDataUseCase
from src.application.use_cases.toggle_classroom_light import ToggleClassroomLightUseCase
from src.application.use_cases.toggle_room import ToggleRoomUseCase
from src.application.use_cases.register_user import RegisterUserUseCase
from src.application.use_cases.login_user import LoginUserUseCase
from src.infrastructure.database.config import get_session_factory
from src.infrastructure.repositories.classroom_repository import ClassroomRepositoryImpl
from src.infrastructure.repositories.room_repository import RoomRepositoryImpl
from src.infrastructure.repositories.sensor_repository import SensorRepositoryImpl
from src.infrastructure.repositories.user_repository import UserRepositoryImpl
from src.infrastructure.auth.password_hasher import PasswordHasher
from src.infrastructure.auth.jwt_provider import JwtProvider


# ── Session generator ──────────────────────────────────────────────


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Yield a short-lived async DB session."""
    factory = get_session_factory()
    async with factory() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


# ── Repository factories ──────────────────────────────────────────


def get_sensor_repo(session: SessionDep) -> SensorRepositoryImpl:
    return SensorRepositoryImpl(session)


def get_classroom_repo(session: SessionDep) -> ClassroomRepositoryImpl:
    return ClassroomRepositoryImpl(session)


def get_room_repo(session: SessionDep) -> RoomRepositoryImpl:
    return RoomRepositoryImpl(session)


def get_user_repo(session: SessionDep) -> UserRepositoryImpl:
    return UserRepositoryImpl(session)


SensorRepoDep = Annotated[SensorRepositoryImpl, Depends(get_sensor_repo)]
ClassroomRepoDep = Annotated[ClassroomRepositoryImpl, Depends(get_classroom_repo)]
RoomRepoDep = Annotated[RoomRepositoryImpl, Depends(get_room_repo)]
UserRepoDep = Annotated[UserRepositoryImpl, Depends(get_user_repo)]


# ── Auth Providers ────────────────────────────────────────────────

def get_password_hasher() -> PasswordHasher:
    return PasswordHasher()


def get_jwt_provider() -> JwtProvider:
    return JwtProvider()


PasswordHasherDep = Annotated[PasswordHasher, Depends(get_password_hasher)]
JwtProviderDep = Annotated[JwtProvider, Depends(get_jwt_provider)]


# ── Auth & Security ───────────────────────────────────────────────

security_scheme = HTTPBearer()

async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security_scheme)],
    jwt_provider: JwtProviderDep,
    user_repo: UserRepoDep,
) -> UserEntity:
    """Validate JWT token and return the active user."""
    token = credentials.credentials
    payload = jwt_provider.decode_token(token)
    if not payload or payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    subject = payload.get("sub")
    if not subject:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    user = await user_repo.get_by_id(subject)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User no longer exists",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

CurrentUserDep = Annotated[UserEntity, Depends(get_current_user)]


# ── Use-case factories ────────────────────────────────────────────


def get_save_sensor_use_case(repo: SensorRepoDep) -> SaveSensorDataUseCase:
    return SaveSensorDataUseCase(sensor_repo=repo)


def get_toggle_classroom_use_case(repo: ClassroomRepoDep) -> ToggleClassroomLightUseCase:
    return ToggleClassroomLightUseCase(classroom_repo=repo)


def get_toggle_room_use_case(repo: RoomRepoDep) -> ToggleRoomUseCase:
    return ToggleRoomUseCase(room_repo=repo)


def get_dashboard_use_case(repo: RoomRepoDep, sensor_repo: SensorRepoDep) -> GetDashboardUseCase:
    return GetDashboardUseCase(room_repo=repo, sensor_repo=sensor_repo)


def get_analytics_use_case(repo: RoomRepoDep) -> GetAnalyticsUseCase:
    return GetAnalyticsUseCase(room_repo=repo)


def get_register_user_use_case(
    repo: UserRepoDep, hasher: PasswordHasherDep
) -> RegisterUserUseCase:
    return RegisterUserUseCase(user_repo=repo, password_hasher=hasher)


def get_login_user_use_case(
    repo: UserRepoDep, hasher: PasswordHasherDep, provider: JwtProviderDep
) -> LoginUserUseCase:
    return LoginUserUseCase(
        user_repo=repo, password_hasher=hasher, token_provider=provider
    )


SaveSensorUseCaseDep = Annotated[SaveSensorDataUseCase, Depends(get_save_sensor_use_case)]
ToggleClassroomUseCaseDep = Annotated[ToggleClassroomLightUseCase, Depends(get_toggle_classroom_use_case)]
ToggleRoomUseCaseDep = Annotated[ToggleRoomUseCase, Depends(get_toggle_room_use_case)]
DashboardUseCaseDep = Annotated[GetDashboardUseCase, Depends(get_dashboard_use_case)]
AnalyticsUseCaseDep = Annotated[GetAnalyticsUseCase, Depends(get_analytics_use_case)]
RegisterUserUseCaseDep = Annotated[RegisterUserUseCase, Depends(get_register_user_use_case)]
LoginUserUseCaseDep = Annotated[LoginUserUseCase, Depends(get_login_user_use_case)]

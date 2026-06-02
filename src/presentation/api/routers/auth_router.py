"""Auth router — registration, login and token refresh."""

import logging

from fastapi import APIRouter, HTTPException, status
import jwt

from src.presentation.api.dependencies import (
    LoginUserUseCaseDep,
    RegisterUserUseCaseDep,
    JwtProviderDep,
)
from src.presentation.api.schemas.mobile_schemas import (
    AuthResponse,
    LoginRequest,
    RegisterRequest,
    RefreshRequest,
    TokenResponse,
    UserResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Creates a new user account with hashed password.",
)
async def register(body: RegisterRequest, use_case: RegisterUserUseCaseDep) -> UserResponse:
    """Validate data and register user."""
    try:
        user = await use_case.execute(body.name, body.email, body.password)
        logger.info("User registered: %s", user.email)
        return UserResponse(
            id=str(user.id),
            name=user.name,
            email=user.email,
            role=user.role,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

@router.post(
    "/login",
    response_model=AuthResponse,
    summary="User login",
    description="Authenticate with e-mail and password. Returns a JWT access token and refresh token.",
)
async def login(body: LoginRequest, use_case: LoginUserUseCaseDep) -> AuthResponse:
    """Validate credentials and return an auth response."""
    try:
        result = await use_case.execute(body.email, body.password)
        user = result["user"]
        
        logger.info("User logged in: %s", user.email)
        
        return AuthResponse(
            user=UserResponse(
                id=str(user.id),
                name=user.name,
                email=user.email,
                role=user.role,
            ),
            access_token=result["access_token"],
            refresh_token=result["refresh_token"],
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Refresh access token",
    description="Generates a new access token using a valid refresh token.",
)
async def refresh_token(body: RefreshRequest, jwt_provider: JwtProviderDep) -> TokenResponse:
    """Validate refresh token and issue a new access token."""
    payload = jwt_provider.decode_token(body.refresh_token)
    
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )
        
    subject = payload.get("sub")
    if not subject:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )
        
    access_token = jwt_provider.create_access_token(subject)
    
    return TokenResponse(access_token=access_token)

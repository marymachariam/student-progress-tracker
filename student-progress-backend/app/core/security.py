from datetime import datetime, timedelta, timezone
from typing import Optional, Any

from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import HTTPException, status
import secrets

from app.core.config import get_settings

settings = get_settings()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a plain password."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)

def generate_otp(length: int = 6) -> str:
    """Cryptographically secure numeric OTP — never use random.randint for this."""
    return "".join(secrets.choice("0123456789") for _ in range(length))
# JWT helpers
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.
    `data` should contain at least {"sub": student_id}
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def decode_access_token(token: str) -> dict[str, Any]:
    """
    Decode and validate a JWT token.
    Raises HTTPException if invalid or expired.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        student_id: str | None = payload.get("sub")
        if student_id is None:
            raise credentials_exception
        return payload
    except JWTError:
        raise credentials_exception

def create_password_reset_token(student_id: int) -> str:
    return create_access_token(
        data={"sub": str(student_id), "purpose": "password_reset"},
        expires_delta=timedelta(minutes=15),
    )

def generate_reset_token() -> str:
    return secrets.token_urlsafe(32)
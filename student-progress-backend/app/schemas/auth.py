import re
from pydantic import BaseModel, EmailStr, Field, field_validator


def _validate_strength(v: str) -> str:
    if not re.search(r"[A-Z]", v):
        raise ValueError("Password must contain an uppercase letter")
    if not re.search(r"[a-z]", v):
        raise ValueError("Password must contain a lowercase letter")
    if not re.search(r"\d", v):
        raise ValueError("Password must contain a digit")
    return v


class RegisterRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)

    @field_validator("password")
    @classmethod
    def check_password(cls, v: str) -> str:
        return _validate_strength(v)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class OTPVerifyRequest(BaseModel):
    email: EmailStr
    code: str = Field(..., pattern=r"^\d{6}$")


class ResendOTPRequest(BaseModel):
    email: EmailStr
    purpose: str = Field(..., pattern=r"^email_verification$")


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8, max_length=100)

    @field_validator("new_password")
    @classmethod
    def check_password(cls, v: str) -> str:
        return _validate_strength(v)


class MessageResponse(BaseModel):
    message: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    student_id: int
    name: str
    email: str
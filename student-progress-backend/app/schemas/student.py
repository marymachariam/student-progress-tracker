from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from pydantic import model_validator


class StudentBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr


class StudentCreate(StudentBase):
    password: str = Field(..., min_length=6, max_length=100)


class StudentLogin(BaseModel):
    email: EmailStr
    password: str


class StudentUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=100)
    email: EmailStr | None = None
    password: str | None = Field(None, min_length=6, max_length=100)

class StudentResponse(StudentBase):
    student_id: int
    created_at: datetime
    profile_picture_url: str | None = None
    is_active: bool
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    student_id: int | None = None


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=6, max_length=100)
    confirm_password: str

    @model_validator(mode="after")
    def passwords_match(self):
        if self.new_password != self.confirm_password:
            raise ValueError("New password and confirmation do not match")
        return self
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from database import get_db
from app.core.security import decode_access_token
from app.models.student import Student

bearer_scheme = HTTPBearer()


def get_current_student(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> Student:
    token = credentials.credentials
    payload = decode_access_token(token)
    student_id = payload.get("sub")

    if student_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    student = db.get(Student, int(student_id))
    if student is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Student not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return student


CurrentStudent = Annotated[Student, Depends(get_current_student)]
DBSession = Annotated[Session, Depends(get_db)]
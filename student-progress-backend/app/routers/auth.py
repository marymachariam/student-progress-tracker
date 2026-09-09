from fastapi import APIRouter, HTTPException, Request, status, BackgroundTasks

from app.core.deps import DBSession
from app.core.limiter import limiter
from app.core.config import get_settings
from app.core.security import (
    hash_password, verify_password, create_access_token, generate_otp,
    generate_reset_token,
)
from app.core.redis import (
    set_otp, verify_otp, delete_otp,
    is_login_locked, record_failed_login, clear_login_attempts,
    set_reset_token, get_reset_token_student_id, delete_reset_token,
)
from app.core.mail import send_otp_email, send_password_reset_email
from app.models.student import Student
from app.schemas.auth import (
    RegisterRequest, LoginRequest, OTPVerifyRequest, ResendOTPRequest,
    ForgotPasswordRequest, ResetPasswordRequest, MessageResponse, TokenResponse,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])
settings = get_settings()


def _otp_key(purpose: str, email: str) -> str:
    return f"otp:{purpose}:{email.lower()}"


@router.post("/register", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("3/minute")
def register(request: Request, data: RegisterRequest, db: DBSession, background_tasks: BackgroundTasks):
    existing = db.query(Student).filter(Student.email == data.email.lower()).first()
    if existing:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Unable to register with this email")

    student = Student(
        name=data.name,
        email=data.email.lower(),
        hashed_password=hash_password(data.password),
        is_verified=False,
    )
    db.add(student)
    db.commit()
    db.refresh(student)

    code = generate_otp()
    set_otp(_otp_key("email_verification", data.email), code)
    background_tasks.add_task(send_otp_email, data.email, code, "verify your email")

    return {"message": "Registration successful. Please check your email for the OTP."}


@router.post("/verify-otp", response_model=MessageResponse)
@limiter.limit("10/minute")
def verify_otp_route(request: Request, data: OTPVerifyRequest, db: DBSession):
    key = _otp_key("email_verification", data.email)
    if not verify_otp(key, data.code):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid or expired OTP")

    student = db.query(Student).filter(Student.email == data.email.lower()).first()
    if not student:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid email or OTP")

    student.is_verified = True
    db.commit()
    delete_otp(key)

    return {"message": "Email verified successfully. You can now log in."}


@router.post("/resend-otp", response_model=MessageResponse)
@limiter.limit("3/minute")
def resend_otp(request: Request, data: ResendOTPRequest, db: DBSession, background_tasks: BackgroundTasks):
    student = db.query(Student).filter(Student.email == data.email.lower()).first()
    if not student:
        return {"message": "If the email exists, a new OTP has been sent."}

    code = generate_otp()
    set_otp(_otp_key(data.purpose, data.email), code)
    background_tasks.add_task(send_otp_email, data.email, code, "verify your email")

    return {"message": "If the email exists, a new OTP has been sent."}


@router.post("/login", response_model=TokenResponse)
@limiter.limit("5/minute")
def login(request: Request, data: LoginRequest, db: DBSession):
    email = data.email.lower()

    if is_login_locked(email):
        raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS, "Too many failed attempts. Try again later.")

    student = db.query(Student).filter(Student.email == email).first()

    if not student or not verify_password(data.password, student.hashed_password):
        record_failed_login(email)
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Incorrect email or password")

    if not student.is_verified:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Please verify your email before logging in")

    if not student.is_active:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "This account has been deactivated")

    clear_login_attempts(email)
    access_token = create_access_token(data={"sub": str(student.student_id)})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "student_id": student.student_id,
        "name": student.name,
        "email": student.email,
    }


@router.post("/forgot-password", response_model=MessageResponse)
@limiter.limit("3/minute")
def forgot_password(request: Request, data: ForgotPasswordRequest, db: DBSession, background_tasks: BackgroundTasks):
    student = db.query(Student).filter(Student.email == data.email.lower()).first()

    if student:
        token = generate_reset_token()
        set_reset_token(token, student.student_id)
        reset_link = f"{settings.FRONTEND_URL}/reset-password?token={token}"
        background_tasks.add_task(send_password_reset_email, student.email, reset_link)

    return {"message": "If the email exists, a password reset link has been sent."}


@router.post("/reset-password", response_model=MessageResponse)
@limiter.limit("5/minute")
def reset_password(request: Request, data: ResetPasswordRequest, db: DBSession):
    student_id = get_reset_token_student_id(data.token)
    if student_id is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid or expired reset link")

    student = db.get(Student, student_id)
    if not student:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid reset link")

    student.hashed_password = hash_password(data.new_password)
    db.commit()
    delete_reset_token(data.token)

    return {"message": "Password has been reset successfully. You can now log in."}
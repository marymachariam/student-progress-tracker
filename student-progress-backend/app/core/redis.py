import hashlib
import time

_store: dict[str, tuple[str, float]] = {}       
_attempts: dict[str, tuple[int, float]] = {}     

MAX_OTP_ATTEMPTS = 5
OTP_LOCKOUT_SECONDS = 900
LOGIN_MAX_ATTEMPTS = 5
LOGIN_LOCKOUT_SECONDS = 900


def _hash_code(code: str) -> str:
    return hashlib.sha256(code.encode()).hexdigest()


def _get(key: str) -> str | None:
    entry = _store.get(key)
    if not entry:
        return None
    value, expire_at = entry
    if time.time() > expire_at:
        _store.pop(key, None)
        return None
    return value


def set_otp(key: str, code: str, expire_seconds: int | None = None) -> None:
    from app.core.config import get_settings
    expire = expire_seconds or get_settings().OTP_EXPIRE_SECONDS
    _store[key] = (_hash_code(code), time.time() + expire)
    _attempts.pop(f"{key}:attempts", None)


def verify_otp(key: str, code: str) -> bool:
    attempts_key = f"{key}:attempts"
    count, expire_at = _attempts.get(attempts_key, (0, 0))
    if time.time() > expire_at:
        count = 0
    count += 1
    _attempts[attempts_key] = (count, time.time() + OTP_LOCKOUT_SECONDS)

    if count > MAX_OTP_ATTEMPTS:
        return False

    stored_hash = _get(key)
    if not stored_hash:
        return False
    return stored_hash == _hash_code(code)


def delete_otp(key: str) -> None:
    _store.pop(key, None)
    _attempts.pop(f"{key}:attempts", None)


def is_login_locked(email: str) -> bool:
    key = f"login_attempts:{email.lower()}"
    count, expire_at = _attempts.get(key, (0, 0))
    if time.time() > expire_at:
        return False
    return count >= LOGIN_MAX_ATTEMPTS


def record_failed_login(email: str) -> None:
    key = f"login_attempts:{email.lower()}"
    count, expire_at = _attempts.get(key, (0, 0))
    if time.time() > expire_at:
        count = 0
    _attempts[key] = (count + 1, time.time() + LOGIN_LOCKOUT_SECONDS)


def clear_login_attempts(email: str) -> None:
    _attempts.pop(f"login_attempts:{email.lower()}", None)
    

def set_reset_token(token: str, student_id: int, expire_seconds: int = 900) -> None:
    _store[f"reset_token:{_hash_code(token)}"] = (str(student_id), time.time() + expire_seconds)


def get_reset_token_student_id(token: str) -> int | None:
    value = _get(f"reset_token:{_hash_code(token)}")
    return int(value) if value else None


def delete_reset_token(token: str) -> None:
    _store.pop(f"reset_token:{_hash_code(token)}", None)
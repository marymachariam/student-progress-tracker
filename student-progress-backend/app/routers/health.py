from fastapi import APIRouter
from sqlalchemy import text

from app.core.deps import DBSession
from app.core.config import get_settings

router = APIRouter(tags=["health"])
settings = get_settings()


@router.get("/health")
def health_check(db: DBSession):
    db_status = "ok"
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        db_status = "unreachable"

    return {
        "status": "ok" if db_status == "ok" else "degraded",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "database": db_status,
    }
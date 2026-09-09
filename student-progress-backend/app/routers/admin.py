from fastapi import APIRouter
from app.core.deps import DBSession

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/trigger-digest")
async def trigger_digest_manually(db: DBSession):
    from app.services.digest import send_weekly_digests
    count = await send_weekly_digests(db)
    return {"sent": count}
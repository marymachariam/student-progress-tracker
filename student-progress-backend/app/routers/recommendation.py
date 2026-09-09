from fastapi import APIRouter

from app.core.deps import DBSession, CurrentStudent
from app.schemas.recommendation import RecommendationResponse
from app.services.recommendation import get_recommendation

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.get("", response_model=RecommendationResponse)
async def recommendation(db: DBSession, current_student: CurrentStudent):
    return await get_recommendation(db, current_student.student_id)
from pydantic import BaseModel


class RecommendationResponse(BaseModel):
    recommendation: str
    source: str 
    based_on: dict
    cached_at: float | None = None
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.core.config import get_settings
from app.core.logging_config import setup_logging
from database import Base, engine
from app.core.limiter import limiter
from app.routers import (
    auth, student, subject, topic, study_session,
    quiz_score, goal, analytics, health, recommendation,
)
from app.core.scheduler import start_scheduler, stop_scheduler
import app.models

from app.routers import (
    auth, student, subject, topic, study_session,
    quiz_score, goal, analytics, health,
)

settings = get_settings()

setup_logging(debug=settings.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION, debug=settings.DEBUG)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(student.router)
app.include_router(subject.router)
app.include_router(topic.router)
app.include_router(study_session.router)
app.include_router(quiz_score.router)
app.include_router(goal.router)
app.include_router(analytics.router)
app.include_router(health.router)
app.include_router(recommendation.router)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    logger.info("Application startup complete.")
    start_scheduler()
@app.on_event("shutdown")
def on_shutdown():
    stop_scheduler()
    
@app.get("/")
def home():
    return {"message": f"Welcome to {settings.APP_NAME}"}
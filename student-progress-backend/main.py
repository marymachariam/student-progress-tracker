import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.core.config import get_settings
from app.core.logging_config import setup_logging
from app.core.limiter import limiter
from app.core.scheduler import start_scheduler, stop_scheduler
from app.routers import (
    auth,
    student,
    subject,
    topic,
    study_session,
    quiz_score,
    goal,
    analytics,
    health,
    recommendation,
    admin,
)
import app.models  

settings = get_settings()

setup_logging(debug=settings.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://student-progress-tracker-umber.vercel.app",
        "https://student-progress-tracker-git-main-marymacharia.vercel.app",
        "https://student-progress-tracker-46fjr6w7p-marymacharia.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
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
app.include_router(admin.router)




@app.get("/")
def home():
    return {"message": f"Welcome to {settings.APP_NAME}"}
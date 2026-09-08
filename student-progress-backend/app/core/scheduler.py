import asyncio
import logging

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from database import SessionLocal
from app.services.digest import send_weekly_digests

logger = logging.getLogger(__name__)
scheduler = BackgroundScheduler()


def run_weekly_digest_job():
    """Wraps the async digest sender for APScheduler's sync BackgroundScheduler."""
    db = SessionLocal()
    try:
        count = asyncio.run(send_weekly_digests(db))
        logger.info("Weekly digest sent to %d students", count)
    except Exception as exc:
        logger.error("Weekly digest job failed: %s", exc)
    finally:
        db.close()


def start_scheduler():
    scheduler.add_job(run_weekly_digest_job, CronTrigger(day_of_week="sun", hour=18, minute=0))
    scheduler.start()
    logger.info("Scheduler started — weekly digest set for Sundays 18:00")


def stop_scheduler():
    scheduler.shutdown()
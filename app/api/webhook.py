from fastapi import FastAPI, Request, BackgroundTasks
from app.automation import run_scheduler
import logging
import traceback

logging.basicConfig(level=logging.INFO)

app = FastAPI()
logger = logging.getLogger(__name__)


def run_scheduler_safe():
    try:
        logger.info("===== Scheduler Started =====")
        run_scheduler()
        logger.info("===== Scheduler Finished =====")
    except Exception:
        logger.exception("Scheduler failed")
        traceback.print_exc()


@app.post("/webhook")
async def webhook(request: Request, background_tasks: BackgroundTasks):
    payload = await request.json()

    logger.info("Webhook received")
    logger.info(payload)

    background_tasks.add_task(run_scheduler_safe)

    return {
        "success": True,
        "message": "Scheduler started"
    }
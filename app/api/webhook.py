from fastapi import FastAPI, Request, BackgroundTasks
from app.automation import run_scheduler
import logging
app = FastAPI()
logger = logging.getLogger(__name__)

@app.post("/webhook")
async def webhook(request: Request, background_tasks: BackgroundTasks):
    payload = await request.json()

    logger.info(payload)

    try:
        background_tasks.add_task(run_scheduler)
    except Exception as e:
        print(f"Scheduler run failed: {e}")
        return {"success": False, "error": str(e)}

    return {"success": True}
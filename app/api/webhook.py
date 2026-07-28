from fastapi import FastAPI, Request, BackgroundTasks, HTTPException

from app.automation import run_scheduler
from app.config import WEBHOOK_SECRET

app = FastAPI()


def _run_scheduler_safely():
    """Runs in the background so the webhook response isn't held up by
    the Todoist/Groq calls inside run_scheduler()."""
    try:
        run_scheduler()
    except Exception as e:
        print(f"Scheduler run failed: {e}")

@app.get("/")
async def root():
    return {
        "service": "AI Task Scheduler",
        "status": "running"
    }

@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/webhook")
async def webhook(request: Request, background_tasks: BackgroundTasks):
    if WEBHOOK_SECRET:
        provided = request.headers.get("x-webhook-secret")
        if provided != WEBHOOK_SECRET:
            raise HTTPException(status_code=401, detail="Invalid webhook secret")

    try:
        payload = await request.json()
    except Exception:
        payload = None
    print(payload)

    # Hand off the actual scheduling work to a background task so we can
    # respond immediately. run_scheduler() does several sequential blocking
    # HTTP calls (Todoist fetch, Groq call, per-task Todoist updates) — if
    # we await it inline here, callers with a webhook timeout (most
    # automation platforms time out in 10-30s) will see failures/timeouts
    # even when the job eventually succeeds.
    background_tasks.add_task(_run_scheduler_safely)

    return {"success": True, "status": "scheduling started"}

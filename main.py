from app.managers.test import tester
from app.automation import run_scheduler
import uvicorn

if __name__ == "__main__":
    # tester()
    run_scheduler()
    # uvicorn.run(
    #     "app.api.webhook:app",
    #     host="0.0.0.0",
    #     port=8000
    # )

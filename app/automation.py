import traceback

from app.managers.task_manager import TaskManager
from app.ai.ai_planner import AIPlanner
from app.scheduler.todoist_scheduler import TodoistScheduler
from app.ai.ai_provider import GroqProvider


def run_scheduler():
    try:
        print("===== Scheduler Started =====")

        print("Creating TaskManager...")
        manager = TaskManager()
        print(f"Schedulable Tasks: {len(manager.schedulable_tasks)}")
        print(f"Locked Tasks: {len(manager.appointment_tasks)}")

        print("Creating AI Planner...")
        planner = AIPlanner(llm=GroqProvider())

        print("Calling AI...")
        ai_response = planner.schedule_task(
            tasks=manager.schedulable_tasks,
            locked_tasks=manager.appointment_tasks,
            work_start="23:00",
            work_end="16:00",
        )

        print("AI Response:")
        print(ai_response)

        print("Creating Todoist Scheduler...")
        scheduler = TodoistScheduler()

        print("Updating Todoist...")
        result = scheduler.apply_schedule(ai_response)

        print("Todoist Result:")
        print(result)

        print("===== Scheduler Finished =====")

    except Exception:
        traceback.print_exc()
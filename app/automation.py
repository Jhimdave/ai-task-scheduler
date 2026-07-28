from app.managers.task_manager import TaskManager
from app.ai.ai_planner import AIPlanner
from app.scheduler.todoist_scheduler import TodoistScheduler
from app.ai.ai_provider import GroqProvider
import traceback

def run_scheduler():
    try:
        print("===== Scheduler Started =====")

        manager = TaskManager()
        print("TaskManager created")

        planner = AIPlanner(llm=GroqProvider())
        print("Planner created")

        ai_response = planner.schedule_task(
            tasks=manager.schedulable_tasks,
            locked_tasks=manager.appointment_tasks,
            work_start="23:00",
            work_end="16:00",
        )
        # print("AI Response:")
        # print(ai_response)
        print("AI Finished")

        scheduler = TodoistScheduler()
        print("Todoist Scheduler created")

        scheduler.apply_schedule(ai_response)
        print("Todoist Updated")

        print("===== Scheduler Finished =====")

    except Exception:
        traceback.print_exc()
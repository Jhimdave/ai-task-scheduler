from app.managers.task_manager import TaskManager
from app.ai.ai_planner import AIPlanner
from app.scheduler.todoist_scheduler import TodoistScheduler
from app.ai.ai_provider import GroqProvider

def run_scheduler():

    manager = TaskManager()

    planner = AIPlanner(llm=GroqProvider())

    ai_response = planner.schedule_task(
        tasks = manager.schedulable_tasks,
        locked_tasks = manager.appointment_tasks,
        work_start = "23:00",
        work_end = "16:00",
    )

    scheduler = TodoistScheduler()
    scheduler.apply_schedule(ai_response)
import json

from app.ai.ai_planner import AIPlanner
from app.ai.ai_provider import GroqProvider
from app.managers.task_manager import TaskManager
from app.scheduler.todoist_scheduler import TodoistScheduler


def tester():

    manager = TaskManager()

    print("=" * 80)
    print("TODAY TASKS")
    print("=" * 80)

    for task in manager.today_tasks:
        print(
            f"- {task['content']} "
            f"| Due: {task['due']['date'] if task.get('due') else 'None'} "
            f"| Priority: {task['priority']}"
        )

    print()

    print("=" * 80)
    print("LOCKED TASKS")
    print("=" * 80)

    for task in manager.appointment_tasks:
        print(
            f"- {task['content']} "
            f"| {task['due']['date']}"
        )

    print()

    print("=" * 80)
    print("TASKS TO SCHEDULE")
    print("=" * 80)

    for task in manager.schedulable_tasks:
        print(
            f"- {task['content']}"
        )

    print()

    if not manager.schedulable_tasks:
        print("No schedulable tasks today. Exiting.")
        return

    # -------------------------------------------------------
    # AI INPUT
    # -------------------------------------------------------

    planner = AIPlanner(
        llm=GroqProvider()
    )

    ai_payload = planner.create_input(
        tasks=manager.schedulable_tasks,
        locked_tasks=manager.appointment_tasks,
        work_start="23:00",
        work_end="16:00"
    )

    print("=" * 80)
    print("AI INPUT")
    print("=" * 80)

    print(json.dumps(ai_payload, indent=4))

    # -------------------------------------------------------
    # SEND TO AI
    # -------------------------------------------------------

    try:
        ai_response = planner.schedule_task(
            tasks=manager.schedulable_tasks,
            locked_tasks=manager.appointment_tasks,
            work_start="23:00",
            work_end="16:00"
        )
    except json.JSONDecodeError as e:
        print(f"AI returned invalid JSON: {e}")
        return
    except Exception as e:
        print(f"AI request failed: {e}")
        return

    print()

    print("=" * 80)
    print("AI RESPONSE")
    print("=" * 80)

    print(json.dumps(ai_response, indent=4))

    # -------------------------------------------------------
    # UPDATE TODOIST
    # -------------------------------------------------------

    print()

    print("=" * 80)
    print("UPDATING TODOIST")
    print("=" * 80)

    scheduler = TodoistScheduler()

    try:
        updated_tasks = scheduler.apply_schedule(ai_response)
    except Exception as e:
        print(f"Failed to update Todoist: {e}")
        return

    for item in updated_tasks:
        print(
            f"- Task {item['task_id']} -> {item['due_datetime']}"
        )

    print()

    print("=" * 80)
    print("AUTOMATION COMPLETE")
    print("=" * 80)
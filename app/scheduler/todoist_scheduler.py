from app.services.todoist_service import TodoistService

class TodoistScheduler:
    def __init__(self):
        self.todoist = TodoistService()

    def apply_schedule(self, ai_schedule):
        updated_tasks = []

        for item in ai_schedule["schedule"]:
            result = self.todoist.update_due_datetime(
                task_id=item["task_id"],
                due_datetime=item["due_datetime"]
            )

            updated_tasks.append({
                "task_id": item["task_id"],
                "due_datetime": item["due_datetime"],
                "result": result
            })

        return updated_tasks

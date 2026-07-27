import json
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from app.ai.prompts import SYSTEM_PROMPT

class AIPlanner:
    def __init__(self, llm):
        self.llm = llm

    def create_input(self, tasks, locked_tasks, work_start, work_end):
        current_time = datetime.now().astimezone() + timedelta(minutes=30)

        remainder_time = current_time.minute % 10
        if remainder_time != 0:
            current_time += timedelta(minutes=(10 - remainder_time))

        current_time = current_time.replace(second=0, microsecond=0)

        return {
            "current_time": current_time.strftime("%Y-%m-%dT%H:%M:%S"),
            "work_hours": {
                "start": work_start,
                "end": work_end
            },
            "locked_tasks": [
                {
                    "title": task['content'],
                    "due_datetime": task['due']["date"],
                }
                for task in locked_tasks
                if task.get('due') and task['due'].get("date")
            ],
            "tasks": [
                {
                    "id": task["id"],
                    "title": task["content"],
                    "priority": task["priority"]
                }
                for task in tasks
            ]
        }

    def schedule_task(self, tasks, locked_tasks, work_start, work_end):
        payload = self.create_input(tasks, locked_tasks, work_start, work_end)
        print("Input payload: ", payload)
        prompt = f"""
{SYSTEM_PROMPT}
INPUT; {json.dumps(payload)}"""

        response = self.llm.generate(prompt)
        return json.loads(response)
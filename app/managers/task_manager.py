from datetime import date
from zoneinfo import ZoneInfo
from datetime import datetime

from app.services.todoist_service import TodoistService
from app.constants import (
    LOCKED_PROJECTS,
    WORK_PROJECT_ID
)

class TaskManager:
    def __init__(self):
        self.todoist = TodoistService()
        self.tasks = self.todoist.get_tasks()

    @property
    def today_tasks(self):

        today = self._today_manila()

        return[
            task for task in self.tasks
            if task.get('due') and task['due']['date'].startswith(today)
        ]

    @property
    def appointment_tasks(self):

        return [
            task for task in self.today_tasks
            if task['project_id'] in LOCKED_PROJECTS
        ]

    @property
    def work_tasks(self):

        return [
            task for task in self.today_tasks
            if task['project_id'] == WORK_PROJECT_ID
        ]

    @property
    def schedulable_tasks(self):

        return [
            task for task in self.today_tasks
            if not task['checked'] and task['project_id'] not in LOCKED_PROJECTS and not task['due'].get('is_recurring')
        ]

    @property
    def overdue_tasks(self):

        today = self._today_manila()

        return [
            task for task in self.tasks
            if task.get('due') and task['due']['date'][:10] < today
        ]

    def _today_manila(self) -> str:
        return datetime.now(ZoneInfo("Asia/Manila")).date().isoformat()

    def by_project(self, project_id : str):

        return [
            task for task in self.today_tasks
            if task['project_id'] == project_id
        ]

    def by_priority(self, priority : str):

        return [
            task for task in self.tasks
            if task['priority'] == priority
        ]

    def recurring_tasks(self):

        return [
            task for task in self.tasks
            if task.get('due') and task['due'].get('is_recurring')
        ]

    def group_by_project(self):

        grouped = {}

        for task in self.tasks:
            grouped.setdefault(task['project_id'], []).append(task)

        return grouped

    def refresh_tasks(self):
        self.tasks = self.todoist.get_tasks()
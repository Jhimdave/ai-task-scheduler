import requests
from app.config import TODOIST_API_KEY

class TodoistService:
    BASE_URL = "https://api.todoist.com/api/v1"

    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {TODOIST_API_KEY}"
        }

    def get_projects(self):
        url = f"{self.BASE_URL}/projects"

        response = requests.get(url, headers=self.headers, timeout=30)
        response.raise_for_status()

        return response.json()['results']

    def get_tasks(self):
        url = f"{self.BASE_URL}/tasks"

        response = requests.get(url, headers=self.headers, timeout=30)
        response.raise_for_status()

        data = response.json()

        # print("Status:", response.status_code)
        # print("Response Keys:", data.keys())
        print("Task Count:", len(data.get("results", [])))
        # print("First Task:", data.get("results", [])[:1])

        return data["results"]

    def update_task(self, task_id : str, payload: dict):
        url = f"{self.BASE_URL}/tasks/{task_id}"

        response = requests.post(url, json=payload, headers=self.headers, timeout=30)
        response.raise_for_status()
        # print(response.status_code)
        # print(response.text)
        return response.json()

    def update_due_datetime(self, task_id: str, due_datetime: str):
        payload = {
            "due_string": due_datetime
        }

        return self.update_task(task_id, payload)

    def delete_task(self, task_id : str):
        url = f"{self.BASE_URL}/tasks/{task_id}"

        response = requests.delete(url, headers=self.headers, timeout=30)
        response.raise_for_status()
        return response.json()

    def get_task(self, task_id : str):
        url = f"{self.BASE_URL}/tasks/{task_id}"

        response = requests.get(url, headers=self.headers, timeout=30)
        response.raise_for_status()
        return response.json()

    def create_task(self, payload: dict):
        url = f"{self.BASE_URL}/tasks"

        response = requests.post(url, json=payload, headers=self.headers, timeout=30)
        response.raise_for_status()
        return response.json()
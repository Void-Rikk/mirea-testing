from models import Task, TaskStatus
from storage import TaskStorage
from typing import Optional


class TaskManager:
    def __init__(self, storage: TaskStorage):
        self.storage = storage
        self.tasks = storage.load_tasks()

    def _save(self) -> None:
        self.storage.save_tasks(self.tasks)

    def _get_next_id(self) -> int:
        if not self.tasks:
            return 1

        return max(task.id for task in self.tasks) + 1

    def add_task(
        self,
        title: str,
        description: str = ""
    ) -> Task:
        title = title.strip()

        if not title:
            raise ValueError("Task title cannot be empty")

        task = Task(
            id=self._get_next_id(),
            title=title,
            description=description.strip()
        )

        self.tasks.append(task)
        self._save()

        return task

    def get_tasks(self) -> list[Task]:
        return list(self.tasks)

    def get_task(self, task_id: int) -> Task:
        for task in self.tasks:
            if task.id == task_id:
                return task

        raise ValueError(f"Task with ID {task_id} not found")

    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> Task:
        task = self.get_task(task_id)

        if title is not None:
            title = title.strip()

            if not title:
                raise ValueError("Task title cannot be empty")

            task.title = title

        if description is not None:
            task.description = description.strip()

        self._save()
        return task

    def update_status(
        self,
        task_id: int,
        status: TaskStatus
    ) -> Task:
        task = self.get_task(task_id)

        if not isinstance(status, TaskStatus):
            raise ValueError("Invalid task status")

        task.status = status
        self._save()

        return task

    def delete_task(self, task_id: int) -> None:
        task = self.get_task(task_id)

        self.tasks.remove(task)
        self._save()

    def search_tasks(self, query: str) -> list[Task]:
        query = query.strip().lower()

        if not query:
            return []

        return [
            task for task in self.tasks
            if query in task.title.lower()
            or query in task.description.lower()
        ]

    def filter_by_status(
        self,
        status: TaskStatus
    ) -> list[Task]:
        return [
            task for task in self.tasks
            if task.status == status
        ]

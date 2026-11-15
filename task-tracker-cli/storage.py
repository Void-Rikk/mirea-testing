import json
from pathlib import Path

from models import Task


class TaskStorage:
    def __init__(self, file_path: str = "data/tasks.json"):
        self.file_path = Path(file_path)

    def load_tasks(self) -> list[Task]:
        if not self.file_path.exists():
            return []

        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, list):
                raise ValueError("Invalid tasks data format")

            return [Task.from_dict(item) for item in data]

        except json.JSONDecodeError as error:
            raise ValueError("Tasks file contains invalid JSON") from error

    def save_tasks(self, tasks: list[Task]) -> None:
        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        data = [task.to_dict() for task in tasks]

        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=4
            )

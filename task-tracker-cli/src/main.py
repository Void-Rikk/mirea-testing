from models import TaskStatus
from storage import TaskStorage
from task_manager import TaskManager


def print_menu() -> None:
    print("\n========== TASK MANAGER ==========")
    print("1. Show all tasks")
    print("2. Add task")
    print("3. Show task")
    print("4. Update task")
    print("5. Change task status")
    print("6. Delete task")
    print("7. Search tasks")
    print("8. Filter tasks by status")
    print("0. Exit")
    print("==================================")


def print_task(task) -> None:
    print(f"\nID:          {task.id}")
    print(f"Title:       {task.title}")
    print(f"Description: {task.description}")
    print(f"Status:      {task.status.value}")
    print(f"Created at:  {task.created_at}")


def show_tasks(manager: TaskManager) -> None:
    tasks = manager.get_tasks()

    if not tasks:
        print("\nNo tasks found.")
        return

    for task in tasks:
        print_task(task)
        print("-" * 35)


def add_task(manager: TaskManager) -> None:
    title = input("Enter task title: ")
    description = input("Enter task description: ")

    task = manager.add_task(title, description)

    print(f"\nTask #{task.id} successfully added!")


def show_task(manager: TaskManager) -> None:
    task_id = int(input("Enter task ID: "))
    task = manager.get_task(task_id)

    print_task(task)


def update_task(manager: TaskManager) -> None:
    task_id = int(input("Enter task ID: "))

    title = input("Enter new title (leave empty to skip): ")
    description = input(
        "Enter new description (leave empty to skip): "
    )

    manager.update_task(
        task_id,
        title=title if title else None,
        description=description if description else None
    )

    print("\nTask successfully updated!")


def change_status(manager: TaskManager) -> None:
    task_id = int(input("Enter task ID: "))

    print("\nAvailable statuses:")
    for status in TaskStatus:
        print(f"- {status.value}")

    status_value = input("Enter new status: ").strip()

    status = TaskStatus(status_value)

    manager.update_status(task_id, status)

    print("\nTask status successfully updated!")


def delete_task(manager: TaskManager) -> None:
    task_id = int(input("Enter task ID: "))

    manager.delete_task(task_id)

    print("\nTask successfully deleted!")


def search_tasks(manager: TaskManager) -> None:
    query = input("Enter search query: ")

    tasks = manager.search_tasks(query)

    if not tasks:
        print("\nNo matching tasks found.")
        return

    for task in tasks:
        print_task(task)


def filter_tasks(manager: TaskManager) -> None:
    print("\nAvailable statuses:")
    for status in TaskStatus:
        print(f"- {status.value}")

    status_value = input("Enter status: ").strip()
    status = TaskStatus(status_value)

    tasks = manager.filter_by_status(status)

    if not tasks:
        print("\nNo tasks with this status.")
        return

    for task in tasks:
        print_task(task)


def main() -> None:
    storage = TaskStorage()
    manager = TaskManager(storage)

    actions = {
        "1": lambda: show_tasks(manager),
        "2": lambda: add_task(manager),
        "3": lambda: show_task(manager),
        "4": lambda: update_task(manager),
        "5": lambda: change_status(manager),
        "6": lambda: delete_task(manager),
        "7": lambda: search_tasks(manager),
        "8": lambda: filter_tasks(manager)
    }

    print("Welcome to Task Manager!")

    while True:
        print_menu()
        choice = input("Choose an option: ").strip()

        if choice == "0":
            print("Goodbye!")
            break

        action = actions.get(choice)

        if action is None:
            print("\nInvalid menu option.")
            continue

        try:
            action()
        except ValueError as error:
            print(f"\nError: {error}")
        except OSError as error:
            print(f"\nStorage error: {error}")


if __name__ == "__main__":
    main()

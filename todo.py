import os
import json
import time
from datetime import datetime
from colorama import Fore, init

init(autoreset=True)

TASK_FILE = "tasks.json"
COMPLETED_FILE = "completed.json"

def ensure_files():
    if not os.path.exists(TASK_FILE):
        with open(TASK_FILE, "w") as f:
            json.dump([], f)

    if not os.path.exists(COMPLETED_FILE):
        with open(COMPLETED_FILE, "w") as f:
            json.dump([], f)


def load_tasks():
    with open(TASK_FILE, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            print(Fore.RED + "Error: tasks.json is corrupted. Resetting file.")
            save_tasks([])
            return []


def save_tasks(tasks):
    with open(TASK_FILE, "w") as file:
        json.dump(tasks, file, indent=4)


def load_completed():
    with open(COMPLETED_FILE, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []


def save_completed(done_tasks):
    with open(COMPLETED_FILE, "w") as file:
        json.dump(done_tasks, file, indent=4)


def validate_priority():
    while True:
        p = input(Fore.GREEN + "Priority (high/medium/low): ").lower().strip()
        if p in ["high", "medium", "low"]:
            return p
        print(Fore.RED + "Invalid priority. Type high/medium/low.")


def validate_date(prompt):
    while True:
        date = input(Fore.GREEN + prompt).strip()
        try:
            datetime.strptime(date, "%Y-%m-%d")
            return date
        except ValueError:
            print(Fore.RED + "Invalid date. Use YYYY-MM-DD format.")

def show_banner():
    print("|" * 20)
    print(Fore.CYAN + "--" * 10)
    print(Fore.YELLOW + "    To do list      ")
    print(Fore.CYAN + "--" * 10)
    print("|" * 20)
    time.sleep(0.3)

def show_menu():
    print(Fore.CYAN + "1. View Tasks")
    print("2. Add Task")
    print("3. Edit Task")
    print("4. Delete Task")
    print("5. Mark Completed")
    print("6. View Completed Tasks")
    print("7. Clear All Tasks")
    print("8. Exit")

def show_tasks(tasks):
    print(Fore.CYAN + "Pending Tasks:")

    if not tasks:
        print(Fore.YELLOW + "No tasks available.")
        return

    for i, t in enumerate(tasks, start=1):
        print(Fore.GREEN + f"{i}. {t['title']}")
        print(Fore.CYAN + f"   Priority: {t['priority']}")
        print(Fore.CYAN + f"   Deadline: {t['deadline']}")
        print(Fore.CYAN + f"   Description: {t['description']}")
        print()


def show_completed_tasks():
    completed = load_completed()
    print(Fore.MAGENTA + "Completed Tasks:")

    if not completed:
        print(Fore.YELLOW + "No completed tasks.")
        return

    for i, t in enumerate(completed, start=1):
        print(Fore.GREEN + f"{i}. {t['title']}")
        print(Fore.CYAN + f"   Completed On: {t['completed_on']}")
        print(Fore.CYAN + f"   Deadline: {t['deadline']}")

        if t["deadline"] != "Daily Task":
            d1 = datetime.strptime(t["deadline"], "%Y-%m-%d")
            d2 = datetime.strptime(t["completed_on"], "%Y-%m-%d")
            if d2 <= d1:
                print(Fore.GREEN + "   Finished Before Deadline")
            else:
                print(Fore.RED + "   Finished After Deadline")
        print()

def add_task(tasks):
    title = input(Fore.GREEN + "Task title: ").strip()
    while title == "":
        print(Fore.RED + "Title cannot be empty.")
        title = input(Fore.GREEN + "Task title: ").strip()

    priority = validate_priority()
    description = input(Fore.GREEN + "Description: ").strip()

    # DAILY OR DEADLINE
    while True:
        t = input(Fore.BLUE + "Is this a daily task? (y/n): ").lower().strip()
        if t in ["y", "n"]:
            break
        print(Fore.RED + "Invalid. Enter y or n.")

    if t == "y":
        deadline = "Daily Task"
    else:
        deadline = validate_date("Deadline (YYYY-MM-DD): ")

    tasks.append({
        "title": title,
        "priority": priority,
        "description": description,
        "deadline": deadline,
        "status": "pending"
    })

    save_tasks(tasks)
    print(Fore.GREEN + "Task added.")


def edit_task(tasks):
    show_tasks(tasks)
    if not tasks:
        return

    choice = input(Fore.GREEN + "Task number to edit: ").strip()

    if not choice.isdigit() or not (1 <= int(choice) <= len(tasks)):
        print(Fore.RED + "Invalid task number.")
        return

    t = tasks[int(choice) - 1]

    new_title = input(Fore.GREEN + f"New title ({t['title']}): ").strip()
    new_priority = input(Fore.GREEN + f"New priority ({t['priority']}): ").strip()
    new_description = input(Fore.GREEN + f"New description ({t['description']}): ").strip()
    new_deadline = input(Fore.GREEN + f"New deadline ({t['deadline']}): ").strip()

    if new_title:
        t['title'] = new_title
    if new_priority.lower() in ["high", "medium", "low"]:
        t['priority'] = new_priority.lower()
    if new_description:
        t['description'] = new_description
    if new_deadline:
        t['deadline'] = new_deadline

    save_tasks(tasks)
    print(Fore.GREEN + "Task updated.")

def delete_task(tasks):
    show_tasks(tasks)
    if not tasks:
        return

    choice = input(Fore.GREEN + "Task number to delete: ").strip()

    if choice.isdigit() and 1 <= int(choice) <= len(tasks):
        deleted = tasks.pop(int(choice) - 1)
        save_tasks(tasks)
        print(Fore.RED + f"Deleted: {deleted['title']}")
    else:
        print(Fore.RED + "Invalid number.")

def mark_completed(tasks):
    completed = load_completed()
    show_tasks(tasks)

    if not tasks:
        return

    while True:
        choice = input(Fore.GREEN + "Task number to mark completed: ").strip()
        if choice.isdigit():
            index = int(choice)
            if 1 <= index <= len(tasks):
                task = tasks.pop(index - 1)
                task["status"] = "done"
                task["completed_on"] = datetime.now().strftime("%Y-%m-%d")

                completed.append(task)

                save_tasks(tasks)
                save_completed(completed)

                print(Fore.GREEN + "Task marked as completed.")
                return

        print(Fore.RED + "Invalid number.")

def clear_all(tasks):
    confirm = input(Fore.RED + "Are you sure you want to delete ALL tasks? (y/n): ").lower()
    if confirm == "y":
        tasks.clear()
        save_tasks(tasks)
        print(Fore.RED + "All tasks cleared.")
    else:
        print(Fore.YELLOW + "Cancelled.")

def main():
    ensure_files()
    show_banner()

    while True:
        tasks = load_tasks()
        show_menu()

        choice = input(Fore.GREEN + "Choose (1-8): ").strip()

        if choice == "1":
            show_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            edit_task(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            mark_completed(tasks)
        elif choice == "6":
            show_completed_tasks()
        elif choice == "7":
            clear_all(tasks)
        elif choice == "8":
            print(Fore.YELLOW + "Thank you for using  our to do list!")
            break
        else:
            print(Fore.RED + "Invalid choice.")

if __name__ == "__main__":
    main()

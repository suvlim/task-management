from app.database import init_db
from app.service import (
    create_project,
    get_projects,
    get_project_with_tasks,
    delete_project,
    create_task,
    get_tasks,
    get_tasks_by_project,
    update_task_status,
    delete_task
)

# ================= UI HELPERS =================

def print_projects(projects):
    if not projects:
        print("\nNo projects found.")
        return

    print("\n=== PROJECT LIST ===")
    for p in projects:
        print(f"[{p['id']}] {p['name']} - {p['description']}")


def print_tasks(tasks):
    if not tasks:
        print("\nNo tasks found.")
        return

    print("\n=== TASK LIST ===")
    for t in tasks:
        print(f"[{t['id']}] {t['title']} ({t['status']})")


def input_int(prompt):
    try:
        return int(input(prompt))
    except ValueError:
        print("Invalid number input.")
        return None


def menu():
    print("\n=== TASK MANAGEMENT SYSTEM ===")
    print("1. Create Project")
    print("2. View Projects")
    print("3. View Project Detail")
    print("4. Delete Project")
    print("5. Create Task")
    print("6. View Tasks by Project")
    print("7. View All Tasks")
    print("8. Update Task Status")
    print("9. Delete Task")
    print("0. Exit")


# ================= MAIN APP =================

def main():
    init_db()

    while True:
        menu()
        choice = input("Choose menu: ").strip()

        try:
            # 1. Create Project
            if choice == "1":
                name = input("Project name: ")
                desc = input("Description: ")

                project = create_project(name, desc)
                print(f"Project created: [{project['id']}] {project['name']}")

            # 2. View Projects
            elif choice == "2":
                projects = get_projects()
                print_projects(projects)

            # 3. Project Detail
            elif choice == "3":
                project_id = input_int("Project ID: ")
                if project_id is None:
                    continue

                project = get_project_with_tasks(project_id)

                print(f"\n=== PROJECT DETAIL ===")
                print(f"ID   : {project['id']}")
                print(f"Name : {project['name']}")
                print(f"Desc : {project['description']}")

                print_tasks(project["tasks"])

            # 4. Delete Project
            elif choice == "4":
                project_id = input_int("Project ID: ")
                if project_id is None:
                    continue

                delete_project(project_id)
                print("Project deleted")

            # 5. Create Task
            elif choice == "5":
                title = input("Task title: ")
                project_id = input_int("Project ID: ")
                if project_id is None:
                    continue

                task = create_task(title, project_id)
                print(f"Task created: [{task['id']}] {task['title']}")

            # 6. View Tasks by Project
            elif choice == "6":
                project_id = input_int("Project ID: ")
                if project_id is None:
                    continue

                tasks = get_tasks_by_project(project_id)
                print_tasks(tasks)

            # 7. View All Tasks
            elif choice == "7":
                tasks = get_tasks()
                print_tasks(tasks)   
            
            # 8. Update Task Status
            elif choice == "8":
                task_id = input_int("Task ID: ")
                if task_id is None:
                    continue

                print("\nValid status:")
                print("TODO | ONGOING | REVIEW | REVISION | COMPLETE | CANCELLED")

                status = input("New status: ").strip().upper()

                result = update_task_status(task_id, status)
                print(f"Task updated to {result['status']}")

            # 9. Delete Task
            elif choice == "9":
                task_id = input_int("Task ID: ")
                if task_id is None:
                    continue

                delete_task(task_id)
                print("Task deleted")

            # 0. Exit
            elif choice == "0":
                print("Goodbye!")
                break

            else:
                print("Invalid menu choice")

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()

import pytest
import os
from app.database import init_db
from app.service import (
    create_project,
    get_projects,
    get_project_with_tasks,
    delete_project,
    create_task,
    get_tasks_by_project,
    get_tasks,
    update_task_status,
    delete_task
)

# Set Up Database
@pytest.fixture(autouse=True)
def setup_database():
    if os.path.exists("tasks.db"):
        os.remove("tasks.db")
    init_db()
    yield
    if os.path.exists("tasks.db"):
        os.remove("tasks.db")

# I-1. Test Full Proyek Flow (Buat Project -> Isi Task -> Update Status Task Hingga Complete -> Ambil Proyek dan Task -> Hapus Projek)
def test_full_project_lifecycle():
    # Buat Proyek
    project = create_project("Inventory System", "Inventory Products Management")
    assert project["id"] > 0
    assert project["name"] == "Inventory System"

    # Buat Tugas
    task1 = create_task("Create Login Feature", project["id"])
    task2 = create_task("Create Dashboard Feature", project["id"])
    assert task1["status"] == "TODO"
    assert task2["status"] == "TODO"

    # Ambil Tugas di Proyek
    tasks = get_tasks_by_project(project["id"])
    assert len(tasks) == 2
    assert tasks[0]["title"] == "Create Login Feature"
    assert tasks[0]["status"] == "TODO"


    # Update Status Tugas
    update_task_status(task1["id"], "ONGOING")
    update_task_status(task1["id"], "REVIEW")
    update_task_status(task1["id"], "COMPLETE")

    
    # Ambil Semua Tugas di Proyek
    project_detail = get_project_with_tasks(project["id"])
    assert len(project_detail["tasks"]) == 2
    assert any(t["status"] == "COMPLETE" for t in project_detail["tasks"])

   # Hapus Proyek
    result = delete_project(project["id"])
    assert result is True

    # Verifikasi Penghapusan
    projects = get_projects()
    assert len(projects) == 0


# I-2 . Test Ambil Proyek dan Tugasnya
def test_get_project_with_tasks():
    project = create_project("Test Project")
    create_task("Task 1", project["id"])
    create_task("Task 2", project["id"])
    detail = get_project_with_tasks(project["id"])
    assert len(detail["tasks"]) == 2

# I-3. Test Full Status Flow (Tanpa Revisi)
def test_status_transition_flow():
    project = create_project("Status Flow")
    task = create_task("Status Flow Test", project["id"])

    update_task_status(task["id"], "ONGOING")
    update_task_status(task["id"], "REVIEW")
    update_task_status(task["id"], "COMPLETE")

    tasks = get_tasks_by_project(project["id"])
    assert tasks[0]["status"] == "COMPLETE"

# I-4. Test Full Status Flow (Revisi)
def test_status_transition_revision_flow():
    project = create_project("Status Flow Revision")
    task = create_task("Task 1", project["id"])

    update_task_status(task["id"], "ONGOING")
    update_task_status(task["id"], "REVIEW")
    update_task_status(task["id"], "REVISION")
    update_task_status(task["id"], "ONGOING")
    result = update_task_status(task["id"], "REVIEW")

    assert result["status"] == "REVIEW"

# I-5. Test Invalid Complete Status Flow (Complete -> X)
def test_invalid_complete_transition_integration():
    project = create_project("Invalid Transition")
    task = create_task("Invalid Transition Complete", project["id"])

    update_task_status(task["id"], "ONGOING")
    update_task_status(task["id"], "REVIEW")
    update_task_status(task["id"], "COMPLETE")

    with pytest.raises(ValueError):
        update_task_status(task["id"], "ONGOING")

# I-6. Test Invalid Cancelled Status Flow (Cancelled -> X)
def test_invalid_cancelled_transition_integration():
    project = create_project("Invalid Transition")
    task = create_task("Invalid Transition Cancelled", project["id"])

    update_task_status(task["id"], "ONGOING")
    update_task_status(task["id"], "REVIEW")
    update_task_status(task["id"], "CANCELLED")

    with pytest.raises(ValueError):
        update_task_status(task["id"], "ONGOING")


# I-7. Test Penghapusan Tugas Terkait
def test_create_and_delete_tasks():
    project = create_project("Delete Tasks")
    task1 = create_task("Task 1", project["id"])
    task2 = create_task("Task 2", project["id"])

    delete_task(task1["id"])
    all_tasks = get_tasks()
    titles = [t["title"] for t in all_tasks]
    assert "Task 1" not in titles
    assert "Task 2" in titles

# I-8. Test Pemisahan Antar Proyek
def test_tasks_are_isolated_between_projects():
    project_a = create_project("Project A", "First project")
    project_b = create_project("Project B", "Second project")

    create_task("Task A1", project_a["id"])
    create_task("Task B1", project_b["id"])
  
    tasks_a = get_tasks_by_project(project_a["id"])
    tasks_b = get_tasks_by_project(project_b["id"])

    assert len(tasks_a) == 1
    assert len(tasks_b) == 1

    titles_a = [t["title"] for t in tasks_a]
    titles_b = [t["title"] for t in tasks_b]

    assert "Task B1" not in titles_a
    assert "Task A1" not in titles_b

import pytest
from unittest.mock import patch, MagicMock
from app.service import (
    create_project,
    get_projects,
    delete_project,
    create_task, 
    get_tasks,
    delete_task, 
    get_project_with_tasks,
    get_tasks_by_project,
)

# ======================PROYEK==========================================
# PEMBUATAN PROYEK
# P-1. Pembuatan Proyek Valid
def test_create_project_success():
    with patch('app.service.get_connection') as mock_get_conn:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.lastrowid = 5
        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn

        result = create_project("Website E-Commerce", "Proyek pengembangan website")

        assert result["id"] == 5
        assert result["name"] == "Website E-Commerce"
        assert result["description"] == "Proyek pengembangan website"
        mock_cursor.execute.assert_called_with(
            "INSERT INTO projects (name, description) VALUES (?, ?)",
            ("Website E-Commerce", "Proyek pengembangan website")
        )


# PENGAMBILAN DATA PROYEK
# P-1. Pengambilan Semua Proyek (Hanya Nama dan Deskripsi Proyek)
def test_get_projects_success():
    with patch('app.service.get_connection') as mock_get_conn:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            (1, "Project A", "Desc A"),
            (2, "Project B", "Desc B")
        ]
        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn

        projects = get_projects()
        assert len(projects) == 2
        assert projects[0]["name"] == "Project A"
        assert projects[1]["name"] == "Project B"
        assert projects[0]["description"] == "Desc A"
        assert projects[1]["description"] == "Desc B"

# P-2 Pengambilan Proyek dan Semua Tugas Di Dalamnya (Sukses)
def test_get_project_with_tasks_success():
    with patch('app.service.get_connection') as mock_get_conn:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
   
        mock_cursor.fetchone.side_effect = [
            (1, "Mobile App", "Aplikasi mobile")
        ]
        mock_cursor.fetchall.return_value = [
            (10, "Login Feature", "ONGOING"),
            (11, "Payment Integration", "TODO")
        ]
        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn

        result = get_project_with_tasks(1)
        assert result["id"] == 1
        assert result["name"] == "Mobile App"
        assert len(result["tasks"]) == 2

# PENGHAPUSAN DATA PROYEK
# P-1 Penghapusan Proyek Sukses
def test_delete_project_success():
    with patch('app.service.get_connection') as mock_get_conn:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (1,)
        mock_cursor.rowcount = 1
        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn

        result = delete_project(3)
        assert result is True
    
# ======================TUGAS==========================================
# PEMBUATAN TUGAS
# T-1 Test Pembuatan Tugas Valid
def test_create_task_success():
    with patch('app.service.get_connection') as mock_get_conn:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (1,) 
        mock_cursor.lastrowid = 42
        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn

        task = create_task("Belajar CI", 1)
        assert task["title"] == "Belajar CI"
        assert task["status"] == "TODO"

# PENGAMBILAN TUGAS
# T-1 Test Pengambilan Semua Tugas Valid
def test_get_tasks():
    with patch('app.service.get_connection') as mock_get_conn:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            (1, "Task A", "TODO"),
            (2, "Task B", "COMPLETE")
        ]
        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn

        tasks = get_tasks()
        assert len(tasks) == 2
        assert tasks[0]["title"] == "Task A"
        assert tasks[1]["title"] == "Task B"
        assert tasks[0]["status"] == "TODO"
        assert tasks[1]["status"] == "COMPLETE"

# T-2 Test Pengambilan Tugas Per Proyek
def test_get_tasks_by_project_success():
    with patch('app.service.get_connection') as mock_get_conn:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            (1, "Task 1", "TODO"),
            (2, "Task 2", "ONGOING")
        ]
        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn

        tasks = get_tasks_by_project(1)
        assert len(tasks) == 2
        assert tasks[0]["title"] == "Task 1"
        assert tasks[1]["title"] == "Task 2"
        assert tasks[0]["status"] == "TODO"
        assert tasks[1]["status"] == "ONGOING"

# PENGHAPUSAN TUGAS
# T-1 Test Penghapusan Tugas
def test_delete_task_success():
    with patch('app.service.get_connection') as mock_get_conn:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 1
        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn

        assert delete_task(10) is True


import pytest
from unittest.mock import patch, MagicMock
from app.service import (
    create_project,
    get_projects,
    delete_project,
    create_task, 
    get_tasks,
    delete_task, 
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


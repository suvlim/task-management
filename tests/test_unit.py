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
    update_task_status
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

# P-2. Pembuatan Proyek Nama Kosong
def test_create_project_empty_name():
    with pytest.raises(ValueError, match="Project name cannot be empty"):
        create_project("")

# P-3. Pembuatan Proyek Nama Whitespace
def test_create_project_whitespace_name():
    with pytest.raises(ValueError, match="Project name cannot be empty"):
        create_project("   ")

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

# P-3 Pengambilan Proyek Tidak Terdaftar
def test_get_project_with_tasks_not_found():
    with patch('app.service.get_connection') as mock_get_conn:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn

        with pytest.raises(ValueError, match="Project not found"):
            get_project_with_tasks(999)

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
        mock_cursor.execute.assert_any_call(
        "DELETE FROM projects WHERE id = ?",
        (3,)
        )
    
# P-2 Penghapusan Proyek Tidak Terdaftar
def test_delete_project_not_found():
    with patch('app.service.get_connection') as mock_get_conn:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn

        with pytest.raises(ValueError, match="Project not found"):
            delete_project(999)

# Penghapusan Proyek Invalid Proyek Id (Format Id)
def test_delete_project_invalid_id():
    with pytest.raises(ValueError, match="Valid project_id is required"):
        delete_project(-5)
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

# T-2 Test Pembuatan Tugas Judul Kosong
def test_create_task_empty():
    with pytest.raises(ValueError, match="Title cannot be empty"):
        create_task("", 1)

# T-3 Test Pembuatan Task WhiteSpace
def test_create_task_whitespace():
    with pytest.raises(ValueError, match="Title cannot be empty"):
        create_task("    ", 1)

# T-4 Test Pembuatan Task Invalid Project Id
def test_create_task_invalid_project_id():
    with pytest.raises(ValueError, match="Valid project_id is required"):
        create_task("test task", -5)

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

# PERUBAHAN STATUS TUGAS
# T-1 Test Perubahan Status Valid
def test_update_status_valid():
    with patch('app.service.get_connection') as mock_get_conn:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = ("ONGOING",)
        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn

        result = update_task_status(5, "REVIEW")
        assert result["status"] == "REVIEW"

# T-2 Test Perubahan Status Invalid Transition
def test_update_status_invalid_transition():
    with patch('app.service.get_connection') as mock_get_conn:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = ("COMPLETE",)
        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn

        with pytest.raises(ValueError):
            update_task_status(1, "ONGOING")

# T-3 Test Perubahan Status Invalid Status
def test_update_status_invalid_status():
    with pytest.raises(ValueError, match="Invalid status"):
        update_task_status(1, "UNKNOWN")
        
# T-4 Test Perubahan Status Pada Tugas Tidak di Data
def test_update_task_not_available():
    with patch('app.service.get_connection') as mock_get_conn:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
    
        mock_cursor.fetchone.return_value = None  
        
        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn

        with pytest.raises(ValueError) as exc_info:
            update_task_status(999, "ONGOING")
        
        assert "Task not found" in str(exc_info.value)

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

# T-2 Test Penghapusan Tugas Tidak Terdaftar
def test_delete_task_not_found():
    with patch('app.service.get_connection') as mock_get_conn:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 0
        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn

        with pytest.raises(ValueError, match="Task not found"):
            delete_task(999)


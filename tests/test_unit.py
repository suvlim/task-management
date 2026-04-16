import pytest
from unittest.mock import patch, MagicMock
from app.service import (
    create_project,
    get_projects,
    delete_project,
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
    

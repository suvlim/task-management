from app.database import get_connection

VALID_STATUS = [
    "TODO",
    "ONGOING",
    "REVIEW",
    "REVISION",
    "COMPLETE",
    "CANCELLED"
]

VALID_TRANSITIONS = {
    "TODO": ["ONGOING", "CANCELLED"],
    "ONGOING": ["REVIEW", "CANCELLED"],
    "REVIEW": ["COMPLETE", "REVISION", "CANCELLED"],
    "REVISION": ["ONGOING"],
    "COMPLETE": [],
    "CANCELLED": []
}


# Buat Proyek
def create_project(name, description=""):
    # Validasi Input (Nama Tidak Kosong)
    if not name or name.strip() == "":
        raise ValueError("Project name cannot be empty")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO projects (name, description) VALUES (?, ?)",
        (name.strip(), description.strip())
    )
    conn.commit()
    project_id = cursor.lastrowid
    conn.close()

    return {
        "id": project_id,
        "name": name.strip(),
        "description": description.strip()
    }

# Ambil Semua Proyek Yang Ada
def get_projects():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, description FROM projects")
    rows = cursor.fetchall()
    conn.close()

    return [
        {"id": row[0], "name": row[1], "description": row[2]}
        for row in rows
    ]

# Ambil Proyek dan Tugas Terkait
def get_project_with_tasks(project_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, name, description FROM projects WHERE id = ?", (project_id,))
    project = cursor.fetchone()
    if not project:
        conn.close()
        raise ValueError("Project not found")
    
    cursor.execute("""
        SELECT id, title, status 
        FROM tasks 
        WHERE project_id = ? 
        ORDER BY id
    """, (project_id,))
    tasks = cursor.fetchall()
    
    conn.close()
    
    return {
        "id": project[0],
        "name": project[1],
        "description": project[2],
        "tasks": [{"id": t[0], "title": t[1], "status": t[2]} for t in tasks]
    }

# Hapus Proyek
def delete_project(project_id):

    if not project_id or project_id <= 0:
        raise ValueError("Valid project_id is required")

    conn = get_connection()
    cursor = conn.cursor()

    # Cek apakah project ada
    cursor.execute("SELECT id FROM projects WHERE id = ?", (project_id,))
    if not cursor.fetchone():
        conn.close()
        raise ValueError("Project not found")


    cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))

    if cursor.rowcount == 0:
        conn.close()
        raise ValueError("Project not found")

    conn.commit()
    conn.close()

    return True

# Buat Tugas 
def create_task(title, project_id):
    # Validasi Input (Judul Tidak Kosong)
    if not title or title.strip() == "":
        raise ValueError("Title cannot be empty")
    # Validasi Proyek (Tidak Kosong & Terdaftar)
    if not project_id or project_id <= 0:
        raise ValueError("Valid project_id is required")

    conn = get_connection()
    cursor = conn.cursor()
 
    cursor.execute("SELECT id FROM projects WHERE id = ?", (project_id,))
    if not cursor.fetchone():
        conn.close()
        raise ValueError("Project not found")

    cursor.execute(
        "INSERT INTO tasks (title, status, project_id) VALUES (?, ?, ?)",
        (title.strip(), "TODO", project_id)
    )

    conn.commit()
    task_id = cursor.lastrowid
    conn.close()

    return {
        "id": task_id,
        "title": title.strip(),
        "status": "TODO",
        "project_id": project_id
    }

# Ambil Semua Tugas
def get_tasks():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, title, status FROM tasks")

    rows = cursor.fetchall()
    conn.close()

    return [
        {"id": row[0], "title": row[1], "status": row[2]}
        for row in rows
    ]

# Ambil Tugas Berdasarkan Proyek
def get_tasks_by_project(project_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, title, status FROM tasks WHERE project_id = ? ORDER BY id",
        (project_id,)
    )

    rows = cursor.fetchall()
    conn.close()

    return [
        {"id": row[0], "title": row[1], "status": row[2]}
        for row in rows
    ]

# Update Status Tugas 
def update_task_status(task_id, status):
    # Validasi status (Ada Pada Status yang Disediakan)
    if status not in VALID_STATUS:
        raise ValueError("Invalid status")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT status FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()

    # Pengecekan Keberadaan Tugas Yang Di-update
    if not row:
        conn.close()
        raise ValueError("Task not found")

    current_status = row[0]

    # Validasi transisi status
    allowed_next = VALID_TRANSITIONS[current_status]

    if status not in allowed_next:
        conn.close()
        # Ubah Semua Kemungkinan Perubahan Status yang Diizinkan ke String
        allowed_status = " or ".join(allowed_next)

        raise ValueError(
            f"{current_status} tasks can only be set to {allowed_status}"
        )
    
    cursor.execute(
        "UPDATE tasks SET status = ? WHERE id = ?",
        (status, task_id)
    )

    conn.commit()
    conn.close()

    return {
        "id": task_id,
        "status": status
    }

# Hapus Tugas
def delete_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))

    # Pengecekan Keberadaan Tugas Yang Di-hapus
    if cursor.rowcount == 0:
        conn.close()
        raise ValueError("Task not found")

    conn.commit()
    conn.close()

    return True

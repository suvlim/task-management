from app.database import get_connection


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
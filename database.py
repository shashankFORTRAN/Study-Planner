import sqlite3
from datetime import datetime

DB_NAME = "study_planner.db"


def connect():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


def create_tables():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            subject TEXT NOT NULL,
            priority TEXT NOT NULL,
            completed INTEGER DEFAULT 0,
            created_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weekly_plan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day TEXT UNIQUE NOT NULL,
            plan TEXT DEFAULT ''
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY,
            content TEXT DEFAULT ''
        )
    """)

    default_subjects = ["Python", "C Programming"]

    for subject in default_subjects:
        cursor.execute(
            "INSERT OR IGNORE INTO subjects (name) VALUES (?)",
            (subject,)
        )

    cursor.execute(
        "INSERT OR IGNORE INTO notes (id, content) VALUES (1, '')"
    )

    conn.commit()
    conn.close()


def get_subjects():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM subjects ORDER BY name")
    subjects = [row[0] for row in cursor.fetchall()]

    conn.close()
    return subjects


def add_subject(name):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT OR IGNORE INTO subjects (name) VALUES (?)",
        (name,)
    )

    conn.commit()
    conn.close()


def add_task(title, subject, priority):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tasks
        (title, subject, priority, completed, created_at)
        VALUES (?, ?, ?, 0, ?)
    """, (
        title,
        subject,
        priority,
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()


def get_tasks():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title, subject, priority, completed
        FROM tasks
        ORDER BY id DESC
    """)

    tasks = cursor.fetchall()

    conn.close()
    return tasks


def update_task(task_id, completed):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE tasks SET completed = ? WHERE id = ?",
        (int(completed), task_id)
    )

    conn.commit()
    conn.close()


def delete_task(task_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    conn.commit()
    conn.close()


def get_weekly_plan(day):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT plan FROM weekly_plan WHERE day = ?",
        (day,)
    )

    result = cursor.fetchone()

    conn.close()

    return result[0] if result else ""


def save_weekly_plan(day, plan):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO weekly_plan (day, plan)
        VALUES (?, ?)
        ON CONFLICT(day)
        DO UPDATE SET plan = excluded.plan
    """, (day, plan))

    conn.commit()
    conn.close()


def get_notes():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT content FROM notes WHERE id = 1"
    )

    result = cursor.fetchone()

    conn.close()

    return result[0] if result else ""


def save_notes(content):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE notes SET content = ? WHERE id = 1",
        (content,)
    )

    conn.commit()
    conn.close()

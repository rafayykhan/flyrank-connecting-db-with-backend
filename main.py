from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
import sqlite3

app = FastAPI(
    title="Task API",
    version="2.0"
)

DATABASE = "tasks.db"


# -----------------------------
# Database
# -----------------------------

def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done INTEGER NOT NULL
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.executemany(
            """
            INSERT INTO tasks(title, done)
            VALUES (?, ?)
            """,
            [
                ("Watch the W2 lecture", 1),
                ("Read MDN: How the web works", 0),
                ("Build the CRUD API", 0)
            ]
        )

    connection.commit()
    connection.close()


initialize_database()


# -----------------------------
# Helpers
# -----------------------------

def task_to_dict(row):
    return {
        "id": row["id"],
        "title": row["title"],
        "done": bool(row["done"])
    }


def get_task(task_id):
    connection = get_connection()

    row = connection.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    connection.close()

    if row:
        return task_to_dict(row)

    return None


def not_found(task_id):
    return JSONResponse(
        status_code=404,
        content={
            "error": f"Task {task_id} not found"
        }
    )


# -----------------------------
# Root
# -----------------------------

@app.get("/")
def root():
    return {
        "name": "Task API",
        "version": "2.0",
        "endpoints": [
            "/tasks"
        ]
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


# -----------------------------
# GET ALL TASKS
# -----------------------------

@app.get("/tasks")
def list_tasks():

    connection = get_connection()

    rows = connection.execute(
        "SELECT * FROM tasks"
    ).fetchall()

    connection.close()

    return [task_to_dict(row) for row in rows]


# -----------------------------
# GET ONE TASK
# -----------------------------

@app.get("/tasks/{task_id}")
def get_single_task(task_id: int):

    task = get_task(task_id)

    if task is None:
        return not_found(task_id)

    return task


# -----------------------------
# CREATE TASK
# -----------------------------

@app.post("/tasks", status_code=201)
async def create_task(request: Request):

    try:
        body = await request.json()
    except Exception:
        body = {}

    title = str(body.get("title") or "").strip()

    if title == "":
        return JSONResponse(
            status_code=400,
            content={
                "error": "title is required"
            }
        )

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO tasks(title, done)
        VALUES (?, ?)
        """,
        (
            title,
            0
        )
    )

    task_id = cursor.lastrowid

    connection.commit()

    row = connection.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    connection.close()

    return task_to_dict(row)


# -----------------------------
# UPDATE TASK
# -----------------------------

@app.put("/tasks/{task_id}")
async def update_task(task_id: int, request: Request):

    task = get_task(task_id)

    if task is None:
        return not_found(task_id)

    try:
        body = await request.json()
    except Exception:
        body = {}

    if "title" not in body and "done" not in body:
        return JSONResponse(
            status_code=400,
            content={
                "error": "title or done is required"
            }
        )

    title = task["title"]
    done = task["done"]

    if "title" in body:

        new_title = str(body.get("title") or "").strip()

        if new_title == "":
            return JSONResponse(
                status_code=400,
                content={
                    "error": "title cannot be empty"
                }
            )

        title = new_title

    if "done" in body:

        if not isinstance(body["done"], bool):
            return JSONResponse(
                status_code=400,
                content={
                    "error": "done must be true or false"
                }
            )

        done = body["done"]

    connection = get_connection()

    connection.execute(
        """
        UPDATE tasks
        SET title = ?, done = ?
        WHERE id = ?
        """,
        (
            title,
            int(done),
            task_id
        )
    )

    connection.commit()

    row = connection.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    connection.close()

    return task_to_dict(row)


# -----------------------------
# DELETE TASK
# -----------------------------

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):

    task = get_task(task_id)

    if task is None:
        return not_found(task_id)

    connection = get_connection()

    connection.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    connection.commit()
    connection.close()

    return Response(status_code=204)
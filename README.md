# FlyRank Backend API – Week 3 Assignment

A RESTful CRUD API built with **FastAPI** and **SQLite**.

This project is the continuation of Week 2. Instead of storing tasks in memory, all tasks are now stored in a SQLite database. This means data survives application restarts.

---

# Technologies

- Python 3.10+
- FastAPI
- SQLite (sqlite3)
- Uvicorn

---

# Why SQLite?

SQLite was chosen because it:

- stores everything in a single file
- requires no separate server
- requires zero configuration
- is lightweight
- automatically creates the database file
- keeps data after the application stops

The database file is named:

```
tasks.db
```

It is automatically created the first time the application runs.

---

# Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/tasks-api.git
```

Move into the project

```bash
cd tasks-api
```

Create a virtual environment

```bash
python -m venv venv
```

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the server

```bash
uvicorn main:app --reload
```

---

# API Documentation

FastAPI automatically generates Swagger UI.

Open:

```
http://127.0.0.1:8000/docs
```

---

# Project Structure

```
tasks-api/
│
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
└── tasks.db
```

---

# Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | / | API Information |
| GET | /health | Health Check |
| GET | /tasks | Get All Tasks |
| GET | /tasks/{id} | Get One Task |
| POST | /tasks | Create Task |
| PUT | /tasks/{id} | Update Task |
| DELETE | /tasks/{id} | Delete Task |

---

# Task Object

```json
{
    "id": 1,
    "title": "Buy Milk",
    "done": false
}
```

---

# Status Codes

| Code | Description |
|------|-------------|
|200|Success|
|201|Created|
|204|Deleted Successfully|
|400|Bad Request|
|404|Task Not Found|

---

# Database

The application automatically performs the following steps:

1. Creates **tasks.db** if it does not exist.
2. Creates the **tasks** table if it does not exist.
3. Checks whether the table is empty.
4. Inserts three sample tasks only on the first run.

The seed data is **never duplicated** after restarting the application.

---

# SQL Queries Used

## Create Table

```sql
CREATE TABLE IF NOT EXISTS tasks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    done INTEGER NOT NULL
);
```

---

## Get All Tasks

```sql
SELECT * FROM tasks;
```

---

## Get Task By ID

```sql
SELECT * FROM tasks
WHERE id = ?;
```

---

## Insert Task

```sql
INSERT INTO tasks(title, done)
VALUES(?, ?);
```

---

## Update Task

```sql
UPDATE tasks
SET title = ?, done = ?
WHERE id = ?;
```

---

## Delete Task

```sql
DELETE FROM tasks
WHERE id = ?;
```

---

# Example SQL Query (Stage 4)

Query

```sql
SELECT * FROM tasks;
```

Result

Returns every task stored inside the database.

---

# Testing Persistence

Run the server.

Create a task.

Example

```json
{
    "title":"Learn SQLite"
}
```

Stop the server.

Start the server again.

Run

```
GET /tasks
```

The task is still present because it is stored inside **tasks.db**.

---

# DB Browser Screenshot

Open **tasks.db** using **DB Browser for SQLite**.

Navigate to

```
Browse Data
```

Select

```
tasks
```

Take a screenshot and include it in your repository.

---

# Running on a Clean Clone

Delete the existing **tasks.db** file.

Run

```bash
uvicorn main:app --reload
```

The application automatically

- creates tasks.db
- creates the tasks table
- inserts the three sample tasks

No manual setup is required.

---

# Git Commits

Example commit history

```
Stage 0: create SQLite database

Stage 1: database read endpoints

Stage 2: insert into database

Stage 3: update and delete with SQL

Stage 4: explored SQLite

Stage 5: database documentation
```

---

# Author

Rafay

FlyRank Backend Internship

Week 3 Assignment
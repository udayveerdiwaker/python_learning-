# Project 03: Task Manager API

This project is a micro-service designed to track team tasks, assign priorities (Low, Medium, High), and manage task deadlines.

---

## 🚀 How to Run Locally

1. Navigate to this folder:
   ```bash
   cd python_practice/08_projects/03_task_manager
   ```
2. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```
3. Open your browser and navigate to: **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

---

## 📮 Postman API Request Guides

### 1. Create a Task (POST `/tasks`)
- **URL:** `http://127.0.0.1:8000/tasks`
- **Method:** `POST`
- **Headers:** `Content-Type: application/json`
- **Body (raw JSON):**
  ```json
  {
    "title": "Build FastAPI Front-End UI",
    "description": "Develop a glassmorphic dashboard for the AI Coding Assistant.",
    "priority": "High",
    "due_date": "2026-06-25"
  }
  ```

### 2. List Tasks with Filters (GET `/tasks`)
- **URL:** `http://127.0.0.1:8000/tasks?completed=false&priority=High`
- **Method:** `GET`
- *(Returns all uncompleted, high-priority tasks).*

### 3. Update Task Completion and Assignee (PUT `/tasks/{task_id}`)
- **URL:** `http://127.0.0.1:8000/tasks/1`
- **Method:** `PUT`
- **Headers:** `Content-Type: application/json`
- **Body (raw JSON):**
  ```json
  {
    "completed": true,
    "assignee_id": 2
  }
  ```

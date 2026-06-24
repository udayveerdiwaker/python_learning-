# 🚀 Running the Python Learning Project & Practice Lab

This guide explains how to run the two major parts of this repository:
1. **The Main Project**: A modern glassmorphic Post & Feed Dashboard (React frontend + FastAPI backend + JSON database).
2. **The Python Practice Lab**: A structured, 10-module learning environment.

---

## 💻 1. Main Project: Post & Feed Dashboard

This application consists of a **FastAPI backend** that handles database actions and security, and a **React (Vite) frontend** that displays the dashboard.

### A. Run the Backend (FastAPI)
The backend manages posts in a local file database (`posts.json`) and seeds 10,000 items on startup.

1. Open a new terminal.
2. Navigate to the `backend` folder:
   ```bash
   cd backend
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the server:
   ```bash
   python main.py
   ```
   * *Server endpoint:* **`http://localhost:8000`**
   * *Interactive API documentation (Swagger):* **`http://localhost:8000/docs`**

### B. Run the Frontend (React + Vite)
The frontend provides a dark-mode community feed and dashboard.

1. Open a second, separate terminal window.
2. Navigate to the `frontend` folder:
   ```bash
   cd frontend
   ```
3. Install the Node packages:
   ```bash
   npm install
   ```
4. Start the Vite development server:
   ```bash
   npm run dev
   ```
   * *App URL:* **`http://localhost:5173`**

---

## 🐍 2. The Python Practice Lab (`python_practice/`)

The practice lab contains step-by-step learning modules (from `01_python_basics` to `10_ai_coding_assistant`).

### A. Python Executable Location
A fresh installation of **Python 3.12** is configured on your system at:
`C:\Users\udayv\AppData\Local\Programs\Python\Python312\python.exe`

If standard commands like `python` or `python3` do not work in your current terminal session (due to unsaved environment paths), use the absolute path:
```bash
& "C:\Users\udayv\AppData\Local\Programs\Python\Python312\python.exe" <script_name.py>
```

### B. Running Module 01 (Python Basics)
Navigate to the module directory:
```bash
cd python_practice/01_python_basics
```

* **Run the basics tutorial:**
  ```bash
  & "C:\Users\udayv\AppData\Local\Programs\Python\Python312\python.exe" basics.py
  ```
* **Run the practice automated tests:**
  ```bash
  $env:PYTHONUTF8=1; & "C:\Users\udayv\AppData\Local\Programs\Python\Python312\python.exe" exercises.py
  ```
* **Play the interactive RPG Challenge game:**
  ```bash
  & "C:\Users\udayv\AppData\Local\Programs\Python\Python312\python.exe" challenge.py
  ```

---

## 📁 3. Directory Structure Details

* **`backend/`**: Contains `main.py` which exposes GET/POST routes for the posts feed, generates authentication tokens, and writes data to `posts.json`.
* **`frontend/`**: Contains the React code. The main dashboard and community feed logic is in `src/App.jsx`.
* **`python_practice/`**:
  * `01_python_basics/`: Variables, lists, dicts, conditionals, loops, functions, and OOP.
  * `02_file_handling/` to `09_testing/`: Step-by-step concepts, files, databases, and testing tools.
  * `10_ai_coding_assistant/`: A local FastAPI chat interface using Gemini API to serve as an interactive learning mentor.

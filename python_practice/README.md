# 🐍 Python, MySQL & FastAPI Practice Lab

Welcome to the Python Practice Lab! This directory is a structured, hands-on learning environment designed to take you from a Python beginner to building and testing advanced, real-world REST APIs with MySQL databases and JWT authentication.

---

## 🗺️ Learning Path

The directory is divided into 10 step-by-step modules. Each folder contains its own `README.md` explaining the concepts, starter files with line-by-line comments, practice exercises, and a final challenge task.

1. **[01_python_basics](./01_python_basics/)**
   - *Topics:* Variables, data types, lists, dictionaries, conditionals, loops, functions, and basic object-oriented programming (OOP).
2. **[02_file_handling](./02_file_handling/)**
   - *Topics:* Opening, reading, writing, and appending files; working with CSVs, using context managers (`with` statements).
3. **[03_json_crud](./03_json_crud/)**
   - *Topics:* JSON serialization (`json.dumps`) and deserialization (`json.loads`), building a local file-based CRUD database.
4. **[04_mysql_crud](./04_mysql_crud/)**
   - *Topics:* Connecting to a MySQL server, creating tables, inserting, reading, updating, and deleting rows using SQL queries.
5. **[05_fastapi_basics](./05_fastapi_basics/)**
   - *Topics:* Setting up a FastAPI app, path & query parameters, request bodies, and Pydantic validation schemas.
6. **[06_rest_apis](./06_rest_apis/)**
   - *Topics:* REST architecture principles, standard HTTP verbs (`GET`, `POST`, `PUT`, `DELETE`), and REST status codes.
7. **[07_authentication](./07_authentication/)**
   - *Topics:* Security, password hashing (bcrypt), JSON Web Tokens (JWT) creation, token verification, and protecting routes.
8. **[08_projects](./08_projects/)**
   - *Real-world Projects:*
     - **User Management System:** Signup, profile retrieval, updating users.
     - **Blog API:** Multi-author posts, category management.
     - **Task Manager API:** TODOs with priorities, deadlines, and completion states.
     - **Authentication System:** Token refresh endpoints, password resets, role-based controls.
     - **E-commerce API:** Products, shopping cart, orders management.
9. **[09_testing](./09_testing/)**
   - *Topics:* Unit testing with `pytest`, API endpoint testing using FastAPI's `TestClient`.
10. **[10_ai_coding_assistant](./10_ai_coding_assistant/)**
    - *The AI Tool:* A premium ChatGPT-like local web application to practice code generation, explanation, debugging, optimization, API design, and database queries.

---

## 🚀 Setup Instructions

Follow these steps to configure your environment and start practicing:

### 1. Create a Python Virtual Environment
Creating a virtual environment ensures that the learning dependencies do not conflict with other Python projects on your computer.

```bash
# Navigate to the python_practice directory
cd python_practice

# Create a virtual environment named "venv"
python -m venv venv

# Activate the virtual environment
# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# On Windows (CMD):
.\venv\Scripts\activate.bat
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies
Install all the modules required for the FastAPI servers, database connection, and testing:

```bash
pip install -r requirements.txt
```

### 3. Configure MySQL Database
For the MySQL sections and projects, make sure your MySQL server is running (e.g., via XAMPP, Laragon, or standalone installation).

1. Log in to your MySQL terminal or database client (phpMyAdmin, DBeaver, etc.).
2. Run the SQL script located in `04_mysql_crud/setup_db.sql` to initialize your databases and tables:
   ```sql
   CREATE DATABASE IF NOT EXISTS python_practice_db;
   ```
3. Update connection parameters (host, user, password) inside `04_mysql_crud/db_connection.py` if your database uses custom credentials.

---

## 🤖 Launch the AI Coding Assistant

To launch the ChatGPT-like AI assistant:
1. Navigate to the folder:
   ```bash
   cd 10_ai_coding_assistant
   ```
2. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload --port 8080
   ```
3. Open your browser and navigate to: **`http://127.0.0.1:8080`**
4. Paste your Gemini API Key in the settings panel to enable live coding discussions, or use the pre-configured educational modules directly.

Let's get coding! 🚀

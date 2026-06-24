# 🛠️ Command Cheat Sheet - Chat API

A complete list of commands required to set up, initialize, and run the advanced real-time Chat API project on Windows.

---

## 1. Environment & Setup Commands

Use these commands to navigate to the project directory and prepare your virtual environment.

```powershell
# Step 1: Navigate to the chat_api directory
cd "c:\Users\User\Desktop\python_learning-\chat_api"

# Step 2: Create a virtual environment (run only if the 'venv' folder does not exist)
python -m venv venv
```

---

## 2. Dependency Installation Commands

Install all required Python packages (FastAPI, Uvicorn, SQLAlchemy, MySQL Connector, and WebSockets).

```powershell
# Step 1: Upgrade pip to the latest version inside the venv
.\venv\Scripts\python -m pip install --upgrade pip

# Step 2: Install dependencies from the requirements file
.\venv\Scripts\pip install -r requirements.txt

# Alternative: Install packages manually one by one
.\venv\Scripts\pip install fastapi uvicorn sqlalchemy mysql-connector-python websockets
```

---

## 3. Database Initialization Commands

If you need to verify or manually create the tables in your database before launching the server.

```powershell
# Run the helper script to initialize tables in your MySQL database ('chat_api')
.\venv\Scripts\python create_db.py
```

---

## 4. Run the Application Server

Start the Uvicorn development server with live reload.

```powershell
# Start the FastAPI server on default port 8000
.\venv\Scripts\python -m uvicorn main:app --reload

# Start the FastAPI server on a custom port (e.g. 8080)
.\venv\Scripts\python -m uvicorn main:app --reload --port 8080
```

Once running, access the web client at:
👉 **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## 5. MySQL Reference Queries

Use these queries in phpMyAdmin (or any MySQL tool) to manage your database table.

```sql
-- View all chat messages stored in the database
SELECT * FROM messages;

-- Clear all chat messages from the database
TRUNCATE TABLE messages;

-- Insert a test message manually
INSERT INTO messages (sender, message, room, created_at) 
VALUES ('System', 'Hello from SQL!', 'general', NOW());
```

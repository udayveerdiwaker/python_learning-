# Project 01: User Management System Micro-Service

This project is a micro-service managing user profiles, registrations, and login credentials. It utilizes FastAPI, SQLAlchemy ORM, and MySQL.

---

## 🚀 How to Run Locally

1. Open your terminal and navigate to this folder:
   ```bash
   cd python_practice/08_projects/01_user_management
   ```
2. Start the Uvicorn ASGI server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```
3. Open your browser to test endpoints directly inside the Swagger UI: **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

---

## 📮 Postman API Request Guides

Here is how you can configure requests inside Postman:

### 1. User Registration (POST `/register`)
- **URL:** `http://127.0.0.1:8000/register`
- **Method:** `POST`
- **Headers:** `Content-Type: application/json`
- **Body (raw JSON):**
  ```json
  {
    "username": "learning_coder",
    "email": "coder@example.com",
    "password": "mysecretpassword123"
  }
  ```

### 2. User Login (POST `/login`)
- **URL:** `http://127.0.0.1:8000/login`
- **Method:** `POST`
- **Body (form-data):**
  - Key: `username` | Value: `learning_coder`
  - Key: `password` | Value: `mysecretpassword123`
- **Response:**
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsIn...",
    "token_type": "bearer"
  }
  ```

### 3. Update User Profile (PUT `/users/{user_id}`)
- **URL:** `http://127.0.0.1:8000/users/1` (replace `1` with the actual user ID)
- **Method:** `PUT`
- **Headers:** `Content-Type: application/json`
- **Body (raw JSON):**
  ```json
  {
    "email": "new_coder_email@example.com",
    "password": "newpassword123"
  }
  ```

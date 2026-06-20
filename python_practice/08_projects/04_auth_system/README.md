# Project 04: Role-Based Authentication System

This service implements standard secure JWT authentication, Token Refresh rotation, and Role-Based Access Control (RBAC) to guard admin-only routes.

---

## 🚀 How to Run Locally

1. Navigate to this folder:
   ```bash
   cd python_practice/08_projects/04_auth_system
   ```
2. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```
3. Open your browser and navigate to: **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

---

## 📮 Postman API Request Guides

### 1. Login to Get Token Pair (POST `/login`)
- **URL:** `http://127.0.0.1:8000/login`
- **Method:** `POST`
- **Body (form-data):**
  - Key: `username` | Value: `admin_user` *(role: Admin)* or `john_doe` *(role: User)*
  - Key: `password` | Value: `password123`
- **Response:**
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
    "token_type": "bearer"
  }
  ```

### 2. Refresh Access Token (POST `/refresh`)
- **URL:** `http://127.0.0.1:8000/refresh`
- **Method:** `POST`
- **Headers:** `Content-Type: application/json`
- **Body (raw JSON):**
  ```json
  {
    "refresh_token": "<insert_your_refresh_token_here>"
  }
  ```
- *(Returns a new access and refresh token pair).*

### 3. Test Admin Guard Endpoint (GET `/admin-only`)
- **URL:** `http://127.0.0.1:8000/admin-only`
- **Method:** `GET`
- **Headers:**
  - `Authorization: Bearer <your_access_token>`
- **Result:**
  - If logged in as `admin_user`: Returns `200 OK` and a welcome message.
  - If logged in as `john_doe`: Returns `403 Forbidden` ("Admin privileges required").

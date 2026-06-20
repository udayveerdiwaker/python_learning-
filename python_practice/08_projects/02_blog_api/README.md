# Project 02: Blog API Micro-Service

This project implements a multi-author blogging engine. It features relational schemas (categories and posts) and ownership verification logic.

---

## 🚀 How to Run Locally

1. Navigate to this folder:
   ```bash
   cd python_practice/08_projects/02_blog_api
   ```
2. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```
3. Open your browser and navigate to: **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

---

## 📮 Postman API Request Guides

Some endpoints in this API require authentication. Make sure you register and login in Project 1 or Project 4 to retrieve an `access_token`.

### 1. Get Blog Posts (GET `/blogs`)
- **URL:** `http://127.0.0.1:8000/blogs`
- **Method:** `GET`
- **Query Params (optional):** `category_id` (e.g. `?category_id=1`)

### 2. Create Blog Post (POST `/blogs`)
- **URL:** `http://127.0.0.1:8000/blogs`
- **Method:** `POST`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer <your_access_token>`
- **Body (raw JSON):**
  ```json
  {
    "title": "Getting Started with FastAPI",
    "content": "This is a comprehensive guide to building REST APIs using FastAPI.",
    "category_id": 1
  }
  ```

### 3. Update Blog Post (PUT `/blogs/{blog_id}`)
- **URL:** `http://127.0.0.1:8000/blogs/1` (replace `1` with the actual blog ID)
- **Method:** `PUT`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer <your_access_token>`
- **Body (raw JSON):**
  ```json
  {
    "title": "Mastering FastAPI and ORMs",
    "content": "Updated content: Learning SQLAlchemy helps map database rows into python objects easily.",
    "category_id": 1
  }
  ```
  *(Note: This request will fail with a `403 Forbidden` if the `access_token` does not belong to the user who created the blog post).*

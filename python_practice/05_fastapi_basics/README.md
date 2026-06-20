# Module 05: FastAPI Basics ⚡

In this module, you will learn the fundamentals of building web servers in Python using **FastAPI**—one of the fastest, most popular web frameworks for building high-performance REST APIs.

---

## 📚 Topics Covered

1. **FastAPI & Uvicorn**: Understanding the difference between a web framework (FastAPI) and an ASGI web server (Uvicorn).
2. **Routing & HTTP Methods**: Mapping URLs to Python functions (e.g. `@app.get("/")`).
3. **Path Parameters**: Passing variables directly inside the URL path (e.g. `/items/{item_id}`).
4. **Query Parameters**: Passing optional parameters using the key-value URL query format (e.g. `/items?category=books&limit=5`).
5. **Request Bodies & Pydantic**: Defining JSON schemas using Pydantic models to automatically parse, validate, and document incoming data.
6. **Automatic API Documentation**: Exploring FastAPI's interactive Swagger UI documentation at `/docs` and Redoc at `/redoc`.

---

## 🗂️ Files in this Module

- `main.py`: A commented FastAPI starter code server. Run it using:
  ```bash
  uvicorn main:app --reload --port 8000
  ```
  And navigate to: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- `exercises.py`: Code exercises where you practice defining path/query parameters and Pydantic validation schemas.
- `challenge.py`: A complete product catalog API challenge where you will build CRUD endpoints for items. Run it using:
  ```bash
  uvicorn challenge:app --reload --port 8001
  ```

---

## ✍️ Practice Exercises Overview

Inside `exercises.py`, you will find templates to complete:
1. A GET route `/greet/{name}` that takes a name and returns a JSON greeting message.
2. A GET route `/search` that takes an optional query parameter `q` and page number `page` and returns them.
3. A Pydantic schema class `UserSignUp` validating user registration input.

---

## 🏆 Challenge Task: Product Catalog API
Inside `challenge.py`, you will complete a FastAPI server managing products in memory:
- Create schemas for Product.
- Implement endpoints:
  - `POST /products` to add a product (with validation like price > 0).
  - `GET /products` to list products (with optional minimum price filter).
  - `GET /products/{product_id}` to retrieve a single product.
  - `DELETE /products/{product_id}` to delete a product.

# Module 08: Real-World Micro-Service Projects 🚀

This module houses 5 real-world REST API projects built using **FastAPI**, **SQLAlchemy ORM (Object-Relational Mapping)**, and **MySQL**. These projects represent typical backend micro-services found in modern software architecture.

---

## 🏗️ The 5 Projects

1. **[01_user_management](./01_user_management/)**: User Registration, profile retrieval, updates, and account creation.
2. **[02_blog_api](./02_blog_api/)**: Multi-author blog platform with articles, categories, and owner-guarded deletion.
3. **[03_task_manager](./03_task_manager/)**: Team Task tracker with priority levels (Low, Medium, High), deadlines, and statuses.
4. **[04_auth_system](./04_auth_system/)**: Auth service implementing Role-Based Access Control (Admin vs User) and JWT Refresh Tokens.
5. **[05_ecommerce_api](./05_ecommerce_api/)**: E-commerce catalog with shopping cart management, orders creation, and checkout.

---

## 🐬 Database Setup for Projects

All projects connect to the same local MySQL database: `python_practice_db` but use distinct table prefixes to avoid conflict.

Before running any project, run the SQL script [setup_projects_db.sql](./setup_projects_db.sql) in your MySQL console. This initializes all tables:
- `proj_users` (for Project 1 & 4)
- `proj_blogs` and `proj_categories` (for Project 2)
- `proj_tasks` (for Project 3)
- `proj_products`, `proj_cart_items`, and `proj_orders` (for Project 5)

---

## 🚀 How to Run the Projects

1. Ensure your virtual environment is active and database tables are loaded.
2. Navigate to any project directory:
   ```bash
   cd 08_projects/01_user_management
   ```
3. Start the FastAPI server using Uvicorn:
   ```bash
   uvicorn main:app --reload --port 8000
   ```
4. Explore and test endpoints using the interactive documentation at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

---

## 📮 API Testing with Postman
Every project contains a detailed `README.md` containing sample JSON request bodies, headers, and endpoints so you can construct test collections in Postman.
- Set headers: `Content-Type: application/json`
- For protected routes, set Authorization header: `Bearer <your_token>`

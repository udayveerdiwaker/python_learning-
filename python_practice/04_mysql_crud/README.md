# Module 04: MySQL CRUD Operations 🐬

In this module, you will transition from local text/JSON files to a real relational database manager: **MySQL**. You will learn how to connect Python to a MySQL server, write SQL queries, and perform robust database operations (Create, Read, Update, Delete).

---

## 📚 Topics Covered

1. **MySQL Connector Driver**: Installing and using `mysql-connector-python` to communicate between Python and MySQL.
2. **Database Configuration**: Configuring credentials (host, username, password, database name) in a safe and structured manner.
3. **Database Schema & Seeding**: Writing SQL queries to create databases, tables, and insert starting seed data.
4. **Python-MySQL CRUD Operations**:
   - **CREATE**: `INSERT INTO` queries using parameterized inputs (to prevent SQL injection attacks).
   - **READ**: `SELECT` queries with `fetchone()` and `fetchall()` to retrieve database rows.
   - **UPDATE**: `UPDATE ... SET` queries to alter specific row data.
   - **DELETE**: `DELETE FROM` queries to safely remove records.
5. **Transactions**: Committing changes to the database using `connection.commit()` and rolling back on errors with `connection.rollback()`.

---

## ⚙️ Database Setup

Before running the python files, you need to set up the database:
1. Ensure your MySQL server (like XAMPP MySQL, Laragon, or standalone MySQL) is running.
2. Open your database GUI (phpMyAdmin, DBeaver, etc.) or standard MySQL CLI.
3. Open and run the contents of [setup_db.sql](./setup_db.sql). This will:
   - Create a database named `python_practice_db`.
   - Create a table named `students`.
   - Seed it with initial sample rows.

---

## 🗂️ Files in this Module

- `setup_db.sql`: The SQL commands to build the database, tables, and starter data.
- `db_connection.py`: Reusable, robust database connection helper function with clean error handling. Run it to test if your MySQL credentials connect successfully:
  ```bash
  python db_connection.py
  ```
- `mysql_crud.py`: A fully commented tutorial script performing complete CREATE, READ, UPDATE, and DELETE actions on the `students` table. Run it using:
  ```bash
  python mysql_crud.py
  ```
- `exercises.py`: Practice tasks for you to complete to practice database querying. Run it using:
  ```bash
  python exercises.py
  ```
- `challenge.py`: A library book database system CLI utilizing MySQL. Run it using:
  ```bash
  python challenge.py
  ```

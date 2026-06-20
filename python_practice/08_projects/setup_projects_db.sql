-- setup_projects_db.sql
-- Initializes all tables required for the 5 real-world projects in Module 08.

CREATE DATABASE IF NOT EXISTS python_practice_db;
USE python_practice_db;

-- ==============================================================================
-- 1. Tables for Projects 01 & 04 (User Management & Auth System)
-- ==============================================================================
DROP TABLE IF EXISTS proj_users;
CREATE TABLE proj_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'User', -- 'User' or 'Admin'
    is_active BOOLEAN DEFAULT TRUE,
    refresh_token VARCHAR(255) DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Seed an Admin and a standard User (passwords are bcrypt hash of 'password123')
INSERT INTO proj_users (username, email, hashed_password, role) VALUES 
('admin_user', 'admin@example.com', '$2b$12$R.S4oG/d1ZpGfFqJq8l8EuD/hA6pD7QexgD9.P2T1f7m/5t7e.Vre', 'Admin'),
('john_doe', 'john@example.com', '$2b$12$R.S4oG/d1ZpGfFqJq8l8EuD/hA6pD7QexgD9.P2T1f7m/5t7e.Vre', 'User');


-- ==============================================================================
-- 2. Tables for Project 02 (Blog API)
-- ==============================================================================
DROP TABLE IF EXISTS proj_blogs;
DROP TABLE IF EXISTS proj_categories;

CREATE TABLE proj_categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE proj_blogs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    category_id INT NULL,
    author_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES proj_categories(id) ON DELETE SET NULL
);

-- Seed Categories
INSERT INTO proj_categories (name) VALUES ('Tech'), ('Life'), ('Tutorials');


-- ==============================================================================
-- 3. Tables for Project 03 (Task Manager API)
-- ==============================================================================
DROP TABLE IF EXISTS proj_tasks;
CREATE TABLE proj_tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    description TEXT,
    priority VARCHAR(20) DEFAULT 'Medium', -- 'Low', 'Medium', 'High'
    due_date DATE NULL,
    completed BOOLEAN DEFAULT FALSE,
    assignee_id INT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Seed some tasks
INSERT INTO proj_tasks (title, description, priority, due_date, completed) VALUES 
('Design API Schema', 'Create tables and plan relational schemas', 'High', '2026-06-25', FALSE),
('Write Unit Tests', 'Achieve 80% code coverage using pytest', 'Medium', '2026-06-29', FALSE);


-- ==============================================================================
-- 4. Tables for Project 05 (E-commerce API)
-- ==============================================================================
DROP TABLE IF EXISTS proj_order_items;
DROP TABLE IF EXISTS proj_orders;
DROP TABLE IF EXISTS proj_cart_items;
DROP TABLE IF EXISTS proj_products;

CREATE TABLE proj_products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL DEFAULT 0
);

CREATE TABLE proj_cart_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(100) NOT NULL, -- Used to track guest carts
    product_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    FOREIGN KEY (product_id) REFERENCES proj_products(id) ON DELETE CASCADE
);

CREATE TABLE proj_orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_email VARCHAR(150) NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(50) DEFAULT 'Pending', -- 'Pending', 'Processing', 'Shipped', 'Cancelled'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE proj_order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES proj_orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES proj_products(id) ON DELETE CASCADE
);

-- Seed products
INSERT INTO proj_products (name, price, stock) VALUES 
('Professional Coding Keyboard', 120.00, 50),
('Ergonomic Mouse', 65.50, 100),
('USB-C Hub Multi-port', 45.00, 200),
('Full HD Webcam', 89.99, 10);

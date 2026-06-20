-- setup_db.sql
-- Run this SQL script in your MySQL client to initialize the learning database.

-- 1. Create the database if it doesn't already exist
CREATE DATABASE IF NOT EXISTS python_practice_db;

-- 2. Switch to using this database
USE python_practice_db;

-- 3. Drop table if it exists to start fresh
DROP TABLE IF EXISTS students;

-- 4. Create the students table
CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    subject VARCHAR(100) NOT NULL,
    score INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. Seed sample data for practice
INSERT INTO students (name, subject, score) VALUES 
('Alice Smith', 'Python', 95),
('Bob Jones', 'MySQL', 88),
('Charlie Brown', 'FastAPI', 92),
('David Miller', 'Python', 78),
('Emma Watson', 'MySQL', 85);

-- 6. Verify seed data
SELECT * FROM students;

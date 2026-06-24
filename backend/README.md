# FastAPI Backend & MySQL Database Documentation

This directory contains the FastAPI backend, data migration scripts, and utility tools for the Python Practice project.

---

## 1. Prerequisites
Ensure you have the following installed and running:
* **Python 3.8+** (with virtual environment in `venv`)
* **XAMPP Control Panel** (or standalone MySQL/MariaDB server)

---

## 2. Database Configuration
* **DBMS**: MySQL / MariaDB
* **Database Name**: `python_post_db`
* **Table Name**: `posts`
* **Host**: `127.0.0.1` (localhost)
* **Port**: `3306`
* **User**: `root`
* **Password**: *(empty)*

### Posts Table Schema
```sql
CREATE TABLE posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    content TEXT NOT NULL,
    author VARCHAR(50) NOT NULL,
    category VARCHAR(20) DEFAULT 'General',
    likes INT DEFAULT 0,
    small_cover_image VARCHAR(255) DEFAULT '',
    medium_cover_image VARCHAR(255) DEFAULT '',
    large_cover_image VARCHAR(255) DEFAULT '',
    screenshots JSON NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Comments Table Schema
```sql
CREATE TABLE comments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    post_id INT NOT NULL,
    author VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE
);
```

---

## 3. Quick Run Scripts
We have included double-clickable Windows Batch (`.bat`) files in this folder for easy execution:

1. **`run_migration.bat`**: Double-click this to install the required Python libraries and import all 10,001 posts from `posts.json` into MySQL.
2. **`run_backend.bat`**: Double-click this to start the FastAPI server on `http://127.0.0.1:8000`.

---

## 4. Main API Endpoints

Once the backend is running (`run_backend.bat`), you can access these endpoints:

* **Interactive OpenAPI Docs**: `http://127.0.0.1:8000/docs`
* **Get Posts (Paginated & Filtered)**: `GET /v1/api/get_posts?page=1&limit=12&category=Tech&search=Hacking`
* **Search Posts**: `GET /v1/api/posts/search?query=Hacking`
* **Create Post**: `POST /v1/api/create_posts` (Requires Bearer Token)
* **Delete Post**: `DELETE /v1/api/posts/delete/{post_id}` (Requires Bearer Token)
* **Get Comments**: `GET /v1/api/posts/{post_id}/comments`
* **Create Comment**: `POST /v1/api/posts/{post_id}/comments` (Requires Bearer Token)
* **Stats Summary**: `GET /v1/api/stats/summary`
* **Stats Categories**: `GET /v1/api/stats/categories`

---

## 5. Premium Interactive Features
1. **Interactive Image Lightbox Overlay**: Clicking on any post cover image or screenshot thumbnail launches a full-screen, responsive image viewer with next/prev pagination, keyboard support (Arrow Keys to navigate, Escape to close), and a direct link to the original high-resolution asset.
2. **Bookmarks & Saved Posts**: Users can bookmark any post directly from the card. Bookmarked items are saved locally in the browser and filtered via a dedicated "Bookmarks" filter pill.
3. **Popup API Key Generator**: Protects operations dynamically through a beautiful, glassmorphic security session activation modal.


-- 1. Create and select the database
CREATE DATABASE IF NOT EXISTS python_post_db;
USE python_post_db;

-- 2. Create the posts table
CREATE TABLE IF NOT EXISTS posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    content TEXT NOT NULL,
    author VARCHAR(50) NOT NULL,
    category VARCHAR(20) DEFAULT 'General',
    likes INT DEFAULT 0,
    small_cover_image VARCHAR(255) DEFAULT '',
    medium_cover_image VARCHAR(255) DEFAULT '',
    large_cover_image VARCHAR(255) DEFAULT '',
    screenshots JSON NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 3. Insert sample data from posts.json
INSERT INTO posts (id, title, content, author, category, likes, small_cover_image, medium_cover_image, large_cover_image, screenshots, created_at) VALUES
(1, 'The Future of Indie Hacking', 'This approach has helped us scale to thousands of daily active users with minimal hosting costs. Leveraging modular component design patterns lets teams ship clean features faster.', 'Fatima Al-Sayed', 'Tech', 261, 'https://picsum.photos/seed/photo-sm-1/200/300', 'https://picsum.photos/seed/photo-med-1/600/350', 'https://picsum.photos/seed/photo-large-1/1000/600', '["https://picsum.photos/seed/photo-scr1-1/500/300", "https://picsum.photos/seed/photo-scr2-1/500/300", "https://picsum.photos/seed/photo-scr3-1/500/300"]', '2026-06-05 20:35:20'),
(2, 'Introduction to UX Best Practices', 'A clean and responsive interface is the boundary between user delight and frustration. Continuous iteration and user testing are the only ways to build a product people actually want.', 'Alex Rivera', 'Tech', 86, 'https://picsum.photos/seed/photo-sm-2/200/300', 'https://picsum.photos/seed/photo-med-2/600/350', 'https://picsum.photos/seed/photo-large-2/1000/600', '["https://picsum.photos/seed/photo-scr1-2/500/300", "https://picsum.photos/seed/photo-scr2-2/500/300", "https://picsum.photos/seed/photo-scr3-2/500/300"]', '2026-06-05 20:37:20'),
(3, 'Sleek Indie Hacking', 'Choosing the right stack is critical. We dive deep into the trade-offs of using modern micro-frameworks. In this article, we cover key architectural decisions to maximize developer efficiency and system uptime.', 'Chloe Dubois', 'Idea', 378, 'https://picsum.photos/seed/photo-sm-3/200/300', 'https://picsum.photos/seed/photo-med-3/600/350', 'https://picsum.photos/seed/photo-large-3/1000/600', '["https://picsum.photos/seed/photo-scr1-3/500/300", "https://picsum.photos/seed/photo-scr2-3/500/300", "https://picsum.photos/seed/photo-scr3-3/500/300"]', '2026-06-05 20:39:20'),
(4, 'Sleek Tailwind CSS Layouts', 'Choosing the right stack is critical. We dive deep into the trade-offs of using modern micro-frameworks. Leveraging modular component design patterns lets teams ship clean features faster.', 'Sophia Chen', 'General', 490, 'https://picsum.photos/seed/photo-sm-4/200/300', 'https://picsum.photos/seed/photo-med-4/600/350', 'https://picsum.photos/seed/photo-large-4/1000/600', '["https://picsum.photos/seed/photo-scr1-4/500/300", "https://picsum.photos/seed/photo-scr2-4/500/300", "https://picsum.photos/seed/photo-scr3-4/500/300"]', '2026-06-05 20:41:20'),
(5, 'The Secrets of Tailwind CSS Layouts', 'This approach has helped us scale to thousands of daily active users with minimal hosting costs. Make sure to structure your project files logically from day one to avoid technical debt.', 'Nikolai Volkov', 'Life', 814, 'https://picsum.photos/seed/photo-sm-5/200/300', 'https://picsum.photos/seed/photo-med-5/600/350', 'https://picsum.photos/seed/photo-large-5/1000/600', '["https://picsum.photos/seed/photo-scr1-5/500/300", "https://picsum.photos/seed/photo-scr2-5/500/300", "https://picsum.photos/seed/photo-scr3-5/500/300"]', '2026-06-05 20:43:20');

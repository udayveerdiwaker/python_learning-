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

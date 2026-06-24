# FastAPI Backend Architecture Walkthrough

This document provides a detailed breakdown of the `backend/main.py` application. The backend serves as a high-performance REST API designed to connect a React client with a MySQL/MariaDB database, providing full support for pagination, search, comments, user likes, cascading deletion, and database-wide stats.

---

## 1. Database & Connection Pooling
At startup, `main.py` establishes connection rules for MySQL:

1. **Auto-Database Creation**:
   It first makes a connection to the baseline MySQL instance to execute `CREATE DATABASE IF NOT EXISTS python_post_db` automatically.
2. **SQLAlchemy Engine**:
   Configured with two essential optimization flags:
   * `pool_recycle=3600`: Recycles idle connections every hour to prevent MySQL handshake timeouts.
   * `pool_pre_ping=True`: Pings the database on checkout to verify the connection is active, auto-reconnecting if it died.
3. **Session Factories**:
   `SessionLocal = sessionmaker(...)` creates transaction-safe sessions. The `get_db()` dependency generator cleans up these connections after each request.

---

## 2. Relational Database Models (SQLAlchemy)
The system maps two key relational tables in MySQL:

### **`posts` Table Model (`DBPost`)**
Stores the visual feeds, likes, and image paths:
* `id` (Primary Key, Auto-Increment)
* `title` (String, max 150 chars)
* `content` (Text block)
* `author` (String, max 50 chars)
* `category` (String, max 20 chars, default "General")
* `likes` (Integer counter, default 0)
* `small_cover_image`, `medium_cover_image`, `large_cover_image` (String paths)
* `screenshots` (JSON list to store gallery URLs)
* `created_at` (Datetime timestamp)

### **`comments` Table Model (`DBComment`)**
Stores comments linked to their parent posts:
* `id` (Primary Key, Auto-Increment)
* `post_id` (Integer, indexed for fast querying)
* `author` (String, max 50 chars)
* `content` (Text block)
* `created_at` (Datetime timestamp)

---

## 3. Pydantic Verification Schemas
Pydantic is used to validate inputs on incoming POST requests and serialize outputs on GET queries:

* **`PostCreate` / `CommentCreate`**: Enforce string length validation rules (e.g. `min_length=1`, `max_length=150` for post titles) and prevent empty submissions.
* **`Post` / `Comment`**: Serialize ORM models back to clean JSON nodes. Enforces relational count attributes like `comment_count` for card UI.

---

## 4. Optimized Seeding Strategy
To initialize the database with 10,000+ posts:
1. **Fallback Generation**: If `posts.json` is missing, `generate_mock_posts()` generates 10,000 stable seed records using pseudo-random seeds.
2. **Chunked Insertion**: To avoid packet size limits (`Got a packet bigger than 'max_allowed_packet' bytes`), records are bulk saved using `db.bulk_save_objects()` in optimized batches of **2,000 items**.

---

## 5. Security & Session Authorization
Authentication relies on the `verify_token` dependency injected into sensitive routes:
* **Bearer Token validation**: Enforced via FastAPI's `HTTPBearer` security middleware.
* **In-Memory Cache**: Active session tokens are stored in the `valid_tokens` set.
* **Key Generation**: `/api/auth/token` creates cryptographically secure hex keys (`secrets.token_hex(16)`) and registers them in the set.

---

## 6. Main REST API Endpoints

| Endpoint | Method | Security | Description |
| :--- | :---: | :---: | :--- |
| `/api/auth/token` | `GET` | Public | Generates a new cryptographic API key and saves it to the session token cache. |
| `/v1/api/get_posts` | `GET` | Public | Retrieves a paginated chunk of posts (default limit: 12). Supports `category` pills filtering and `search` query string logic. |
| `/v1/api/posts/search` | `GET` | Public | Legacy endpoint returning matching posts with a hard limit of 50. |
| `/v1/api/create_posts` | `POST` | protected | Publishes a new post record. Generates random cover and thumbnail assets if omitted. |
| `/v1/api/like_post/{id}` | `POST` | protected | Increments the like counter on the target post record. |
| `/v1/api/posts/delete/{id}` | `DELETE` | protected | Performs a cascading cleanup, deleting the post and all associated comments in a single database transaction. |
| `/v1/api/posts/{id}/comments` | `GET` | Public | Retrieves all comments for a post, ordered chronologically. |
| `/v1/api/posts/{id}/comments` | `POST` | protected | Appends a comment to the post. |
| `/v1/api/stats/summary` | `GET` | Public | Queries database counts for posts, total likes, and unique author names. |
| `/v1/api/stats/categories` | `GET` | Public | Groups and aggregates posts to return counts for each active category. |

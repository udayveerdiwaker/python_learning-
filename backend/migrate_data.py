import os
import sys
from datetime import datetime
import traceback

# Setup logging immediately
log_path = os.path.join(os.path.dirname(__file__), "migration_log.txt")
try:
    with open(log_path, "w", encoding="utf-8") as log_file:
        log_file.write(f"Migration script execution started at {datetime.now()}\n")
except Exception as e:
    sys.stderr.write(f"Error initializing log file: {e}\n")

# Custom print that logs to both console and file
old_print = print
def print(*args, **kwargs):
    old_print(*args, **kwargs)
    try:
        with open(log_path, "a", encoding="utf-8") as log_file:
            log_file.write(" ".join(map(str, args)) + "\n")
    except Exception:
        pass

# Now try importing libraries that might be missing
try:
    import json
    # pyrefly: ignore [missing-import]
    import mysql.connector
except Exception as e:
    error_msg = traceback.format_exc()
    print("FATAL ERROR: Missing libraries or failed import.")
    print(error_msg)
    print("Please make sure you installed the dependencies using:")
    print(".\\venv\\Scripts\\pip install -r requirements.txt")
    sys.exit(1)

# Connection config
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '',
}

def migrate():
    # 1. Connect to MySQL server
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        print("Connected to MySQL server successfully.")
    except Exception as e:
        print(f"Error connecting to MySQL: {e}")
        return

    # 2. Create database and table
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS python_post_db")
        cursor.execute("USE python_post_db")
        
        cursor.execute("""
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
            )
        """)
        print("Database 'python_post_db' and table 'posts' verified/created.")
    except Exception as e:
        print(f"Error creating database/table: {e}")
        cursor.close()
        conn.close()
        return

    # 3. Load posts.json
    json_path = os.path.join(os.path.dirname(__file__), "posts.json")
    if not os.path.exists(json_path):
        print(f"Error: {json_path} does not exist.")
        cursor.close()
        conn.close()
        return

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            posts = json.load(f)
        print(f"Loaded {len(posts)} posts from posts.json.")
    except Exception as e:
        print(f"Error loading posts.json: {e}")
        cursor.close()
        conn.close()
        return

    # 4. Clear existing posts to prevent duplication
    try:
        cursor.execute("SELECT COUNT(*) FROM posts")
        count = cursor.fetchone()[0]
        if count > 0:
            cursor.execute("TRUNCATE TABLE posts")
            print("Existing posts table cleared to overwrite with fresh posts.json data.")
    except Exception as e:
        print(f"Error checking table count: {e}")

    # 5. Insert data
    insert_query = """
        INSERT INTO posts (
            id, title, content, author, category, likes,
            small_cover_image, medium_cover_image, large_cover_image,
            screenshots, created_at
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    data_to_insert = []
    for p in posts:
        created_at_str = p.get("created_at")
        try:
            created_at_dt = datetime.fromisoformat(created_at_str.replace("Z", ""))
        except Exception:
            created_at_dt = datetime.now()

        screenshots_json = json.dumps(p.get("screenshots", []))

        data_to_insert.append((
            p.get("id"),
            p.get("title", ""),
            p.get("content", ""),
            p.get("author", ""),
            p.get("category", "General"),
            p.get("likes", 0),
            p.get("small_cover_image", ""),
            p.get("medium_cover_image", ""),
            p.get("large_cover_image", ""),
            screenshots_json,
            created_at_dt
        ))

    try:
        chunk_size = 100
        for i in range(0, len(data_to_insert), chunk_size):
            chunk = data_to_insert[i:i+chunk_size]
            cursor.executemany(insert_query, chunk)
            conn.commit()
            print(f"Successfully migrated records {i} to {i + len(chunk)}...")
        print("Data migration completed successfully!")
    except Exception as e:
        print(f"Error during bulk insert: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    try:
        migrate()
    except Exception as e:
        error_msg = traceback.format_exc()
        print(f"FATAL EXCEPTION in main execution flow:\n{error_msg}")

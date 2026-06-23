import json
import os

def generate_dump():
    json_path = os.path.join(os.path.dirname(__file__), "posts.json")
    sql_path = os.path.join(os.path.dirname(__file__), "posts_dump.sql")
    
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found.")
        return
        
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            posts = json.load(f)
    except Exception as e:
        print(f"Error reading posts.json: {e}")
        return
        
    print(f"Loaded {len(posts)} posts. Generating SQL dump...")
    
    with open(sql_path, "w", encoding="utf-8") as f:
        # Write Database and Table creation statements
        f.write("CREATE DATABASE IF NOT EXISTS python_post_db;\n")
        f.write("USE python_post_db;\n\n")
        f.write("DROP TABLE IF EXISTS posts;\n")
        f.write("""CREATE TABLE posts (
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
);\n\n""")
        
        # Batch insert statement construction
        batch_size = 500
        for i in range(0, len(posts), batch_size):
            batch = posts[i:i+batch_size]
            f.write("INSERT INTO posts (id, title, content, author, category, likes, small_cover_image, medium_cover_image, large_cover_image, screenshots, created_at) VALUES\n")
            
            values_list = []
            for post in batch:
                def escape(val):
                    if val is None:
                        return "NULL"
                    return str(val).replace("'", "''")
                
                pid = post.get("id")
                title = escape(post.get("title", ""))
                content = escape(post.get("content", ""))
                author = escape(post.get("author", ""))
                category = escape(post.get("category", "General"))
                likes = post.get("likes", 0)
                small_cover = escape(post.get("small_cover_image", ""))
                medium_cover = escape(post.get("medium_cover_image", ""))
                large_cover = escape(post.get("large_cover_image", ""))
                screenshots = escape(json.dumps(post.get("screenshots", [])))
                created_at = escape(post.get("created_at", ""))
                
                values_list.append(
                    f"({pid}, '{title}', '{content}', '{author}', '{category}', {likes}, '{small_cover}', '{medium_cover}', '{large_cover}', '{screenshots}', '{created_at}')"
                )
            
            f.write(",\n".join(values_list))
            f.write(";\n\n")
            
    print(f"SQL dump successfully generated: {sql_path}")

if __name__ == "__main__":
    generate_dump()

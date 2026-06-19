from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, timedelta
import secrets
import random
import uvicorn
import json
import os

app = FastAPI(title="Photo Feed API with JSON Persistence")

# Enable CORS for external websites to fetch data
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Token security helper
security = HTTPBearer()

# In-memory store for valid session tokens
valid_tokens = {"demo-secret-key-2026"}

# Database JSON file location
DB_FILE = "posts.json"

# Pydantic schemas with rich image fields
class PostCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=150)
    content: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1, max_length=50)
    category: str = Field("General", min_length=1, max_length=20)
    small_cover_image: Optional[str] = ""
    medium_cover_image: Optional[str] = ""
    large_cover_image: Optional[str] = ""
    screenshots: Optional[List[str]] = []

class Post(BaseModel):
    id: int
    title: str
    content: str
    author: str
    category: str
    likes: int
    small_cover_image: str
    medium_cover_image: str
    large_cover_image: str
    screenshots: List[str]
    created_at: str

# Mock Generator Helper (generating 10,000 rich photo feed items)
def generate_mock_posts(count: int = 10000) -> List[dict]:
    adjectives = ["Mastering", "Exploring", "The Future of", "Sleek", "Minimalist", "Unlocking", "Scaling", "Architecting", "Designing", "The Secrets of", "How to Build", "Advanced Guide to", "Next-Gen", "Introduction to"]
    topics = ["FastAPI APIs", "React 18 & Hooks", "Vite Dev Server", "Python Clean Code", "Tailwind CSS Layouts", "Cloud Services", "Machine Learning", "Frontend State", "Asynchronous Python", "Indie Hacking", "Responsive Design", "API Gateways", "Database Optimization", "UX Best Practices"]
    authors = ["Alex Rivera", "Sophia Chen", "Marcus Vance", "Elena Rostova", "Liam O'Connor", "Yuki Tanaka", "Zara Patel", "Amir Mansoor", "Chloe Dubois", "Diego Gomez", "Sarah Jenkins", "Nikolai Volkov", "Linus Lee", "Fatima Al-Sayed"]
    categories = ["Tech", "Idea", "Life", "General"]
    
    sentences = [
        "In this article, we cover key architectural decisions to maximize developer efficiency and system uptime.",
        "Choosing the right stack is critical. We dive deep into the trade-offs of using modern micro-frameworks.",
        "A clean and responsive interface is the boundary between user delight and frustration.",
        "Make sure to structure your project files logically from day one to avoid technical debt.",
        "Continuous iteration and user testing are the only ways to build a product people actually want.",
        "Optimizing performance requires understanding event loops, networking overhead, and browser rendering cycles.",
        "Security is not an afterthought. Always ensure you protect your endpoints with reliable authorization schemas.",
        "This approach has helped us scale to thousands of daily active users with minimal hosting costs.",
        "Leveraging modular component design patterns lets teams ship clean features faster."
    ]

    generated = []
    base_time = datetime.now()

    for idx in range(1, count + 1):
        random.seed(idx) # Keep generation stable
        adj = random.choice(adjectives)
        topic = random.choice(topics)
        title = f"{adj} {topic}"
        
        author = random.choice(authors)
        category = random.choice(categories)
        likes = random.randint(0, 950)
        
        content = " ".join(random.sample(sentences, k=random.randint(2, 3)))
        created_at = (base_time - timedelta(minutes=2 * (count - idx))).isoformat()
        
        generated.append({
            "id": idx,
            "title": title,
            "content": content,
            "author": author,
            "category": category,
            "likes": likes,
            "small_cover_image": f"https://picsum.photos/seed/photo-sm-{idx}/200/300",
            "medium_cover_image": f"https://picsum.photos/seed/photo-med-{idx}/600/350",
            "large_cover_image": f"https://picsum.photos/seed/photo-large-{idx}/1000/600",
            "screenshots": [
                f"https://picsum.photos/seed/photo-scr1-{idx}/500/300",
                f"https://picsum.photos/seed/photo-scr2-{idx}/500/300",
                f"https://picsum.photos/seed/photo-scr3-{idx}/500/300"
            ],
            "created_at": created_at
        })
        
    return generated

# Database File Operations
def save_posts_to_file(posts_list: List[dict]):
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(posts_list, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving to file database: {e}")

def load_posts_from_file() -> List[dict]:
    force_reseed = False
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                temp_posts = json.load(f)
                # Force reseed if the old movie attributes exist or count is < 10,000
                if len(temp_posts) < 10000 or "mpa_rating" in temp_posts[0] or "genres" in temp_posts[0]:
                    print("Existing database contains movie schemas or is undersized. Forcing clean reseed...")
                    force_reseed = True
        except Exception:
            force_reseed = True

    if not os.path.exists(DB_FILE) or force_reseed:
        print("JSON Database file not found or outdated. Seeding 10,000 photo posts...")
        seeded = generate_mock_posts(10000)
        save_posts_to_file(seeded)
        return seeded
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading JSON Database file: {e}. Re-seeding...")
        seeded = generate_mock_posts(10000)
        save_posts_to_file(seeded)
        return seeded

# Load active database state
posts = load_posts_from_file()
next_post_id = max([p["id"] for p in posts]) + 1 if posts else 1

# Dependency to verify token
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    if token not in valid_tokens:
        raise HTTPException(
            status_code=401, 
            detail="Invalid or expired API token. Please generate a new token."
        )
    return token

# Auth endpoints
@app.get("/api/auth/token")
def generate_token():
    token = secrets.token_hex(16)
    valid_tokens.add(token)
    return {"token": token}

# Post endpoints
@app.get("/v1/api/get_posts", response_model=List[Post])
def get_posts():
    return sorted(posts, key=lambda x: x["created_at"], reverse=True)

@app.post("/v1/api/create_posts", response_model=Post, status_code=201)
def create_post(post_in: PostCreate, token: str = Depends(verify_token)):
    global next_post_id
    
    # Generate default cover image fields if not specified
    sm = post_in.small_cover_image or f"https://picsum.photos/seed/photo-sm-{next_post_id}/200/300"
    med = post_in.medium_cover_image or f"https://picsum.photos/seed/photo-med-{next_post_id}/600/350"
    large = post_in.large_cover_image or f"https://picsum.photos/seed/photo-large-{next_post_id}/1000/600"
    
    new_post = {
        "id": next_post_id,
        "title": post_in.title.strip(),
        "content": post_in.content.strip(),
        "author": post_in.author.strip(),
        "category": post_in.category.strip(),
        "likes": 0,
        "small_cover_image": sm,
        "medium_cover_image": med,
        "large_cover_image": large,
        "screenshots": post_in.screenshots or [
            f"https://picsum.photos/seed/photo-scr1-{next_post_id}/500/300",
            f"https://picsum.photos/seed/photo-scr2-{next_post_id}/500/300",
            f"https://picsum.photos/seed/photo-scr3-{next_post_id}/500/300"
        ],
        "created_at": datetime.now().isoformat()
    }
    posts.append(new_post)
    next_post_id += 1
    
    # Persist state
    save_posts_to_file(posts)
    
    return new_post

@app.post("/v1/api/like_post/{post_id}", response_model=Post)
def like_post(post_id: int, token: str = Depends(verify_token)):
    for post in posts:
        if post["id"] == post_id:
            post["likes"] += 1
            save_posts_to_file(posts)
            return post
    raise HTTPException(status_code=404, detail="Post not found")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

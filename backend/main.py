from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, timedelta
import secrets
import random
import uvicorn
import os
import json

# SQLAlchemy imports
# pyrefly: ignore [missing-import]
from sqlalchemy import create_engine, Column, Integer, String, Text, JSON, DateTime, func, text
# pyrefly: ignore [missing-import]
from sqlalchemy.ext.declarative import declarative_base     
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import sessionmaker, Session

app = FastAPI(title="Photo Feed API with MySQL Persistence")

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

# Database URL for local MySQL instance
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+mysqlconnector://root:@127.0.0.1:3306/python_post_db")

# Attempt to check/create the database if it doesn't exist
try:
    base_url = DATABASE_URL.rsplit("/", 1)[0] + "/"
    temp_engine = create_engine(base_url)
    with temp_engine.connect() as conn:
        conn.execute(text("CREATE DATABASE IF NOT EXISTS python_post_db"))
        conn.commit()
    temp_engine.dispose()
    print("Database python_post_db verified/created.")
except Exception as e:
    print(f"Warning: Could not verify/create database: {e}")

# Create the SQLAlchemy Engine
engine = create_engine(
    DATABASE_URL,
    pool_recycle=3600,
    pool_pre_ping=True
)

# SessionLocal class is the factory that makes new database session objects
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()

# SQLAlchemy Model for Posts
class DBPost(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    content = Column(Text, nullable=False)
    author = Column(String(50), nullable=False)
    category = Column(String(20), default="General")
    likes = Column(Integer, default=0)
    small_cover_image = Column(String(255), default="")
    medium_cover_image = Column(String(255), default="")
    large_cover_image = Column(String(255), default="")
    screenshots = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# SQLAlchemy Model for Comments
class DBComment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, nullable=False, index=True)
    author = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic schemas
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
    created_at: datetime
    comment_count: Optional[int] = 0

    class Config:
        from_attributes = True

class CommentCreate(BaseModel):
    author: str = Field(..., min_length=1, max_length=50)
    content: str = Field(..., min_length=1)

class Comment(BaseModel):
    id: int
    post_id: int
    author: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True

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

# Seed the database if empty
def seed_database():
    db = SessionLocal()
    try:
        if db.query(DBPost).count() == 0:
            posts_data = []
            # Check if posts.json exists and load from it
            db_file = os.path.join(os.path.dirname(__file__), "posts.json")
            if os.path.exists(db_file):
                print(f"Loading seed data from {db_file}...")
                try:
                    with open(db_file, "r", encoding="utf-8") as f:
                        posts_data = json.load(f)
                except Exception as e:
                    print(f"Error reading posts.json: {e}")
            
            # Fallback to generating mock posts if posts.json is missing/empty
            if not posts_data:
                print("posts.json not found or empty. Generating mock posts...")
                posts_data = generate_mock_posts(10000)
            
            print(f"Seeding {len(posts_data)} posts into MySQL...")
            db_posts = []
            for p in posts_data:
                created_at_val = p.get("created_at")
                if isinstance(created_at_val, str):
                    try:
                        # Clean Z suffix or microsecond differences
                        cleaned_time = created_at_val.replace("Z", "")
                        created_dt = datetime.fromisoformat(cleaned_time)
                    except ValueError:
                        created_dt = datetime.utcnow()
                else:
                    created_dt = datetime.utcnow()

                db_posts.append(DBPost(
                    id=p["id"],
                    title=p.get("title", ""),
                    content=p.get("content", ""),
                    author=p.get("author", ""),
                    category=p.get("category", "General"),
                    likes=p.get("likes", 0),
                    small_cover_image=p.get("small_cover_image", ""),
                    medium_cover_image=p.get("medium_cover_image", ""),
                    large_cover_image=p.get("large_cover_image", ""),
                    screenshots=p.get("screenshots", []),
                    created_at=created_dt
                ))
            
            # Bulk save in chunks of 2000 to prevent buffer overflow/issues on some setups
            chunk_size = 2000
            for i in range(0, len(db_posts), chunk_size):
                db.bulk_save_objects(db_posts[i:i+chunk_size])
                db.commit()
            print("Database seeding completed.")
    except Exception as e:
        print(f"Error seeding database: {e}")
    finally:
        db.close()

seed_database()

# Dependency to get db session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
@app.get("/v1/api/get_posts")
def get_posts(
    page: int = 1,
    limit: int = 12,
    category: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(DBPost)
    
    if category and category != "All" and category != "Liked":
        query = query.filter(DBPost.category == category)
        
    if search:
        search_query = f"%{search}%"
        query = query.filter(
            (DBPost.title.like(search_query)) |
            (DBPost.content.like(search_query)) |
            (DBPost.author.like(search_query))
        )
        
    total = query.count()
    
    posts = query.order_by(DBPost.created_at.desc())\
                 .offset((page - 1) * limit)\
                 .limit(limit)\
                 .all()
                 
    # Build response with comment counts
    posts_list = []
    for p in posts:
        comment_count = db.query(DBComment).filter(DBComment.post_id == p.id).count()
        posts_list.append({
            "id": p.id,
            "title": p.title,
            "content": p.content,
            "author": p.author,
            "category": p.category,
            "likes": p.likes,
            "small_cover_image": p.small_cover_image,
            "medium_cover_image": p.medium_cover_image,
            "large_cover_image": p.large_cover_image,
            "screenshots": p.screenshots or [],
            "created_at": p.created_at,
            "comment_count": comment_count
        })
        
    return {
        "total": total,
        "page": page,
        "limit": limit,
        "posts": posts_list
    }

@app.get("/v1/api/posts/search")
def search_posts(query: str, db: Session = Depends(get_db)):
    search_query = f"%{query}%"
    posts = db.query(DBPost).filter(
        (DBPost.title.like(search_query)) |
        (DBPost.content.like(search_query)) |
        (DBPost.author.like(search_query))
    ).order_by(DBPost.created_at.desc()).limit(50).all()
    
    posts_list = []
    for p in posts:
        comment_count = db.query(DBComment).filter(DBComment.post_id == p.id).count()
        posts_list.append({
            "id": p.id,
            "title": p.title,
            "content": p.content,
            "author": p.author,
            "category": p.category,
            "likes": p.likes,
            "small_cover_image": p.small_cover_image,
            "medium_cover_image": p.medium_cover_image,
            "large_cover_image": p.large_cover_image,
            "screenshots": p.screenshots or [],
            "created_at": p.created_at,
            "comment_count": comment_count
        })
    return posts_list

@app.post("/v1/api/create_posts", response_model=Post, status_code=201)
def create_post(post_in: PostCreate, token: str = Depends(verify_token), db: Session = Depends(get_db)):
    max_id = db.query(func.max(DBPost.id)).scalar() or 0
    seed_id = max_id + 1

    sm = post_in.small_cover_image or f"https://picsum.photos/seed/photo-sm-{seed_id}/200/300"
    med = post_in.medium_cover_image or f"https://picsum.photos/seed/photo-med-{seed_id}/600/350"
    large = post_in.large_cover_image or f"https://picsum.photos/seed/photo-large-{seed_id}/1000/600"
    scr = post_in.screenshots or [
        f"https://picsum.photos/seed/photo-scr1-{seed_id}/500/300",
        f"https://picsum.photos/seed/photo-scr2-{seed_id}/500/300",
        f"https://picsum.photos/seed/photo-scr3-{seed_id}/500/300"
    ]

    new_post = DBPost(
        title=post_in.title.strip(),
        content=post_in.content.strip(),
        author=post_in.author.strip(),
        category=post_in.category.strip(),
        likes=0,
        small_cover_image=sm,
        medium_cover_image=med,
        large_cover_image=large,
        screenshots=scr,
        created_at=datetime.utcnow()
    )
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.post("/v1/api/like_post/{post_id}", response_model=Post)
def like_post(post_id: int, token: str = Depends(verify_token), db: Session = Depends(get_db)):
    db_post = db.query(DBPost).filter(DBPost.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    db_post.likes += 1
    db.commit()
    db.refresh(db_post)
    return db_post

@app.delete("/v1/api/posts/delete/{post_id}")
def delete_post(post_id: int, token: str = Depends(verify_token), db: Session = Depends(get_db)):
    db_post = db.query(DBPost).filter(DBPost.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Also delete comments for this post
    db.query(DBComment).filter(DBComment.post_id == post_id).delete()
    
    db.delete(db_post)
    db.commit()
    return {"detail": "Post and associated comments successfully deleted."}

# Comment endpoints
@app.get("/v1/api/posts/{post_id}/comments", response_model=List[Comment])
def get_comments(post_id: int, db: Session = Depends(get_db)):
    return db.query(DBComment).filter(DBComment.post_id == post_id).order_by(DBComment.created_at.asc()).all()

@app.post("/v1/api/posts/{post_id}/comments", response_model=Comment, status_code=201)
def create_comment(
    post_id: int, 
    comment_in: CommentCreate, 
    token: str = Depends(verify_token), 
    db: Session = Depends(get_db)
):
    db_post = db.query(DBPost).filter(DBPost.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")

    new_comment = DBComment(
        post_id=post_id,
        author=comment_in.author.strip(),
        content=comment_in.content.strip(),
        created_at=datetime.utcnow()
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

# Stats endpoints
@app.get("/v1/api/stats/categories")
def get_category_stats(db: Session = Depends(get_db)):
    results = db.query(DBPost.category, func.count(DBPost.id)).group_by(DBPost.category).all()
    return [{"category": r[0] or "General", "count": r[1]} for r in results]

@app.get("/v1/api/stats/summary")
def get_summary_stats(db: Session = Depends(get_db)):
    total_posts = db.query(DBPost).count()
    total_likes = db.query(func.sum(DBPost.likes)).scalar() or 0
    unique_authors = db.query(DBPost.author).distinct().count()
    return {
        "total_posts": total_posts,
        "total_likes": total_likes,
        "unique_authors": unique_authors
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

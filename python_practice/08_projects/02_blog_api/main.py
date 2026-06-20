# main.py
import sys
from pathlib import Path

# Add parent directory for imports
sys.path.append(str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from db_helper import get_db
import crud
import schemas
from security_helper import get_current_user_from_token

app = FastAPI(
    title="Blog Engine Micro-Service",
    description="Project 2: Relational category posts, ownership validation, and CRUD operations.",
    version="1.0.0"
)

# ------------------------------------------------------------------------------
# Category Endpoints
# ------------------------------------------------------------------------------
@app.get("/categories", response_model=List[schemas.CategoryResponse], tags=["Categories"])
def read_categories(db: Session = Depends(get_db)):
    return crud.get_categories(db)

@app.post("/categories", response_model=schemas.CategoryResponse, status_code=status.HTTP_201_CREATED, tags=["Categories"])
def create_new_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    db_cat = crud.get_category_by_name(db, category.name)
    if db_cat:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category already exists."
        )
    return crud.create_category(db, category)


# ------------------------------------------------------------------------------
# Blog Endpoints
# ------------------------------------------------------------------------------
@app.get("/blogs", response_model=List[schemas.BlogResponse], tags=["Blogs"])
def read_blogs(category_id: Optional[int] = None, db: Session = Depends(get_db)):
    """
    Retrieves all blog posts. Optional filter by category.
    """
    return crud.get_blogs(db, category_id=category_id)


@app.get("/blogs/{blog_id}", response_model=schemas.BlogResponse, tags=["Blogs"])
def read_single_blog(blog_id: int, db: Session = Depends(get_db)):
    db_blog = crud.get_blog_by_id(db, blog_id)
    if not db_blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog post not found."
        )
    return db_blog


@app.post("/blogs", response_model=schemas.BlogResponse, status_code=status.HTTP_201_CREATED, tags=["Blogs"])
def create_new_blog(
    blog: schemas.BlogCreate, 
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Creates a new blog post. Requires a valid JWT token.
    The author_id is automatically extracted from the token.
    """
    return crud.create_blog(db, blog, author_id=current_user["id"])


@app.put("/blogs/{blog_id}", response_model=schemas.BlogResponse, tags=["Blogs"])
def update_existing_blog(
    blog_id: int, 
    blog_update: schemas.BlogUpdate, 
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Updates an existing blog post.
    Validates that the editor is the original author of the post.
    """
    db_blog = crud.get_blog_by_id(db, blog_id)
    if not db_blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog post not found."
        )
        
    # Ownership authorization check
    if db_blog.author_id != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to edit this post."
        )
        
    return crud.update_blog(db, blog_id, blog_update)


@app.delete("/blogs/{blog_id}", status_code=status.HTTP_200_OK, tags=["Blogs"])
def delete_existing_blog(
    blog_id: int, 
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Deletes an existing blog post.
    Authorized for the post author or an administrator role.
    """
    db_blog = crud.get_blog_by_id(db, blog_id)
    if not db_blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog post not found."
        )
        
    # Authorization: Author OR Admin role can delete
    if db_blog.author_id != current_user["id"] and current_user["role"] != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this post."
        )
        
    crud.delete_blog(db, blog_id)
    return {"message": "Blog post deleted successfully."}

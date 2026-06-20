# crud.py
from sqlalchemy.orm import Session
from models import DBBlog, DBCategory
from schemas import BlogCreate, BlogUpdate, CategoryCreate

# ------------------------------------------------------------------------------
# Category CRUD Helpers
# ------------------------------------------------------------------------------
def get_categories(db: Session):
    return db.query(DBCategory).all()

def get_category_by_name(db: Session, name: str):
    return db.query(DBCategory).filter(DBCategory.name == name).first()

def create_category(db: Session, category: CategoryCreate):
    db_category = DBCategory(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


# ------------------------------------------------------------------------------
# Blog CRUD Helpers
# ------------------------------------------------------------------------------
def get_blogs(db: Session, category_id: int = None, limit: int = 20):
    query = db.query(DBBlog)
    if category_id:
        query = query.filter(DBBlog.category_id == category_id)
    return query.limit(limit).all()

def get_blog_by_id(db: Session, blog_id: int):
    return db.query(DBBlog).filter(DBBlog.id == blog_id).first()

def create_blog(db: Session, blog: BlogCreate, author_id: int):
    db_blog = DBBlog(
        title=blog.title,
        content=blog.content,
        category_id=blog.category_id,
        author_id=author_id
    )
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog

def update_blog(db: Session, blog_id: int, blog_update: BlogUpdate):
    db_blog = get_blog_by_id(db, blog_id)
    if not db_blog:
        return None
        
    update_data = blog_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_blog, key, value)
        
    db.commit()
    db.refresh(db_blog)
    return db_blog

def delete_blog(db: Session, blog_id: int):
    db_blog = get_blog_by_id(db, blog_id)
    if db_blog:
        db.delete(db_blog)
        db.commit()
        return True
    return False

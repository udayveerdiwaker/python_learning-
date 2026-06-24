from database import engine
from models import Base

def create_database():
    print("Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database 'chat.db' and tables created successfully!")

if __name__ == "__main__":
    create_database()

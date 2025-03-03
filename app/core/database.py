from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.settings import DATABASE_URL
from models.base_model import Base


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Function to create all tables
def create_tables():
    Base.metadata.create_all(bind=engine)

# Dependency to use in routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
